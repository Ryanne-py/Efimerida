from .serializers import RubricSerializer, PostSerializer
import post.services as services
from rest_framework import generics


class PostListCreate(generics.ListCreateAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        return services.get_post()


class RubricListCreate(generics.ListCreateAPIView):
    serializer_class = RubricSerializer

    def get_queryset(self):
        return services.get_rubric()