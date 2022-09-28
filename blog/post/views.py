from .models import CustomUser
from .serializers import *
import post.services as services
from rest_framework import generics, permissions, viewsets
from rest_framework.response import Response
from django.db import IntegrityError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from post.permission import IsOwnerOrReadOnly
import post.generics as additional_generics


@csrf_exempt
def registration(request):
    if request.method == 'POST':
        token = services.registration(request)
        return token


@csrf_exempt
def authentication(request):
    if request.method == 'POST':
        token = services.authentication(request)
        return token


class UserList(generics.ListAPIView):
    queryset = services.get_user_list()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def __str__(self):
        return 'UserListView'


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = services.get_user_list()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def __str__(self):
        return 'UserDetailView'


class PostList(generics.ListCreateAPIView):
    queryset = services.get_post_list(serializer=False)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

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
    queryset = services.get_post_list(serializer=False)
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_update(self, serializer):
        services.update_post_edit_date(serializer)
        serializer.save()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance = services.add_post_view(instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def __str__(self):
        return 'PostDetailView'


class CommentList(generics.ListCreateAPIView):
    queryset = services.get_comment_list()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CommentCreateSerializer
        else:
            return CommentSerializer

    def list(self, request, *args, **kwargs):
        return Response(services.get_comment_on_post(self, request, *args, **kwargs))

    def perform_create(self, serializer):
        serializer.save(comment_author=self.request.user)

    def __str__(self):
        return 'CommentListView'


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = services.get_comment_list()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def __str__(self):
        return 'CommentDetailView'


class RubricList(generics.ListAPIView):
    serializer_class = RubricSerializer
    queryset = services.get_rubric()
    permission_classes = [permissions.AllowAny]

    def __str__(self):
        return 'RubricListView'


class RubricDetail(additional_generics.CreateUpdateDestroyAPIView):
    serializer_class = RubricSerializer
    queryset = services.get_rubric()
    permission_classes = [permissions.IsAdminUser]

    def __str__(self):
        return 'RubricDetailView'