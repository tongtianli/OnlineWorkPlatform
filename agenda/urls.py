from django.urls import path

from . import views

app_name = 'agenda'
urlpatterns = [
    path('', views.AgendaView.as_view(), name='main'),
    path('create/', views.AgendaCreateView.as_view(), name='create'),
    path('create-group/', views.GroupAgendaCreateView.as_view(), name='create-group'),
    path('detail/<int:agenda_id>/', views.AgendaDetialView.as_view(), name='detail'),
    path('delete/', views.deleteAgenda, name='delete'),
    path('create-group/conflict/', views.ConflictView.as_view(), name='conflict'),
]
