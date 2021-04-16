from django.urls import path, include

from . import views

app_name = 'account'
urlpatterns = [
    path('/', views.AccountView.as_view(), name='main'),
    path('create/', views.UserCreateView.as_view(), name='create'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('group/', views.GroupView.as_view(), name='group'),
    path('group/join/', views.GroupJoinView.as_view(), name='join-group'),
    path('group/create/', views.GroupCreateView.as_view(), name='create-group'),
    path('profile/avatar/',views.AvatarChangeView.as_view(),name='change-avatar'),
    path('homepage/<int:user_id>/', views.HomePageView.as_view(),name='homepage'),
]
