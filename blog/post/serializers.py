from rest_framework import serializers
from .models import Rubric, Post, Comment, Tag


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'post_title', 'post_text', 'post_rubric', 'post_tags', 'post_author', 'post_created_date', 'post_edit_date', 'post_likes', 'post_views', 'post_image')
        read_only_fields = ('id', 'post_created_date', 'post_edit_date', 'post_likes', 'post_views')


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('id', 'comment_created_date', 'comment_post', 'comment_author', 'comment_text')
        read_only_fields = ('comment_created_date', )


class RubricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rubric
        fields = ('id', 'rubric_name')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'tag_name')