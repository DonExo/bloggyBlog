from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.template.defaultfilters import slugify
from django.urls import reverse

from .utils import ARTICLE_STATUS_CHOICES


class User(AbstractUser):
    first_name = models.CharField(max_length=255, blank=False)
    last_name = models.CharField(max_length=255, blank=False)
    email = models.EmailField(unique=True, blank=False)

    def __str__(self):
        return self.get_full_name()


class Topic(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


# Replaced the suggested name of Post with Article due to possible confusion
# for readers on Post with HTTP request of POST
class Article(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    slug = models.SlugField(max_length=255, unique=True)
    status = models.CharField(max_length=255, choices=ARTICLE_STATUS_CHOICES, default='draft')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='articles')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, **kwargs):
        if not self.id:
            # Let's create a unique slug
            date_time_object = datetime.utcnow().strftime("%d%m%Y%H%M%S")
            self.slug = "-".join([slugify(self.title), date_time_object])
        super().save(**kwargs)

    def is_published(self):
        return self.status == 'published'

    def publish(self):
        self.status = 'published'
        self.save()

    def get_absolute_url(self):
        return reverse('frontend:article-detail', kwargs={'slug': self.slug})
