from django.urls import path

from . import views

app_name = 'mail'
urlpatterns = [
    path('/', views.MailView.as_view(), name='main'),
]
