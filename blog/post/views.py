from .serializers import RubricSerializer, PostSerializer, CommentSerializer
import post.services as services
from rest_framework import generics, permissions, viewsets
from rest_framework.response import Response


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = services.get_post_list(serializer=False)
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, pk):
        return Response(services.get_post_detail(pk))

    def list(self, request, *args, **kwargs):
        return Response({'post': services.get_post_list(serializer=True).data})


class RubricApiList(generics.ListCreateAPIView):
    serializer_class = RubricSerializer
    queryset = services.get_rubric()
    permission_classes = [permissions.IsAuthenticated]


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = services.get_comment()
    permission_classes = [permissions.IsAuthenticated]