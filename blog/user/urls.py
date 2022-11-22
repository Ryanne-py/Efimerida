from django.urls import path
from . import views

urlpatterns = [
    path('registration/', views.registration),
    path('authentication/', views.authentication),

    path('list/', views.UserList.as_view()),
    path('detail/<int:pk>/', views.UserDetail.as_view()),
]
