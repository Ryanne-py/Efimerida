from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, permissions, views
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from .models import CustomUser
from .permission import IsOwnerOrReadOnly
from .serializers import CustomUserSerializer
from .services import UserServices
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect

from post.serializers import PostCreateSerializer, PostSerializer


@csrf_exempt
def registration(request):
    if request.method == 'POST':
        token = UserServices.registration(request)
        return token
    else:
        return JsonResponse({'Error': f'Method {request.method} not allowed'}, status=400)

# @csrf_exempt
# def check_activate(requests):

@csrf_exempt
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and Token.objects.filter(user=user).exists():
        user.is_active = True
        user.save()
        return redirect('http://localhost:5173/')
    else:
        return redirect('https://octobrowser.net/ru/')


@csrf_exempt
def authentication(request):
    if request.method == 'POST':
        token = UserServices.authentication(request)
        return token
    else:
        return JsonResponse({'Error': f'Method {request.method} not allowed'}, status=400)


class BookmarksList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        response = UserServices.del_bookmarks(request.user, kwargs['post_id'])
        return response

    def create(self, request, *args, **kwargs):
        response = UserServices.add_bookmarks(request.user, kwargs['post_id'])
        return response

    def get_queryset(self):
        return UserServices.get_bookmarks(self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PostCreateSerializer
        else:
            return PostSerializer

    def __str__(self):
        return 'BookmarksListView'


class UserSubscribeList(generics.ListAPIView):
    permissions = [permissions.AllowAny]
    serializer_class = CustomUserSerializer

    def get_queryset(self):
        queryset = UserServices.get_subscribe(self.request.user)
        return queryset


class UserSubscribe(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, **kwargs):
        detail, status = UserServices.subscribe(request.user, kwargs['pk'])
        return Response(detail, status=status)

    def delete(self, request, **kwargs):
        detail, status = UserServices.unsubscribe(request.user, kwargs['pk'])
        return Response(detail, status=status)


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

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, args, kwargs)
        response.data['subscribers'] = UserServices.get_subscriber(kwargs['pk'])
        return response

    def __str__(self):
        return 'UserDetailView'
