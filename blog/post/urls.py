from django.urls import path
from . import views


urlpatterns = [
    path('registration/', views.registration),
    path('authentication/', views.authentication),

    path('user_list/', views.UserList.as_view()),
    path('user_detail/<int:pk>/', views.UserDetail.as_view()),

    path('rubric_list/', views.RubricList.as_view()),
    path('rubric_detail/<int:pk>/', views.RubricDetail.as_view()),

    path('tag_list/', views.TagList.as_view()),
    path('tag_detail/', views.TagDetail.as_view()),

    path('comment_on_post/<int:pk>/', views.CommentList.as_view()),
    path('comment_detail/<int:pk>/', views.CommentDetail.as_view()),

    path('post_list/', views.PostList.as_view()),
    path('post_detail/<int:pk>/', views.PostDetail.as_view()),
    path('like_post/<int:pk>/', views.PostLike.as_view()),

    path('post_by_filter/', views.PostListByFilter.as_view())
]

