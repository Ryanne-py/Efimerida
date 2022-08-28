from django.utils import timezone
from post.models import Post, Rubric


def get_post() -> dict:
    posts = Post.objects.all().filter(
        post_created_date__lte=timezone.now()).order_by('post_created_date')
    return posts


def update_post_edit_date(serializer):
    serializer.instance.post_edit_date = timezone.now()
    serializer.save()


def get_rubric() -> dict:
    rubrics = Rubric.objects.all()
    return rubrics


def get_post_list() -> dict:
    rubrics = Rubric.objects.all()
    posts = Post.objects.all().filter(
        post_created_date__lte=timezone.now()).order_by('post_created_date')
    context = {'posts': posts, 'rubrics': rubrics}
    return context


