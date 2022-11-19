from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core import validators
from django.db import models
from django.utils import timezone
from .managers import CustomUserManager


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


class Post(models.Model):
    """
    Models for post in blog.
    Title, author, text and rubric  are required. Other fields are optional.
    """

    post_title = models.CharField(
        max_length=100,
        validators=[validators.MinLengthValidator(2)],
        error_messages={'min_length': 'Post title must be longer than two characters'}
        )
    post_author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
        )
    post_text = models.TextField(
        validators=[validators.MinLengthValidator(10)],
        error_messages={'min_length': 'Post content must be longer than 10 characters'}
        )
    post_created_date = models.DateTimeField(
        default=timezone.now
        )
    post_edit_date = models.DateTimeField(
        blank=True, null=True,
        default=timezone.now
        )
    post_rubric = models.ForeignKey(
        'Rubric', null=True,
        on_delete=models.SET_NULL,
        verbose_name='Rubric',
        )
    post_image = models.ImageField(
        null=True,
        blank=True,
        upload_to='post_image/',
        )
    post_likes = models.ManyToManyField(
        'CustomUser',
        blank=True,
        related_name='post_likes'
    )
    post_views = models.IntegerField(default=0)
    post_tags = models.ManyToManyField('Tag', blank=True)

    def __str__(self):
        return self.post_title

    class Meta:
        verbose_name_plural = 'Posts'
        verbose_name = 'Post'
        ordering = ['post_edit_date']


class Rubric(models.Model):

    """
    Model rubric for the post in blog.
    """

    rubric_name = models.CharField(
        max_length=25,
        db_index=True
        )

    def __str__(self):
        return self.rubric_name

    class Meta:
        verbose_name_plural = "Rubrics"
        verbose_name = "Rubric"
        ordering = ['rubric_name']


class Tag(models.Model):
    """
    Model tag for the post in blog.
    """
    tag_name = models.CharField(max_length=25)

    def __str__(self):
        return self.tag_name

    class Meta:
        verbose_name_plural = "Tags"
        verbose_name = "Tag"
        ordering = ['tag_name']


class Comment(models.Model):
    """
    Models comment for the post in blog.
    """
    comment_text = models.TextField(
        validators=[validators.MaxLengthValidator(1000)],
        error_messages={'max_length': "The comment cannot be longer than 1000 characters"}
    )
    comment_author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
        )
    comment_post = models.ForeignKey(
        'Post',
        on_delete=models.CASCADE
    )
    comment_created_date = models.DateTimeField(
        default=timezone.now
    )

    def __str__(self):
        return f'Comment in the post {self.comment_post.post_title}'

    class Meta:
        verbose_name_plural = "Comments"
        verbose_name = "Comment"
        ordering = ['-comment_created_date']