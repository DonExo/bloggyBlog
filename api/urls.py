from django.urls import path, include
from .views import UserDetailView, TopicList, TopicDetail, ArticleViewSet

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


router = DefaultRouter()
router.register(r'', ArticleViewSet, 'article')

urlpatterns = [
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),

    path('topics/', TopicList.as_view(), name='topic-list'),
    path('topics/<int:pk>/', TopicDetail.as_view(), name='topic-detail'),

    path('articles/', include(router.urls)),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]