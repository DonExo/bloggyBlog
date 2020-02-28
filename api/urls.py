from django.urls import path, include
from .views import UserDetailView, TopicViewList, TopicViewDetail, ArticleViewSet

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


router = DefaultRouter()
router.register(r'', ArticleViewSet, 'article')

urlpatterns = [
    path('users/<int:pk>/', UserDetailView.as_view()),
    path('topics/', TopicViewList.as_view()),
    path('topics/<int:pk>/', TopicViewDetail.as_view(), name='topic-detail'),
    path('articles/', include(router.urls)),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]