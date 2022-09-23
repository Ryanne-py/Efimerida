from django.urls import path
from . import views


urlpatterns = [
    path('registration/', views.registration),
    path('authentication/', views.authentication),

    path('rubric_list/', views.RubricList.as_view()),
    path('rubric_detail/<int:pk>/', views.RubricDetail.as_view()),

    path('comment_on_post/<int:post_id>/', views.CommentList.as_view()),
    path('comment_detail/<int:pk>/', views.CommentDetail.as_view()),

    path('post_list/', views.PostList.as_view()),
    path('post_detail/<int:pk>/', views.PostDetail.as_view()),
]

