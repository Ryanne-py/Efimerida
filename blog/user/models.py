from django.db import models
from .managers import CustomUserManager
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator


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
        }
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
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name_plural = 'Users'
        verbose_name = 'User'
        ordering = ['email']


