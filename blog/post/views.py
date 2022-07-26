from django.shortcuts import render
import post.services


def post_list(request):
    context = post.services.get_post_list()
    return render(request, 'post/post_list.html', context)

def post_rubric(request):pass