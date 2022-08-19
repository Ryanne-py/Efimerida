from django.http import JsonResponse
from .serializers import RubricSerializer, PostSerializer
import post.services as services

def api_rubric(requests):
    if requests.method == "GET":
        rubric = services.get_rubric()
        serializer = RubricSerializer(rubric, many=True)
        return JsonResponse(serializer.data, safe=False)


def api_post(requests):
    if requests.method == "GET":
        post = services.get_post()
        serializer = PostSerializer(post, many=True)
        return JsonResponse(serializer.data, safe=False)