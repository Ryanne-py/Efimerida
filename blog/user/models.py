from typing import List
from django.db import models
from .managers import CustomUserManager
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core import validators

from post.models import Post


def user_directory_path(instance, filepath):
    return 'user_image/{0}'.format(instance.email + '_avatar.jpg')


class CustomUser(AbstractUser):
    """
    Model for user profile in blog.
    Username, email and password are required. Other fields are optional.
    """
    username_validator = UnicodeUsernameValidator()
    email = models.EmailField(
        unique=True,
        error_messages={
            "unique": "A user with that email already exists.",
        },
        validators=[validators.EmailValidator()]
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
        validators=[username_validator],
        error_messages={
            "unique": "A user with that username already exists.",
        },
    )
    user_bookmarks = models.ManyToManyField(Post, blank=True)
    user_info = models.CharField(
        max_length=500,
        null=True,
        blank=True,
        help_text="Not required. 500 characters or fewer. Letters, digits and @/./+/-/_ only.",
    )
    user_image = models.ImageField(
        null=True,
        blank=True,
        upload_to=user_directory_path,
        )
    is_active = models.BooleanField(
        default=False,
    )
    user_subscriptions = models.ManyToManyField('CustomUser', blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name_plural = 'Users'
        verbose_name = 'User'
        ordering = ['email']


