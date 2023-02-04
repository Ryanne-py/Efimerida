from django.db.models import QuerySet, Count, Q
from rest_framework import status
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
    def get_post_by_filter(filters: dict):
        return PostRecommendationServices.get_post_by_filter(filters)

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


class PostRecommendationServices:
    """
    Recommendations services for post
    """

    @staticmethod
    def get_post_by_filter(filters: dict[str, str | None]):
        """
        Post filtering function, generates a list based on the specified filtering conditions.
        filters must be in the format of an instance of the Filters class in      blog/post/dataclasses.py
        """

        model_filters = [
            PostRecommendationServices.get_filter_by_title(filters.post_title),
            PostRecommendationServices.get_filter_by_rubric(filters.post_rubric),
            PostRecommendationServices.get_filter_by_tags(filters.post_tags),
        ]

        model_filters = [filter for filter in model_filters if filter is not None]

        queryset = Post.objects.select_related('post_rubric').prefetch_related("post_tags")\
            .select_related('post_author').prefetch_related("post_likes").filter(
            reduce(
                operator.and_,
                (filter for filter in model_filters)
            )
        )

        PostRecommendationServices.order_by_sorting_mode(filters.sorting_mode)

        return queryset

    @staticmethod
    def _skip_if_field_is_null(funk):
        """
        this decorator skips applying the filtering,
        if the filtering argument is None
        """
        @wraps(funk)
        def wrapper(field, **kwargs):
            if field is None:
                return None
            return funk(field, **kwargs)

        return wrapper

    @_skip_if_field_is_null
    @staticmethod
    def get_filter_by_title(title: str) -> Q:
        """
        Returns an instance of class Q with post_title filtering settings
        """

        return Q(post_title__icontains=title)

    @_skip_if_field_is_null
    @staticmethod
    def get_filter_by_rubric(rubric: str) -> Q:
        """
        Returns an instance of class Q with post_rubric filtering settings
        """

        return Q(post_rubric__rubric_name=rubric)

    @_skip_if_field_is_null
    @staticmethod
    def get_filter_by_tags(tags: list[str]) -> Q:
        """
        Returns an instance of class Q with post_tags filtering settings

        """
        return Q(
            reduce(
                operator.or_,
                (Q(post_tags__tag_name=tag) for tag in tags))
        )

    @_skip_if_field_is_null
    @staticmethod
    def order_by_sorting_mode(sorting_mode: str, **kwargs: dict):
        if 'queryset' not in list(kwargs.keys()):
            return None
        queryset = kwargs['queryset']
        """
        order queryset by sorting mode, if the initial list queryset is not set, they are filtered by all posts
        """
        if sorting_mode == 'recommended':
            return queryset.annotate(Count('post_likes')).order_by('-post_likes__count')
        elif sorting_mode == 'nuw':
            return queryset.order_by('-post_created_date')


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
     Services for Tag model
     """
    @staticmethod
    def get_comment_on_post(generic, pk):
        """
        Returns all comments to the specified post
        """
        queryset = Comment.objects.filter(comment_post__id=pk)
        page = generic.paginate_queryset(queryset)

        if page is not None:
            serializer = generic.get_serializer(page, many=True)
            return generic.get_paginated_response(serializer.data)

        serializer = generic.get_serializer(queryset, many=True)
        return serializer, status.HTTP_200_OK

    @staticmethod
    def get_comment_list():
        """
        returns all comments
        """
        return Comment.objects.select_related('comment_author').select_related('comment_post').all()