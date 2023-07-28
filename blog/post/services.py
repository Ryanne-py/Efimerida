from django.db.models import QuerySet, Count, Q
from rest_framework import status

from .dataclasses import Filters
from .models import *
from .serializers import PostSerializer, CommentSerializer
from functools import wraps
import operator
from functools import reduce
from django.db.models import Q


class PostServices:
    """
    Services for Post model
    """

    @staticmethod
    def add_post_view(instance):
        instance.post_views += 1
        instance.save()
        return instance

    @staticmethod
    def get_post_list():
        return Post.objects.select_related('post_rubric').prefetch_related("post_tags").\
            select_related('post_author').prefetch_related("post_likes").all()

    @staticmethod
    def get_post_detail(pk=None):
        post = Post.objects.prefetch_related("post_tags").select_related('post_rubric').get_object_or_404(pk=pk)
        comments = Comment.objects.filter(comment_post=pk)
        serializer_post = PostSerializer(post, many=False)
        serializer_comment = CommentSerializer(comments, many=True)
        return {'post': serializer_post.data, 'comment': serializer_comment.data}

    @staticmethod
    def update_post_edit_date(serializer):
        serializer.instance.post_edit_date = timezone.now()
        serializer.save()

    @staticmethod
    def get_posts_by_filters(filters):
        """
        Retrieves a list of posts based on the specified filters.
        Filters must be provided as a dictionary with the following keys:
        - "title" (str): Title of the post (optional)
        - "rubric" (str): Rubric of the post (optional)
        - "tags" (list[str]): Tags associated with the post (optional)
        - "author" (str): Username of the post author (optional)
        - "sorting_mode" (str): Sorting mode for the results (optional)

        Returns a queryset of Post objects.
        """
        queryset = Post.objects.select_related('post_rubric', 'post_author') \
            .prefetch_related('post_tags', 'post_likes').filter(is_finished=True)

        if filters["post_title"] is not None:
            queryset = queryset.filter(post_title__icontains=filters["post_title"])

        if filters["post_rubric"] is not None:
            queryset = queryset.filter(post_rubric__rubric_name=filters["post_rubric"])

        if filters["post_tags"] is not None:
            queryset = queryset.filter(post_tags__tag_name__in=filters["post_tags"]).distinct()

        if filters["post_author"] is not None:
            queryset = queryset.filter(post_author__username=filters["post_author"])

        if filters["sorting_mode"] is not None:
            sorting_mode = filters["sorting_mode"]

            if sorting_mode == "recommended":
                queryset = queryset.annotate(like_count=Count('post_likes')).order_by('-like_count')
            elif sorting_mode == "new":
                queryset = queryset.order_by('-post_created_date')

        return queryset

    @staticmethod
    def add_post_to_draft(post_pk):
        try:
            post = Post.objects.get(id=post_pk)
            post.is_finished = False
            post.save()
            return {'detail': 'post successfully added to draft'}, status.HTTP_200_OK
        except Post.DoesNotExist:
            return {'detail': 'post with such an index does not exist'}, status.HTTP_404_NOT_FOUND

    @staticmethod
    def dell_post_from_draft(post_pk):
        try:
            post = Post.objects.get(id=post_pk)
            post.is_finished = True
            post.save()
            return {'detail': 'post successfully delete from draft'}, status.HTTP_200_OK
        except Post.DoesNotExist:
            return {'detail': 'post with such an index does not exist'}, status.HTTP_404_NOT_FOUND

    @staticmethod
    def like_post(user, post_pk):
        try:
            if not PostServices.is_user_liked_post(user, post_pk):
                Post.objects.get(id=post_pk).post_likes.add(user)
                return {'detail': 'like from user added successfully'}, status.HTTP_200_OK
            else:
                return {'detail': 'like from this user is not added, it is already set before'}, status.HTTP_404_NOT_FOUND
        except Post.DoesNotExist:
            return {'detail': 'post with such an index does not exist'}, status.HTTP_404_NOT_FOUND

    @staticmethod
    def cancel_like(user, post_pk):
        try:
            if PostServices.is_user_liked_post(user, post_pk):
                Post.objects.get(id=post_pk).post_likes.remove(user)
                return {'detail': 'like from this user has been successfully canceled'}, status.HTTP_200_OK
            else:
                return {'detail': 'it was not possible to unlike this user because it was not set before'},\
                    status.HTTP_404_NOT_FOUND
        except Post.DoesNotExist:
            return {'detail': 'post with such an index does not exist'}, status.HTTP_404_NOT_FOUND

    @staticmethod
    def is_user_liked_post(user, post_pk):
        if user in Post.objects.get(id=post_pk).post_likes.all():
            return True
        else:
            return False


class TagServices:
    """
    Services for Tag model
    """
    @staticmethod
    def get_tags():
        return Tag.objects.all()


class RubricServices:
    """
     Services for Tag model
    """
    @staticmethod
    def get_rubric():
        return Rubric.objects.all()


class CommentServices:
    """
    Services for Comment model
    """
    @staticmethod
    def get_comment_on_post(pk):
        """
        Returns all comments to the specified post
        """
        queryset = Comment.objects.filter(comment_post__id=pk)

        return queryset

    @staticmethod
    def get_comment_list():
        """
        returns all comments
        """
        return Comment.objects.select_related('comment_author').select_related('comment_post').all()