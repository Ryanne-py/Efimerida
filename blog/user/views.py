from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, permissions
from .permission import IsOwnerOrReadOnly
from .serializers import CustomUserSerializer
from .services import UserServices


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
