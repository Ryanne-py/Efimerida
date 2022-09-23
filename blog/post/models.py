from django.db import models
from django.core import validators
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    email = models.EmailField(
        _('email address'),
        unique=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name_plural = 'Users'
        verbose_name = 'User'
        ordering = ['email']


class Post(models.Model):
    """A blog post."""
    post_title = models.CharField(
        max_length=100,
        validators=[validators.MinLengthValidator(2)],
        error_messages={'min_length': 'Post title must be longer than two characters'}
        )
    post_image = models.ImageField(
        null=True,
        blank=True,
        upload_to='post_image/',
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
        on_delete=models.PROTECT,
        verbose_name='Rubric'
        )
    post_views = models.IntegerField(default=0)
    post_likes = models.IntegerField(default=0)
    post_tags = models.ManyToManyField('Tag')

    def __str__(self):
        return self.post_title

    class Meta:
        verbose_name_plural = 'Posts'
        verbose_name = 'Post'
        ordering = ['post_edit_date']


class Rubric(models.Model):
    """Rubric for the post."""
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
    """Tag for the post."""
    tag_name = models.CharField(max_length=25)

    def __str__(self):
        return self.tag_name

    class Meta:
        verbose_name_plural = "Tags"
        verbose_name = "Tag"
        ordering = ['tag_name']


class Comment(models.Model):
    """Comments for the post."""
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