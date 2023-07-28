from django.http import JsonResponse, Http404
from rest_framework.generics import get_object_or_404

from .dataclasses import Filters
from .serializers import *
from .services import *
from rest_framework import generics, permissions, views
from rest_framework.response import Response
from .generics import PostListWithFilterAPIView
from .permission import IsOwnerOrReadOnly
from user.services import UserServices
import dataclasses


class PostList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return PostServices.get_post_list().filter(is_finished=True)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PostCreateSerializer
        else:
            return PostSerializer

    def perform_create(self, serializer):
        serializer.save(post_author=self.request.user)

    def __str__(self):
        return 'PostListView'


class PostListBySubscription(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer

    def get_queryset(self):
        user_sub_list = UserServices.get_subscribe(self.request.user)
        empty_queryset = Post.objects.filter(id__lt=0).filter(is_finished=True)
        for user in user_sub_list:
            filters = Filters(post_author=user.username)
            post = PostServices.get_posts_by_filters(filters.dict())
            empty_queryset = empty_queryset | post

        return empty_queryset.order_by('-post_created_date')

    def __str__(self):
        return 'PostListBySubscriptionView'


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostCreateSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PostSerializer
        else:
            return PostCreateSerializer

    def get_object(self):
        obj = super().get_object()
        if obj.is_finished is False and obj.post_author != self.request.user:
            raise Http404
        return obj

    def get_queryset(self):
        return PostServices.get_post_list()

    def perform_update(self, serializer):
        PostServices.update_post_edit_date(serializer)
        serializer.save()

    def retrieve(self, request, *args, **kwargs):
        instance: Post = self.get_object()
        instance = PostServices.add_post_view(instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def __str__(self):
        return 'PostDetailView'


class PostDraft(generics.GenericAPIView):
    serializer_class = PostSerializer

    def post(self, request, **kwargs):
        if Post.objects.get(id=kwargs['pk']).post_author != request.user:
            return JsonResponse(
                {'detail': 'You do not have permission to do this'},
                status=400
            )
        detail, status = PostServices.add_post_to_draft(kwargs['pk'])
        return Response(detail, status=status)

    def delete(self, request, **kwargs):
        if Post.objects.get(id=kwargs['pk']).post_author != request.user:
            return JsonResponse(
                {'detail': 'You do not have permission to do this'},
                status=400
            )
        detail, status = PostServices.dell_post_from_draft(kwargs['pk'])
        return Response(detail, status=status)

    def get(self, requests, **kwargs):
        queryset = PostServices.get_post_list().filter(post_author=requests.user).filter(is_finished=False)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def __str__(self):
        return 'PostDraftView'


class PostListByFilter(PostListWithFilterAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return PostServices.get_post_list().filter(is_finished=True)


class PostLike(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, **kwargs):
        detail, status = PostServices.like_post(request.user, kwargs['pk'])
        return Response(detail, status=status)

    def delete(self, request, **kwargs):
        detail, status = PostServices.cancel_like(request.user, kwargs['pk'])
        return Response(detail, status=status)


class CommentList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return CommentServices.get_comment_on_post(self.kwargs['pk'])

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CommentCreateSerializer
        else:
            return CommentSerializer

    def perform_create(self, serializer):
        serializer.save(comment_author=self.request.user)

    def __str__(self):
        return 'CommentListView'


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        return CommentServices.get_comment_list()

    def __str__(self):
        return 'CommentDetailView'


class RubricList(generics.ListCreateAPIView):
    serializer_class = RubricSerializer

    def get_queryset(self):
        return RubricServices.get_rubric()

    def get_permissions(self):
        if self.request.method == 'POST':
            permission_classes = [permissions.IsAdminUser]
        elif self.request.method == 'GET':
            permission_classes = [permissions.AllowAny]

        return [permission() for permission in permission_classes]

    def __str__(self):
        return 'RubricListView'


class RubricDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RubricSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return RubricServices.get_rubric()

    def __str__(self):
        return 'RubricDetailView'


class TagList(generics.ListCreateAPIView):
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return TagServices.get_tags()

    def __str__(self):
        return 'TagListView'


class TagDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return TagServices.get_tags()


    def __str__(self):
        return 'TagDetailView'