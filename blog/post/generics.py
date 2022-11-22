from rest_framework import mixins, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .services import PostRecommendationServices,  PostSerializer
from .dataclasses import Filters


class PostListWithFilterAPIView(mixins.CreateModelMixin,
                                GenericAPIView):
    """
    Concrete view for listing a queryset with filters that was give in request
    """

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        try:
            filters = Filters(**request.data)
        except ValueError as error:
            return Response({"detail": f"{error.args[0][0].exc}"}, status=status.HTTP_400_BAD_REQUEST)

        queryset_posts = PostRecommendationServices.get_post_by_filter(filters)
        serializer = PostSerializer(queryset_posts, many=True)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, headers=headers)

    def perform_create(self, serializer):
        serializer.save()