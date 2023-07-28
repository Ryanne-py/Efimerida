from rest_framework import mixins, views, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from post.services import *
from post.dataclasses import Filters
from post.serializers import PostSerializer
from post.services import *

from .services import PostServices


class PostListWithFilterAPIView(mixins.CreateModelMixin,
                                GenericAPIView):
    """
    Concrete view for listing a queryset with filters that was give in request
    """

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        filters = Filters(**request.data)
        queryset_posts = PostServices.get_posts_by_filters(filters.dict())
        serializer = PostSerializer(queryset_posts, many=True)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, headers=headers)

    def perform_create(self, serializer):
        serializer.save()