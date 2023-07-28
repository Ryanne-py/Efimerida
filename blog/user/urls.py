from django.urls import path
from . import views

urlpatterns = [
    path('registration/', views.registration),
    path('authentication/', views.authentication),
    path('activate/<str:uidb64>/<str:token>/', views.activate, name='activate'),
    # path('check_activate', views.check_activate),
    path('subscribe/<int:pk>/', views.UserSubscribe.as_view()),
    path('get_subscribe/', views.UserSubscribeList.as_view()),

    path('list/', views.UserList.as_view()),
    path('detail/<int:pk>/', views.UserDetail.as_view()),

    path('bookmarks/<int:post_id>/', views.BookmarksList.as_view())
]
