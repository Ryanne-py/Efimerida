from django.db import IntegrityError
from django.utils import timezone
from rest_framework.exceptions import ParseError
from .models import Post, Rubric, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token
from .models import CustomUser
from django.http import JsonResponse
from django.contrib.auth import authenticate


def get_post_detail(pk=None):
    post = Post.objects.prefetch_related("post_tags").select_related('post_rubric').get_object_or_404(pk=pk)
    comments = Comment.objects.filter(comment_post=pk)
    serializer_post = PostSerializer(post, many=False)
    serializer_comment = CommentSerializer(comments, many=True)
    return {'post': serializer_post.data, 'comment': serializer_comment.data}


def update_post_edit_date(serializer):
    serializer.instance.post_edit_date = timezone.now()
    serializer.save()


def add_post_view(instance):
    instance.post_views += 1
    instance.save()
    return instance


def get_rubric():
    rubrics = Rubric.objects.all()
    return rubrics


def get_comment_list():
    comment = Comment.objects.all()
    return comment


def registration(request):
    try:
        data = JSONParser().parse(request)
        user = CustomUser.objects.create(
            username=data['username'],
            email=data['email'],
            password=data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return JsonResponse({'token': str(token)}, status=201)
    except IntegrityError:
        return JsonResponse(
            {'error': 'username taken. choose another username'}, status=400)
    except ParseError:
        return JsonResponse(
            {'error': 'you need to send data for registration'}, status=400)
    except KeyError:
        return JsonResponse(
            {'error': 'you need to fill in all fields for registration (username, email, password'}, status=400)


def authentication(request):
    data = JSONParser().parse(request)
    user = authenticate(request, username=data['username'],
                        password=data['password'])
    if user is None:
        return JsonResponse(
            {'error': 'unable to login. check username and password'}, status=400)
    else:
        token = Token.objects.get_or_create(user=user)
        return JsonResponse({'token': str(token[0])}, status=201)


def get_post_list(serializer: bool):
    posts = Post.objects.select_related('post_rubric').prefetch_related("post_tags").all().filter(
        post_created_date__lte=timezone.now()).order_by('post_created_date')
    if serializer:
        posts = PostSerializer(posts, many=True)
    return posts


def get_comment_on_post(generic, request, *args, **kwargs):
    queryset = generic.filter_queryset(generic.get_queryset())
    queryset = queryset.filter(comment_post=kwargs['post_id'])
    page = generic.paginate_queryset(queryset)

    if page is not None:
        serializer = generic.get_serializer(page, many=True)
        return generic.get_paginated_response(serializer.data)

    serializer = generic.get_serializer(queryset, many=True)
    return serializer.data