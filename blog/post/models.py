from django.db import models
from django.core import validators
from django.conf import settings
from django.utils import timezone


class Post(models.Model):
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
        blank=True, null=True
        )
    post_rubric = models.ForeignKey(
        'Rubric', null=True,
        on_delete=models.PROTECT,
        verbose_name='Rubric'
        )

    def __str__(self):
        return self.post_title

    class Meta:
        verbose_name_plural = 'Posts'
        verbose_name = 'Post'
        ordering = ['post_edit_date']


class Rubric(models.Model):
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

