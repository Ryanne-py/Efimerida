from django.urls import path
from . import views

urlpatterns = [
    path('rubric/', views.RubricListCreate.as_view()),
    path('post/', views.PostListCreate.as_view()),
]