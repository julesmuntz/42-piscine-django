from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import CreateView, ListView, RedirectView, DetailView
from .forms import ArticleForm, RegisterForm
from .models import Article, UserFavoriteArticle


def is_logged_in(request):
    return request.user.is_authenticated


class HomeView(RedirectView):
    url = reverse_lazy("articles")


class AuthContextMixin:
    template_name = "d07/templates/login.html"
    page_title = ""
    action = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = context.get("form")
        context["title"] = self.page_title
        context["action"] = self.action
        context["username"] = form["username"].value() if form else ""
        context["message"] = self._get_error_message(form)
        return context

    def _get_error_message(self, form):
        if not form or not form.errors:
            return ""

        non_field_errors = form.non_field_errors()
        if non_field_errors:
            return non_field_errors[0]

        for field_errors in form.errors.values():
            if field_errors:
                return field_errors[0]

        return ""


class AuthRegisterView(AuthContextMixin, CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy("home")
    page_title = "Register"
    action = "Register"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class AuthLoginView(AuthContextMixin, LoginView):
    page_title = "Login"
    action = "Login"
    redirect_authenticated_user = True

    def get_success_url(self):
        return str(reverse_lazy("home"))


class AuthLogoutView(LogoutView):
    next_page = reverse_lazy("home")


class ArticleListView(ListView):
    model = Article
    template_name = "d07/templates/articles.html"
    context_object_name = "articles"

    def get_queryset(self):
        return Article.objects.all().order_by("-created")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["logged_in"] = is_logged_in(self.request)
        return context


class ArticleView(DetailView):
    model = Article
    template_name = "d07/templates/article.html"
    context_object_name = "article"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.object.title
        return context


class PublicationListView(LoginRequiredMixin, CreateView):
    model = Article
    template_name = "d07/templates/publications.html"
    context_object_name = "publications"
    form_class = ArticleForm
    success_url = reverse_lazy("publications")
    login_url = reverse_lazy("login")

    def get_queryset(self):
        return Article.objects.filter(author=self.request.user).order_by("-created")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["logged_in"] = is_logged_in(self.request)
        context["publications"] = self.get_queryset()
        return context


class PublicationView(LoginRequiredMixin, DetailView):
    model = Article
    template_name = "d07/templates/publication.html"
    context_object_name = "publication"
    login_url = reverse_lazy("login")

    def get_queryset(self):
        return Article.objects.filter(author=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.object.title
        return context


class FavoriteArticlesView(LoginRequiredMixin, ListView):
    model = UserFavoriteArticle
    template_name = "d07/templates/favorites.html"
    context_object_name = "favorite_articles"
    login_url = reverse_lazy("login")

    def get_queryset(self):
        return (
            Article.objects.filter(userfavoritearticle__user=self.request.user)
            .order_by("-created")
            .distinct()
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["logged_in"] = is_logged_in(self.request)
        return context

class AddFavoriteArticleView(LoginRequiredMixin, View):
    login_url = reverse_lazy("login")

    def post(self, request, pk, *args, **kwargs):
        article = get_object_or_404(Article, pk=pk)
        UserFavoriteArticle.objects.get_or_create(
            user=request.user,
            article=article,
        )
        return redirect("favorites")