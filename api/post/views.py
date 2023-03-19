# 2023-02-16
# post/views.py

from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import PostSerializer
from .models import Author
from .models import Post
from utils.permissions import IsAuthenticatedWithJWT, NodeReadOnly, OwnerCanWrite

import logging
logger = logging.getLogger('django')
rev = 'rev: $xujSyn7$x'

# This code is modifed from a video tutorial from Cryce Truly on 2020-06-19 retrieved on 2023-02-16, to Youtube crycetruly
# video here:
# https://youtu.be/B3HGwFlBvi8
class PostListCreateView(ListCreateAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_url_kwarg = 'author_uuid'
    permission_classes = [IsAuthenticatedWithJWT|OwnerCanWrite|NodeReadOnly]

    def perform_create(self, serializer):
        logger.info(rev)
        author_uuid = self.kwargs.get(self.lookup_url_kwarg)
        author_obj = Author.objects.get(id=author_uuid)
        logger.info('Creating new post for author_uuid: [%s]', author_uuid)
        return serializer.save(author=author_obj)
    
    def get_queryset(self):
        logger.info(rev)
        author_uuid = self.kwargs.get(self.lookup_url_kwarg)
        if (self.request.query_params): # type: ignore
            logger.info('Get recent posts for author_uuid: [%s] with query_params [%s]', author_uuid, str(self.request.query_params)) # type: ignore
        else:
            logger.info('Get recent posts for author_uuid: [%s]', author_uuid)
        return self.queryset.filter(author_id=author_uuid).order_by('-published')

class PostDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_field = 'id'
    permission_classes = [IsAuthenticatedWithJWT|OwnerCanWrite|NodeReadOnly]

    def get_object(self):
        logger.info(rev)
        post_id = self.kwargs.get(self.lookup_field)
        logger.info('Getting content for post id: [%s]', post_id)
        return super().get_object()

    def post(self, request, *args, **kwargs):
        logger.info(rev)
        return self.update(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        logger.info(rev)
        post_uuid = kwargs.get(self.lookup_field)
        author_uuid = kwargs.get('author_uuid')
        post_exists = True if Post.objects.filter(id=post_uuid).exists() else False
        serializer = PostSerializer()
        if post_exists:
            logger.info('Got PUT request for post update for author_uuid: [%s] at id: [%s]', author_uuid, post_uuid)
            post_obj = Post.objects.get(id=post_uuid)
            serializer = PostSerializer(post_obj, data=request.data, partial=True)
        else:
            logger.info('Got PUT request for new post for author_uuid: [%s] at id: [%s]', author_uuid, post_uuid)
            serializer = PostSerializer(data=request.data)
    
        if serializer.is_valid():
            if Author.objects.filter(id=author_uuid):
                author_obj = Author.objects.get(id=author_uuid)
                obj, created = Post.objects.update_or_create(id=kwargs['id'], author=author_obj, defaults=serializer.validated_data)
                obj_serializer = PostSerializer(obj)
                return Response(obj_serializer.data, status=status.HTTP_201_CREATED) if created else Response(obj_serializer.data)
            else:
                logger.error('Cannot create/update post for unknown author id: [%s]', kwargs['author_uuid'])
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def perform_destroy(self, instance):
        logger.info(rev)
        post_id = self.kwargs.get(self.lookup_field)
        logger.info('Deleting post id: [%s]', post_id)
        return super().perform_destroy(instance)
