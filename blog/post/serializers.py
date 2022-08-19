from rest_framework import serializers
from .models import Rubric, Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'post_title', 'post_author', 'post_text', 'post_created_date', 'post_edit_date', 'post_rubric')


class RubricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rubric
        fields = ('id', 'rubric_name')