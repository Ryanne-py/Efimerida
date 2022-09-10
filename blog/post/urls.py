from django.urls import path
from . import views


urlpatterns = [
    path('rubric/', views.RubricApiList.as_view()),
    path('comment/', views.CommentViewSet.as_view({'put': 'create'})),
    path('comment/<int:pk>/', views.CommentViewSet.as_view({'delete': 'destroy', 'get': 'retrieve'})),
    path('post/', views.PostViewSet.as_view({'get': 'list', 'put': 'create'})),
    path('post/<int:pk>/', views.PostViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}))
]

