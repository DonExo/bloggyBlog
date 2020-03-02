import json
from django.db.models import Q
from django.http import Http404

from rest_framework.response import Response
from rest_framework import status, views, generics, viewsets, permissions

from backend.models import User, Topic, Article
from .serializers import UserSerializer, TopicListSerializer, TopicDetailSerializer, ArticleSerializer
from .permissions import IsOwnerOrAdmin

# Below you can find different approaches on creating the views for the API`


class UserDetailView(views.APIView):
    """
    Retrieves a User and his Articles
    """
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TopicList(generics.ListCreateAPIView):
    """
    Retrieves all Topics. Only admin users can submit new topic.
    """
    queryset = Topic.objects.all()
    serializer_class = TopicListSerializer

    def get(self, request, *args, **kwargs):
        context = {'request': request}
        serializer = TopicListSerializer(self.get_queryset(), many=True, context=context)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        if request.user.is_staff:
            serializer = TopicListSerializer(data=request.data)
            if serializer.is_valid():
                return self.create(request, *args, **kwargs)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            response = {"Error": "You don't have access to do this action"}
            return Response(response, status=status.HTTP_403_FORBIDDEN)


class TopicDetail(generics.RetrieveAPIView):
    """
    Retrieves details about a Topic and its articles
    """
    queryset = Topic.objects.all()
    serializer_class = TopicDetailSerializer

    def get_object(self, pk):
        try:
            return Topic.objects.get(pk=pk)
        except Topic.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        context = {'request': request}
        topic = self.get_object(pk)
        serializer = TopicDetailSerializer(topic, context=context)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ArticleViewSet(viewsets.ModelViewSet):
    """
    Displays a list of all articles or CRUD a single article
    """
    serializer_class = ArticleSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        queryset = Article.objects.all()
        search = self.request.GET.get('search')
        if search is not None:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(text__icontains=search)
            ).distinct()
        return queryset

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [permissions.AllowAny]
        elif self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            permission_classes = [IsOwnerOrAdmin]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]