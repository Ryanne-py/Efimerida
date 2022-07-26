from django.utils import timezone

from post.models import Post, Rubric


def get_post_list() -> dict:
    rubrics = Rubric.objects.all()
    posts = Post.objects.all().filter(
        post_created_date__lte=timezone.now()).order_by('post_created_date')
    context = {'posts': posts, 'rubrics': rubrics}
    return context


