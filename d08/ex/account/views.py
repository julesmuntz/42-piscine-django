from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy as rl
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, TemplateView
from .forms import LoginForm, RegisterForm
from django.http import JsonResponse
from django.contrib.auth.models import User


class AccountView(LoginRequiredMixin, TemplateView):
    template_name = "d08/templates/account.html"
    login_url = rl("login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Account"
        return context


class AuthContextMixin:
    template_name = "d08/templates/login.html"
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
        return ""


class AjaxAuthMixin:
    def _is_ajax(self):
        return self.request.headers.get("X-Requested-With") == "XMLHttpRequest"

    def form_valid(self, form):
        if self._is_ajax():
            return self._ajax_form_valid(form)
        return super().form_valid(form)

    def form_invalid(self, form):
        if self._is_ajax():
            return JsonResponse(self._ajax_form_errors(form), status=400)
        return super().form_invalid(form)


class AuthRegisterView(AuthContextMixin, AjaxAuthMixin, CreateView):
    form_class = RegisterForm
    success_url = rl("account")
    page_title = "Register"
    action = "Register"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("account")
        return super().dispatch(request, *args, **kwargs)

    def _ajax_form_valid(self, form):
        self.object = form.save()
        login(self.request, self.object)
        return JsonResponse({"redirect": str(self.success_url)})

    def _ajax_form_errors(self, form):
        return {"errors": form.errors}

class AuthLoginView(AuthContextMixin, AjaxAuthMixin, LoginView):
    form_class = LoginForm
    page_title = "Login"
    action = "Login"
    redirect_authenticated_user = True

    def get_success_url(self):
        return str(rl("account"))

    def _ajax_form_valid(self, form):
        login(self.request, form.get_user())
        return JsonResponse({"redirect": self.get_success_url()})

    def _ajax_form_errors(self, form):
        username = self.request.POST.get("username", "")
        password = self.request.POST.get("password", "")
        username_exists = User.objects.filter(username__iexact=username).exists()
        return {
            "username_does_not_exist": bool(username) and not username_exists,
            "invalid_password": username_exists and bool(username and password),
        }


class AuthLogoutView(LogoutView):
    next_page = rl("account")

    def post(self, request, *args, **kwargs):
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return self.logout(request)
        return super().post(request, *args, **kwargs)

    def logout(self, request):
        super().logout(request)
        return JsonResponse({"redirect": str(self.next_page)})


@require_POST
def check_register(request):
    username = request.POST.get("username", "")
    username_is_empty = not username
    password = request.POST.get("password", "")
    password_confirm = request.POST.get("password_confirm", "")
    password_is_empty = not password
    data = {
        "username_is_empty": username_is_empty,
        "username_is_taken": (
            User.objects.filter(username__iexact=username).exists()
            if not username_is_empty
            else False
        ),
        "password_matches": (
            password == password_confirm if not password_is_empty else False
        ),
    }
    return JsonResponse(data)
