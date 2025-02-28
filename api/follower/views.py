# 2023-03-15
# follower/views.py

from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from author.models import Author
from .serializers import FollowerSerializer
from .pagination import FollowerPagination
from .models import Follower
from utils.permissions import IsAuthenticatedWithJWT, NodeReadOnly, IsOwner
from utils.helper_funcs import toLastModifiedHeader

import logging
logger = logging.getLogger('django')
rev = 'rev: $jsadasd'

class FollowerListView(ListAPIView):
    serializer_class = FollowerSerializer
    queryset = Follower.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = FollowerPagination
    lookup_url_kwarg = 'author_uuid'
    
    def get_queryset(self):
        logger.info(rev)
        author_uuid = self.kwargs.get(self.lookup_url_kwarg)
        if (self.request.query_params):
            logger.info('Get recent followers for author_uuid: [%s] with query_params [%s]', author_uuid, str(self.request.query_params))
        else:
            logger.info('Get recent followers for author_uuid: [%s]', author_uuid)
        return self.queryset.filter(followee=author_uuid).order_by('-followed_at')

class FollowerDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = FollowerSerializer
    queryset = Follower.objects.all()
    permission_classes = [IsAuthenticatedWithJWT|NodeReadOnly|IsOwner]
    http_method_names = ['get', 'put', 'delete', 'head', 'options']
    lookup_field = 'follower_node_id'
    error = {
            "404_error":{
                "Error": "Author not found",
                },
            "400_error":{
                "Error":"Author already follows"
                },
        }
    
    def get(self, request, *args, **kwargs):
        logger.info(rev)
        follower = kwargs.get(self.lookup_field)
        followee = Author.objects.get(id=kwargs.get('author_uuid', ''))
        logger.info('Trying to find follower: [%s] for followee [%s]', follower, followee)
        try:
            instance = Follower.objects.get(follower_node_id=follower, followee=followee)
        except Exception as e:
            logger.info('Could not find follower: [%s] for followee [%s]. e [%s]', follower, followee, e)
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = FollowerSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK, headers={'Last-Modified': toLastModifiedHeader(instance.followed_at)})
    
    def put(self, request, *args, **kwargs):
        followee = Author.objects.get(id=kwargs['author_uuid'])
        follower_url = kwargs.get(self.lookup_field)
        exists = Follower.objects.filter(followee=followee, follower_node_id=follower_url)
        if exists:
            logger.error('Follower [%s] already exists for author_uuid [%s]', follower_url, str(followee.id))
            return Response(self.error["400_error"],status=status.HTTP_400_BAD_REQUEST)
        else:
            created = Follower.objects.create(followee=followee, follower_node_id=follower_url)
            serializer = FollowerSerializer(created)
            if created:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                logger.error('Failed to create follower [%s] for author_uuid [%s]', follower_url, str(followee.id))
                return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        logger.info(rev)
        follower = self.kwargs.get(self.lookup_field)
        followee = Author.objects.get(id=self.kwargs['author_uuid'])
        logger.info('Trying to delete follower: [%s] from followee [%s]', follower, followee)
        instance = Follower.objects.filter(follower_node_id=follower, followee=followee)
        if not instance: return Response(status=status.HTTP_404_NOT_FOUND)

        was_deleted, the_deleted = instance.delete()
        if was_deleted and was_deleted == 1:
            logger.info('Successfully deleted follower [%s] from followee [%s]', follower, followee)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            logger.error('Failed to delete follower [%s] from followee [%s] e [%s] [%s]', follower, followee, was_deleted, the_deleted)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
