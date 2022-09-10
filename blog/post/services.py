from django.utils import timezone
from .models import Post, Rubric, Comment
from .serializers import PostSerializer, CommentSerializer


def get_post_detail(pk=None):
    post = Post.objects.prefetch_related("post_tags").select_related('post_rubric').get(pk=pk)
    comments = Comment.objects.filter(comment_post=pk)
    serializer_post = PostSerializer(post, many=False)
    serializer_comment = CommentSerializer(comments, many=True)
    return {'post': serializer_post.data, 'comment': serializer_comment.data}


def update_post_edit_date(serializer):
    serializer.instance.post_edit_date = timezone.now()
    serializer.save()


def get_rubric():
    rubrics = Rubric.objects.all()
    return rubrics


def get_comment():
    comment = Comment.objects.all()
    return comment


def get_post_list(serializer: bool):
    posts = Post.objects.select_related('post_rubric').prefetch_related("post_tags").all().filter(
        post_created_date__lte=timezone.now()).order_by('post_created_date')
    if serializer:
        posts = PostSerializer(posts, many=True)
    return posts


