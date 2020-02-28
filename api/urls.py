from django.urls import path, include
from .views import UserDetailView, TopicViewList, TopicViewDetail, ArticleViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', ArticleViewSet, 'article')

urlpatterns = [
    path('users/<int:pk>/', UserDetailView.as_view()),
    path('topics/', TopicViewList.as_view()),
    path('topics/<int:pk>/', TopicViewDetail.as_view(), name='topic-detail'),
    path('articles/', include(router.urls))
]