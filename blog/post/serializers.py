from rest_framework import serializers
from .models import Rubric, Post


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'post_title', 'post_author', 'post_text', 'post_created_date', 'post_edit_date', 'post_rubric', 'post_likes', 'post_views', 'post_tags')
        read_only_fields = ['id', 'post_created_date', 'post_edit_date', 'post_likes', 'post_views']


class PostEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'post_title', 'post_text', 'post_rubric', 'post_tags']
        read_only_fields = ['id', 'post_author', 'post_created_date', 'post_edit_date', 'post_likes', 'post_views']


class RubricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rubric
        fields = ('id', 'rubric_name')