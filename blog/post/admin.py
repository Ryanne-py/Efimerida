from django.contrib import admin
from .models import Post, Rubric, Tag, Comment

admin.site.register(Post)
admin.site.register(Rubric)
admin.site.register(Tag)
admin.site.register(Comment)