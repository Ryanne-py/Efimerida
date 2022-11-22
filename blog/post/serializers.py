from rest_framework import serializers
from .models import Rubric, Post, Comment, Tag
import user.serializers as user


class CommentSerializer(serializers.ModelSerializer):
    comment_author = user.CustomUserSerializer()

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('id', 'comment_created_date', 'comment_author')


class CommentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('id', 'comment_created_date', 'comment_author')


class RubricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rubric
        fields = '__all__'
        read_only_fields = ('id',)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
        read_only_fields = ('id',)


class PostSerializer(serializers.ModelSerializer):
    post_rubric = RubricSerializer()
    post_author = user.CustomUserSerializer()

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('id', 'post_created_date', 'post_edit_date', 'post_likes', 'post_views', 'post_author')


class PostCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('id', 'post_created_date', 'post_edit_date', 'post_likes', 'post_views', 'post_author')