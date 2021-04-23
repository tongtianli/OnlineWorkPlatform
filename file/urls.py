from django.urls import path

from . import views

app_name = 'file'

urlpatterns = [
    path('', views.FileView.as_view(), name='main'),
    path('<int:path_id>/', views.FolderView.as_view(), name='folder'),
    path('download/<int:file_id>/', views.DownloadView.as_view(), name='download'),
    path('upload/<int:path_id>/', views.UploadView.as_view(), name='upload'),
    path('new/<int:path_id>/',views.NewFolderView.as_view(),name='new-folder'),
    path('delete/',views.FileDeleteView.as_view(),name='delete'),
]
