import smtplib
from email.mime.text import MIMEText

from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q, F, QuerySet
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.db import IntegrityError
from .models import CustomUser
from rest_framework.exceptions import ParseError
from config import settings

from post.models import Post


class UserServices:

    @staticmethod
    def del_bookmarks(user, post_id) -> JsonResponse:
        try:
            user = CustomUser.objects.get(id=user.id)
            post = Post.objects.get(id=post_id)
            user.user_bookmarks.remove(post)
            user.save()
            return JsonResponse({'detail': 'Bookmark delete successfully'}, status=200)
        except ValueError:
            return JsonResponse({'detail': f'Post with id {post_id} not in bookmark'}, status=400)

    @staticmethod
    def add_bookmarks(user, post_id) -> JsonResponse:
        try:
            user = CustomUser.objects.get(id=user.id)
            post = Post.objects.get(id=post_id)
            user.user_bookmarks.add(post)
            user.save()
            return JsonResponse({'detail': 'Bookmark added successfully'}, status=200)
        except Post.DoesNotExist:
            return JsonResponse({'detail': f'Post with id {post_id} not exist'}, status=400)

    @staticmethod
    def get_bookmarks(user):
        return CustomUser.objects.get(id=user.id).user_bookmarks.all()

    @staticmethod
    def check_activate(user):
        return CustomUser.objects.get(id=user.id).is_active

    @staticmethod
    def get_subscribe(user):
        try:
            return CustomUser.objects.get(id=user.id).user_subscriptions.all()
        except CustomUser.DoesNotExist:
            return {'detail': 'user with such an index does not exist'}

    @staticmethod
    def get_subscriber(user):
        try:
            return CustomUser.objects.filter(user_subscriptions=user).count()
        except CustomUser.DoesNotExist:
            return {'detail': 'user with such an index does not exist'}

    @staticmethod
    def send_mail_activate(mail_subject, message, email):
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()

        try:
            server.login(settings.EMAIL_ACCOUNT, settings.EMAIL_PASSWORD)
            msg = MIMEText(message, 'html')
            msg["Subject"] = mail_subject
            server.sendmail(settings.EMAIL_ACCOUNT, email, msg.as_string())

            return "The message was sent successfully!"
        except Exception as _ex:
            return f"{_ex}\nCheck your login or password please!"
    @staticmethod
    def is_user_in_subscriptions(user, user_pk):
        author = CustomUser.objects.get(id=user_pk)
        if author in CustomUser.objects.get(id=user.id).user_subscriptions.all():
            return True
        else:
            return False

    @staticmethod
    def subscribe(user, user_pk):
        try:
            if not UserServices.is_user_in_subscriptions(user, user_pk):
                author = CustomUser.objects.get(id=user_pk)
                user.user_subscriptions.add(author)
                return {'detail': 'subscribe from user added successfully'}, status.HTTP_200_OK
            else:
                return {
                    'detail': 'subscribe from this user is not added, it is already set before'}, status.HTTP_404_NOT_FOUND
        except CustomUser.DoesNotExist:
            return {'detail': 'user with such an index does not exist'}, status.HTTP_404_NOT_FOUND

    @staticmethod
    def unsubscribe(user, user_pk):
        try:
            if not UserServices.is_user_in_subscriptions(user, user_pk):
                CustomUser.objects.get(id=user_pk).user_subscriptions.remove(user)
                return {'detail': 'subscribe from this user has been successfully canceled'}, status.HTTP_200_OK
            else:
                return {'detail': 'it was not possible to unsubscribe this user because it was not set before'}, \
                    status.HTTP_404_NOT_FOUND
        except CustomUser.DoesNotExist:
            return {'detail': 'user with such an index does not exist'}, status.HTTP_404_NOT_FOUND

    @staticmethod
    def registration(request):
        try:
            data = JSONParser().parse(request)
            user = CustomUser.objects.create_user(
                username=data['username'],
                email=data['email'],
                password=data['password']
            )
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account'
            token = Token.objects.create(user=user)
            message = render_to_string('activation_email.html', {
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': str(token),
                'name': data['username']
            })
            UserServices.send_mail_activate(mail_subject, message, user.email)

            return JsonResponse({'token': str(token), 'detail': 'Registration completed successfully'}, status=201)

        except IntegrityError as i:
            if i.args[0] == 'UNIQUE constraint failed: post_customuser.email':
                return JsonResponse(
                    {'detail': 'A user with that email already exists.'}, status=400)
            else:
                return JsonResponse(
                    {'detail': 'A user with that username already exists.'}, status=400)

        except ParseError:
            return JsonResponse(
                {'detail': 'you need to send data for registration'}, status=400)

        except KeyError:
            return JsonResponse(
                {'detail': 'you need to fill in all fields for registration (username, email, password)'}, status=400)

    @staticmethod
    def authentication(request):
        data = JSONParser().parse(request)
        if list(data.keys()) != ['email', 'password']:
            return JsonResponse(
                {'detail': 'you need to fill in all fields for authentication (email, password)'}, status=400)

        user = authenticate(request, email=data['email'],
                            password=data['password'])
        if user is None:
            return JsonResponse(
                {'detail': 'unable to login. check email and password'}, status=400)
        else:
            token = Token.objects.get_or_create(user=user)
            id = user.id
            return JsonResponse(
                {'token': str(token[0]),
                 'id': int(user.id),
                 'username': str(user.username),
                 'user_image': str(user.user_image)
                 }, status=201)


    @staticmethod
    def get_user_list():
        return CustomUser.objects.all()
