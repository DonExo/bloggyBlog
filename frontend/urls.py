from django.urls import path
from .views import index, ArticleListView, ArticleDetailView, ArticleCreateView, ArticleUpdateView

urlpatterns = [
    path('', index, name='index'),

    path('articles/', ArticleListView.as_view(), name='article-list'),
    path('articles/<slug:slug>', ArticleDetailView.as_view(), name='article-detail'),  # DO NOT ADD SLASH !!!!!
    path('articles/create/', ArticleCreateView.as_view(), name='article-create'),
    path('articles/<slug:slug>/edit/', ArticleUpdateView.as_view(), name='article-edit'),

]
