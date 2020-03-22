from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from django.urls import reverse, reverse_lazy
from backend.models import Article
from frontend.forms import ArticleModelForm, ArticleEditModelForm


def index(request):
    return render(request, 'base.html')


class ArticleListView(ListView):
    queryset = Article.objects.all()
    template_name = 'frontend/article_list.html'
    # context_object_name = 'my_context_object_name'
    # paginate_by = 2

    def get_queryset(self):
        return self.queryset.filter(status='published')

    def get_context_data(self, **kwargs):
        context = super(ArticleListView, self).get_context_data(**kwargs)
        context['donald'] = 'monald'
        return context


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'frontend/article_detail.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     article = self.get_object()
    #     context['author'] = article.user
    #     return context


class ArticleCreateView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('frontend:login')
    queryset = Article.objects.all()
    model = Article
    template_name = 'frontend/article_create.html'
    form_class = ArticleModelForm
    # success_url = reverse_lazy('frontend:article-list')  # superseded by model.get_absolute_url()

    def get_success_url(self):
        return reverse_lazy('frontend:article-detail', kwargs={'slug': self.object.slug})

    def form_valid(self, form):
        form.instance.user = self.request.user  # Adding the current user to the model
        return super().form_valid(form)


class ArticleUpdateView(UserPassesTestMixin, UpdateView):
    model = Article
    template_name = 'frontend/article_edit.html'
    form_class = ArticleEditModelForm
    permission_denied_message = "NECES PROCI"

    def form_valid(self, form):
        return redirect(reverse_lazy('frontend:article-list'))

    def test_func(self):
        article = self.get_object()
        return self.request.user == article.user



