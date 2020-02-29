from rest_framework import serializers
from rest_framework import fields

from backend.models import User, Article, Topic


# USER-related serializers
class UserArticleSerializer(serializers.ModelSerializer):
    topic = serializers.CharField()

    class Meta:
        model = Article
        fields = ('title', 'text', 'topic')

    def get_topic(self, article):
        return article.topic


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    posts = fields.SerializerMethodField()
    post_count = fields.SerializerMethodField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'post_count', 'posts')

    def get_posts(self, user):
        return UserArticleSerializer(user.articles.all(), many=True).data

    def get_post_count(self, user):
        return user.articles.all().count()


# ARTICLE-related serializers
class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(view_name='user-detail', read_only=True)
    created = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ('title', 'text', 'topic', 'status', 'user', 'created')
        extra_kwargs = {
            'status': {'read_only': True}
        }

    def __init__(self, *args, **kwargs):
        super(ArticleSerializer, self).__init__(*args, **kwargs)
        self.request = self.context.get('request', None)
        self.user = self.request.user

    def get_created(self, article):
        return article.created.strftime("%Y-%d-%m %H:%M")

    def validate_title(self, title):
        exists = Article.objects.filter(title=title).exists()
        if exists:
            raise serializers.ValidationError("Article with given title already exists!")
        return title

    def create(self, validated_data):
        validated_data['user'] = self.user
        post = Article.objects.create(**validated_data)
        return post


# TOPIC-related Serializers
class TopicArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('title', 'text', 'status')


class TopicDetailSerializer(serializers.HyperlinkedModelSerializer):
    articles_count = serializers.SerializerMethodField()
    articles = serializers.SerializerMethodField()
    url = serializers.HyperlinkedIdentityField(view_name='topic-detail', read_only=True)

    class Meta:
        model = Topic
        fields = ('title', 'url', 'articles_count', 'articles')

    def get_articles_count(self, topic):
        return topic.articles.all().count()

    def get_articles(self, topic):
        return TopicArticleSerializer(topic.articles.all(), many=True).data


class TopicListSerializer(serializers.HyperlinkedModelSerializer):
    articles_count = serializers.SerializerMethodField()
    url = serializers.HyperlinkedIdentityField(view_name='topic-detail', read_only=True)

    class Meta:
        model = Topic
        fields = ('title', 'url', 'articles_count')

    def get_articles_count(self, topic):
        return topic.articles.all().count()

