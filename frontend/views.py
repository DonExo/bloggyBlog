from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import forms
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy

from backend.models import Article, Topic, User

from frontend.forms import ArticleModelForm
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
)


def index(request):
    return HttpResponse("Welcome to bloggyBlog")


class ArticleListView(ListView):
    queryset = Article.objects.all()
    template_name = 'frontend/article_list.html'

    def get_queryset(self):
        return self.queryset.filter(status='published')


class ArticleDetailView(DetailView):
    queryset = Article.objects.all()
    template_name = 'frontend/article_detail.html'

    # def get_object(self):
    #     return Article.objects.get()



class ArticleCreateView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('frontend:login')
    model = Article
    template_name = 'frontend/article_create.html'
    form_class = ArticleModelForm
    # success_url = reverse_lazy('frontend:article-list')  # superseded by model.get_absolute_url()

    def form_valid(self, form):
        form.instance.user = self.request.user  # Adding the current user to the model
        return super().form_valid(form)


class ArticleUpdateView(UpdateView):
    model = Article
    template_name = 'frontend/article_edit.html'
    form_class = ArticleModelForm



