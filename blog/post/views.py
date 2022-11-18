from .models import CustomUser
from .serializers import *
from post.services import *
from rest_framework import generics, permissions, views
from rest_framework.response import Response
from django.db import IntegrityError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from post.permission import IsOwnerOrReadOnly
import post.generics as additional_generics


@csrf_exempt
def registration(request):
    if request.method == 'POST':
        token = UserServices.registration(request)
        return token


@csrf_exempt
def authentication(request):
    if request.method == 'POST':
        token = UserServices.authentication(request)
        return token


class UserList(generics.ListAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return UserServices.get_user_list()

    def __str__(self):
        return 'UserListView'


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        return UserServices.get_user_list()

    def __str__(self):
        return 'UserDetailView'


class PostList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return PostServices.get_post_list()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PostCreateSerializer
        else:
            return PostSerializer

    def perform_create(self, serializer):
        serializer.save(post_author=self.request.user)

    def __str__(self):
        return 'PostListView'


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        return PostServices.get_post_list()

    def perform_update(self, serializer):
        PostServisec.update_post_edit_date(serializer)
        serializer.save()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance = PostServices.add_post_view(instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def __str__(self):
        return 'PostDetailView'


class PostListByFilter(additional_generics.PostListWithFilterAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return PostServices.get_post_list()


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
        return CommentServices.get_comment_list()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CommentCreateSerializer
        else:
            return CommentSerializer

    def list(self, request, *args, **kwargs):
        serializer, status = CommentServices.get_comment_on_post(self, kwargs['pk'])
        return Response(serializer.data, status=status)

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