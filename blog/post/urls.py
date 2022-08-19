from django.urls import path, include
from . import views

urlpatterns = [
    path('rubric/', views.api_rubric),
    path('post/', views.api_post),
]