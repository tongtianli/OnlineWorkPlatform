from django.urls import path

from . import views

app_name = 'kbase'
urlpatterns = [
    path('', views.KBaseView.as_view(), name='main'),
    path('article-detail/<int:article_id>/', views.ArticleView.as_view(), name='article-detail'),
    path('article-create/', views.ArticleCreateView.as_view(), name='article-create'),
    path('article-delete/<int:article_id>/', views.ArticleDeleteView.as_view(), name='article-delete'),
    path('article-update/<int:article_id>/', views.ArticleUpdateView.as_view(), name='article-update'),
]
