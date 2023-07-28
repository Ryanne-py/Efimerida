from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'user_image', 'user_info', 'is_active')
        read_only_fields = ('id', 'email', 'is_active')
