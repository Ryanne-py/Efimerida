from django.urls import path, include
from . import views


urlpatterns = [
    path('rubric_list/', views.RubricList.as_view()),
    path('rubric_detail/<int:pk>/', views.RubricDetail.as_view()),

    path('tag_list/', views.TagList.as_view()),
    path('tag_detail/<int:pk>/', views.TagDetail.as_view()),

    path('comment/<int:pk>/', views.CommentList.as_view()),
    path('comment_detail/<int:pk>/', views.CommentDetail.as_view()),

    path('list/', views.PostList.as_view()),
    path('detail/<int:pk>/', views.PostDetail.as_view()),

    path('like/<int:pk>/', views.PostLike.as_view()),

    path('by_filter/', views.PostListByFilter.as_view()),
    path('by_sub/', views.PostListBySubscription.as_view()),

    path('draft/<int:pk>/', views.PostDraft.as_view()),

]

