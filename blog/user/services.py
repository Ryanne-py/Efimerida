from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.db import IntegrityError
from .models import CustomUser
from rest_framework.exceptions import ParseError


class UserServices:

    @staticmethod
    def registration(request):
        try:
            data = JSONParser().parse(request)
            user = CustomUser.objects.create_user(
                username=data['username'],
                email=data['email'],
                password=data['password'])
            user.save()
            token = Token.objects.create(user=user)

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
            return JsonResponse({'token': str(token[0])}, status=201)

    @staticmethod
    def get_user_list():
        return CustomUser.objects.all()
