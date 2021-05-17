from django.urls import path

from . import views

app_name = 'mail'
urlpatterns = [
    path('/', views.MailView.as_view(), name='main'),
    path('message/delete/<int:message_id>', views.MessageDeleteView.as_view(), name='delete-message'),
]
