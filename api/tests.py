from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from backend.models import User, Article, Topic


class TestApiUser(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='username', email='email@gom.com', password='password')
        cls.topic = Topic.objects.create(title='Topic title 1')
        Article.objects.bulk_create([
            Article(title="Article title 1", text="Article text 1", user=cls.user, topic=cls.topic),
            Article(title="Article title 2", text="Article text 2", user=cls.user, topic=cls.topic),
            Article(title="Article title 3", text="Article text 3", user=cls.user, topic=cls.topic)
        ])

    @staticmethod
    def user_detail_endpoint(user_pk):
        return reverse('user-detail', kwargs={'pk': user_pk})

    def test_get_request_on_user_endpoint(self):
        response = self.client.get(self.user_detail_endpoint(self.user.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        items_in_response = ['first_name', 'last_name', 'email', 'post_count', 'posts']
        for item in items_in_response:
            self.assertTrue(item in response.data)

    def test_get_articles_for_user(self):
        response = self.client.get(self.user_detail_endpoint(self.user.pk))
        self.assertEqual(response.data['post_count'], 3)
        expected = [
            {
                'title': 'Article title 1',
                'text': 'Article text 1',
                'topic': 'Topic title 1'
            },
            {
                'title': 'Article title 2',
                'text': 'Article text 2',
                'topic': 'Topic title 1'
            },
            {
                'title': 'Article title 3',
                'text': 'Article text 3',
                'topic': 'Topic title 1'
            }
        ]
        posts = [dict(item) for item in response.data['posts']]
        self.assertListEqual(expected, posts)

    def test_post_put_patch_delete_request_on_user_endpoint(self):
        response = self.client.post(self.user_detail_endpoint(self.user.pk))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.put(self.user_detail_endpoint(self.user.pk))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.patch(self.user_detail_endpoint(self.user.pk))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.delete(self.user_detail_endpoint(self.user.pk))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class TestApiTopic(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='username', email='email@gom.com', password='password')
        cls.topic1 = Topic.objects.create(title="Topic title 1")
        cls.topic2 = Topic.objects.create(title="Topic title 2")
        Article.objects.bulk_create([
            Article(title="Article title 1", text="Article text 1", user=cls.user, topic=cls.topic1),
            Article(title="Article title 2", text="Article text 2", user=cls.user, topic=cls.topic1, status='published'),
            Article(title="Article title 3", text="Article text 3", user=cls.user, topic=cls.topic2),
            Article(title="Article title 4", text="Article text 4", user=cls.user, topic=cls.topic2),
            Article(title="Article title 5", text="Article text 5", user=cls.user, topic=cls.topic2)
        ])

    @staticmethod
    def topic_list_endpoint():
        return reverse('topic-list')

    @staticmethod
    def topic_detail_endpoint(user_pk):
        return reverse('topic-detail', kwargs={'pk': user_pk})

    def test_get_topics(self):
        response = self.client.get(self.topic_list_endpoint())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected = [
            {
                "title": "Topic title 1",
                "url": "http://testserver/api/topics/1/",
                "articles_count": 2
            },
            {
                "title": "Topic title 2",
                "url": "http://testserver/api/topics/2/",
                "articles_count": 3
            }
        ]
        topics = [dict(item) for item in response.data]
        self.assertListEqual(expected, topics)

    def test_get_topic_detail(self):
        response = self.client.get(self.topic_detail_endpoint(self.topic1.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['articles_count'], 2)
        items_in_response = ['title', 'url', 'articles_count', 'articles']
        for item in items_in_response:
            self.assertTrue(item in response.data)

    def test_get_articles_from_topic_details(self):
        response = self.client.get(self.topic_detail_endpoint(self.topic1.pk))
        expected = [
            {
                'title': 'Article title 1',
                'text': 'Article text 1',
                'status': 'draft'
            },
            {
                'title': 'Article title 2',
                'text': 'Article text 2',
                'status': 'published'
            }
        ]
        articles = [dict(article) for article in response.data['articles']]
        self.assertListEqual(expected, articles)

    def test_post_put_patch_delete_request_on_topic_detail_endpoint(self):
        response = self.client.post(self.topic_detail_endpoint(self.topic1.pk))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.put(self.topic_detail_endpoint(self.topic1.pk))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.patch(self.topic_detail_endpoint(self.topic1.pk))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.delete(self.topic_detail_endpoint(self.topic1.pk))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)