# 2023-02-25
# comment/views.py

from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Comment
from .pagination import CommentPagination
from .serializers import CommentSerializer
from post.models import Post
from post.serializers import PostSerializer
from utils.permissions import NodeReadOnly

import logging
logger = logging.getLogger('django')
rev = 'rev: $xuasEcn7$x'

import logging
logger = logging.getLogger('django')
rev = 'rev: $xujSyn7$x' # not really sure what to set this to

class CommentListCreateView(ListCreateAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    pagination_class = CommentPagination
    lookup_url_kwarg = 'post_uuid'
    permission_classes = [IsAuthenticated|NodeReadOnly]

    @extend_schema(
        operation_id='comment_create'
    )
    def perform_create(self, serializer):
        logger.info(rev)
        post_uuid = self.kwargs.get(self.lookup_url_kwarg)
        post_obj = Post.objects.get(id=post_uuid)
        logger.info('Creating comment for post_uuid: [%s]', post_uuid)
        author_url = PostSerializer(post_obj).data['author']['id']
        return serializer.save(post=post_obj, author=author_url)
    
    def get_queryset(self):
        logger.info(rev)
        self.request.kwargs = self.kwargs
        post_uuid = self.kwargs.get(self.lookup_url_kwarg)
        if (self.request.query_params):
            logger.info('Get recent comments for post_uuid: [%s] with query_params [%s]', post_uuid, str(self.request.query_params))
        else:
            logger.info('Get recent comments for post_uuid: [%s]', post_uuid)
        return self.queryset.filter(post_id=post_uuid).order_by('-published')
