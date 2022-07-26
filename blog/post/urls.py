from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('<str:rubric>/', views.post_rubric, name='post_rubric'),
]