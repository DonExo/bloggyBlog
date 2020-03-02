from freezegun import freeze_time

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
        items_in_response = ['first_name', 'last_name', 'email', 'articles_count', 'articles']
        for item in items_in_response:
            self.assertTrue(item in response.data)

    def test_get_articles_for_user(self):
        response = self.client.get(self.user_detail_endpoint(self.user.pk))
        self.assertEqual(response.data['articles_count'], 3)
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
        posts = [dict(item) for item in response.data['articles']]
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
    def topic_detail_endpoint(pk):
        return reverse('topic-detail', kwargs={'pk': pk})

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

    def test_create_topic_with_regular_user(self):
        self.client.force_authenticate(self.user)
        data = {
            "title": "Random title"
        }
        response = self.client.post(self.topic_list_endpoint(), data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_topic_with_admin_user(self):
        user = User.objects.create_superuser(username='admin', password='admins', email='admin@gom.com')
        self.client.force_authenticate(user)
        data = {
            "title": "Random title"
        }
        response = self.client.post(self.topic_list_endpoint(), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_topic_with_admin_user_but_missing_data(self):
        user = User.objects.create_superuser(username='admin', password='admins', email='admin@gom.com')
        self.client.force_authenticate(user)
        response = self.client.post(self.topic_list_endpoint())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('title' in response.data)
        self.assertEqual(["This field is required."], response.json()['title'])

    def test_create_topic_that_already_exists(self):
        user = User.objects.create_superuser(username='admin', password='admins', email='admin@gom.com')
        self.client.force_authenticate(user)
        data = {
            "title": "Topic title 1" # this topic already exists in the setUpTestData()
        }
        response = self.client.post(self.topic_list_endpoint(), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('title' in response.json())
        self.assertEqual(["Topic with given title already exists!"], response.json()['title'])

    def test_get_non_existing_topic(self):
        respose = self.client.get(self.topic_detail_endpoint(9999))
        self.assertEqual(respose.status_code, status.HTTP_404_NOT_FOUND)

@freeze_time("2020-03-01 19:36")
class TestApiArticle(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='username', email='email@gom.com', password='password')
        cls.topic1 = Topic.objects.create(title="Topic title 1")
        cls.topic2 = Topic.objects.create(title="Topic title 2")
        Article.objects.bulk_create([
            Article(title="Article title 1", text="Article text 1", user=cls.user, topic=cls.topic1, status='published'),
            Article(title="Article title 2", text="Article text 2", user=cls.user, topic=cls.topic1),
            Article(title="Article title 3", text="Donald is programming", user=cls.user, topic=cls.topic2),
        ])

    @staticmethod
    def article_list_endpoint():
        return reverse('article-list')

    @staticmethod
    def article_detail_endpoint(pk):
        return reverse('article-detail', kwargs={'pk': pk})

    def test_get_article_detail(self):
        response = self.client.get(self.article_detail_endpoint(1))
        article = {
            "title": "Article title 1",
            "text": "Article text 1",
            "topic": "http://testserver/api/topics/1/",
            "status": "published",
            "user": "http://testserver/api/users/1/",
            "created": "2020-01-03 19:36"
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(article, response.data)
        items_in_response = ['title', 'text', 'topic', 'user', 'status', 'created']
        for item in items_in_response:
            self.assertTrue(item in response.data)

    def test_get_non_existing_article(self):
        response = self.client.get(self.article_detail_endpoint(99999))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_articles(self):
        response = self.client.get(self.article_list_endpoint())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected = [
            {
                "title": "Article title 1",
                "text": "Article text 1",
                "topic": "http://testserver/api/topics/1/",
                "status": "published",
                "user": "http://testserver/api/users/1/",
                "created": "2020-01-03 19:36"
            },
            {
                "title": "Article title 2",
                "text": "Article text 2",
                "topic": "http://testserver/api/topics/1/",
                "status": "draft",
                "user": "http://testserver/api/users/1/",
                "created": "2020-01-03 19:36"

            },
            {
                "title": "Article title 3",
                "text": "Donald is programming",
                "topic": "http://testserver/api/topics/2/",
                "status": "draft",
                "user": "http://testserver/api/users/1/",
                "created": "2020-01-03 19:36"
            }
        ]
        topics = [dict(item) for item in response.data]
        self.assertListEqual(expected, topics)

    def test_search_for_articles(self):
        response = self.client.get(''.join([self.article_list_endpoint(), "?search=unknown"]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

        response = self.client.get(''.join([self.article_list_endpoint(), "?search=donald"]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected = [
            {
                "title": "Article title 3",
                "text": "Donald is programming",
                "topic": "http://testserver/api/topics/2/",
                "status": "draft",
                "user": "http://testserver/api/users/1/",
                "created": "2020-01-03 19:36"
            }
        ]
        self.assertEqual(response.data, expected)

    def test_post_new_article_with_unauthorized_user(self):
        data = {
            "title": "Newly posted article title",
            "text": "Newly posted article text",
            "topic": "http://testserver/api/topics/2/",
        }
        response = self.client.post(self.article_list_endpoint(), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_new_article_with_authorized_user(self):
        self.client.force_authenticate(self.user)
        data = {
            "title": "Newly posted article title",
            "text": "Newly posted article text",
            "topic": "http://testserver/api/topics/2/",
        }
        response = self.client.post(self.article_list_endpoint(), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_new_article_with_authorized_user_missing_data(self):
        self.client.force_authenticate(self.user)
        data = {}
        response = self.client.post(self.article_list_endpoint(), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        required_fields = ['title', 'text', 'topic']
        for field in required_fields:
            self.assertTrue(field in response.data)
            self.assertEqual(['This field is required.'], response.data[field])
        self.assertFalse('not_required_field' in response.data)

    def test_patch_existing_article_with_correct_user(self):
        self.client.force_authenticate(self.user)
        data = {
            "title": "Title changed via PATCH request"
        }
        article_1 = Article.objects.get(pk=1)
        response = self.client.patch(self.article_detail_endpoint(article_1.pk), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        article_1.refresh_from_db()
        self.assertEqual(article_1.title, "Title changed via PATCH request")

    def test_patch_existing_article_with_wrong_user(self):
        new_user = User.objects.create_user(username='username2', email='email2@gom.com', password='password2')
        self.client.force_authenticate(new_user)
        data = {
            "title": "Title changed via PATCH request"
        }
        article_1 = Article.objects.get(pk=1)
        response = self.client.patch(self.article_detail_endpoint(article_1.pk), data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual("You do not have permission to perform this action.", response.data['detail'])
        article_1.refresh_from_db()
        self.assertEqual(article_1.title, "Article title 1")

    def test_put_existing_article_with_correct_user(self):
        self.client.force_authenticate(self.user)
        data = {
            "title": "Title changed via PUT request",
            "text": "Text changed via PUT request",
            "topic": "http://testserver/api/topics/2/"
        }
        article_1 = Article.objects.get(pk=1)
        response = self.client.put(self.article_detail_endpoint(article_1.pk), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        article_1.refresh_from_db()
        self.assertEqual(article_1.title, "Title changed via PUT request")
        self.assertEqual(article_1.text, "Text changed via PUT request")
        self.assertEqual(article_1.topic, self.topic2)

    def test_put_existing_article_with_correct_user_missing_data(self):
        self.client.force_authenticate(self.user)
        data = {
            "title": "Title changed via PUT request",
            "text": "Text changed via PUT request",
            # "topic": "missing topic data on purpose"
        }
        article_1 = Article.objects.get(pk=1)
        response = self.client.put(self.article_detail_endpoint(article_1.pk), data=data)
        self.assertTrue('topic' in response.data)
        self.assertEqual(["This field is required."], response.data['topic'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_existing_article_with_wrong_user(self):
        new_user = User.objects.create_user(username='username2', email='email2@gom.com', password='password2')
        self.client.force_authenticate(new_user)
        data = {
            "title": "Title changed via PUT request",
            "text": "Text changed via PUT request",
            "topic": "Topic changed via PUT request"
        }
        article_1 = Article.objects.get(pk=1)
        response = self.client.put(self.article_detail_endpoint(article_1.pk), data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual("You do not have permission to perform this action.", response.data['detail'])
        article_1.refresh_from_db()
        self.assertEqual(article_1.title, "Article title 1")

    def test_publish_article_with_anonymous_user(self):
        article2 = Article.objects.get(pk=2)
        assert article2.status == "draft"
        response = self.client.get("".join([self.article_detail_endpoint(article2.pk), "publish/"]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual('Authentication credentials were not provided.', response.json()['detail'])

    def test_publish_article_with_non_admin_user(self):
        new_user = User.objects.create_user(username='username2', email='email2@gom.com', password='password2')
        self.client.force_authenticate(new_user)
        article2 = Article.objects.get(pk=2)
        assert article2.status == "draft"
        response = self.client.get("".join([self.article_detail_endpoint(article2.pk), "publish/"]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual('You do not have permission to perform this action.', response.json()['detail'])

    def test_publish_article_with_admin_user(self):
        admin_user = User.objects.create_superuser(username='username2', email='email2@gom.com', password='password2')
        self.client.force_authenticate(admin_user)
        article2 = Article.objects.get(pk=2)
        assert article2.status == "draft"
        response = self.client.get("".join([self.article_detail_endpoint(article2.pk), "publish/"]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual("Article '{}' has been successfully published!".format(article2), response.json()['detail'])
        article2.refresh_from_db()
        self.assertTrue(article2.is_published())


class TestApiAuth(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='username', email='email@gom.com', password='password')

    @staticmethod
    def get_token_endpoint():
        return reverse('token_obtain_pair')

    @staticmethod
    def get_token_refresh_endpoint():
        return reverse('token_refresh')

    def test_token_with_missing_data(self):
        response = self.client.post(self.get_token_endpoint())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(["This field is required."], response.json()['username'])
        self.assertEqual(["This field is required."], response.json()['password'])

    def test_token_with_incorrect_data(self):
        data = {
            "username": self.user.username,
            "password": "wrong_password"
        }
        response = self.client.post(self.get_token_endpoint(), data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual('No active account found with the given credentials', response.json()['detail'])

    def test_token_with_correct_data(self):
        data = {
            "username": self.user.username,
            "password": "password"
        }
        response = self.client.post(self.get_token_endpoint(), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("access" in response.data)
        self.assertTrue("refresh" in response.data)

    def test_token_with_get_put_patch_delete(self):
        response = self.client.get(self.get_token_endpoint())
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.put(self.get_token_endpoint())
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.patch(self.get_token_endpoint())
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.delete(self.get_token_endpoint())
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_refresh_token_valid(self):
        data = {
            "username": self.user.username,
            "password": "password"
        }
        response = self.client.post(self.get_token_endpoint(), data=data)
        self.assertTrue("refresh" in response.data)

        # Let's imagine that enough time has passed for the access token to expire
        # (check setting from SIMPLE_JWT -> ACCESS_TOKEN_LIFETIME for managing token lifetime)

        refresh_token = response.data['refresh']
        data = {
            "refresh": refresh_token
        }
        refresh_response = self.client.post(self.get_token_refresh_endpoint(), data=data)
        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)
        self.assertTrue("access" in refresh_response.data)

    def test_refresh_token_invalid_data(self):
        data = {
            "refresh": "some_random_giberish_key_that_mimics_access_token"
        }
        refresh_response = self.client.post(self.get_token_refresh_endpoint(), data=data)
        self.assertEqual(refresh_response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue("Token is invalid or expired" in refresh_response.data['detail'])
        self.assertTrue("token_not_valid" in refresh_response.data['code'])
