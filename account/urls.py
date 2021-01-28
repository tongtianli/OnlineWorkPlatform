from django.urls import path

from . import views

app_name = 'account'
urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]
