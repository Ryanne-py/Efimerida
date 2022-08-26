from django.utils import timezone
from .serializers import RubricSerializer, PostSerializer, PostEditSerializer
import post.services as services
from rest_framework import generics, permissions


class PostListCreate(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return services.get_post()


class PostEdit(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostEditSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return services.get_post()

    def perform_update(self, serializer):
        serializer.instance.post_edit_date = timezone.now()
        serializer.save()
        services.update_post_edit_date(serializer)


class RubricListCreate(generics.ListCreateAPIView):
    serializer_class = RubricSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return services.get_rubric()