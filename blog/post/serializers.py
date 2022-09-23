from rest_framework import serializers
from .models import Rubric, Post, Comment, Tag, CustomUser


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email')


class CommentSerializer(serializers.ModelSerializer):
    comment_author = CustomUserSerializer()

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('comment_created_date', 'comment_author')


class RubricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rubric
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    post_rubric = RubricSerializer()
    post_author = CustomUserSerializer()

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('id', 'post_created_date', 'post_edit_date', 'post_likes', 'post_views', 'post_author')
