from django.test import TestCase

from backend.models import User


class TestUser(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create(first_name='John', last_name='Doe', username='johndoe')
        super(TestUser, cls).setUpClass()

    def test_number_of_users(self):
        self.assertEqual(len(User.objects.all()), 1)