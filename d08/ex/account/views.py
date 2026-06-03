from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.views import View
from django.views.generic.base import TemplateResponseMixin

from chat.message_history import get_preview_messages, get_recent_message_objects
from chat.models import ChatRoom

from .ajax import ajax_json_response, ajax_ok, is_ajax_request
from .forms import LoginForm, RegisterForm


class AccountView(TemplateResponseMixin, View):
    template_name = "d08/templates/account.html"

    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        action = request.POST.get("action")
        handlers = {
            "login": self._post_login,
            "register": self._post_register,
            "logout": self._post_logout,
            "check_register": self._post_check_register,
        }
        handler = handlers.get(action)
        if handler is None:
            return ajax_json_response({"error": "Unknown action"}, status=400)
        return handler(request)

    def get_context_data(self, **kwargs):
        request = self.request
        return {
            "login_form": LoginForm(prefix="login"),
            "register_form": RegisterForm(prefix="register"),
            **self._chat_context(request),
        }

    def _chat_context(self, request):
        user = request.user
        chatrooms = ChatRoom.objects.prefetch_related("members").all()
        chatroom_payloads = []
        for chatroom in chatrooms:
            if user.is_authenticated and chatroom.members.filter(pk=user.pk).exists():
                recent_messages = get_recent_message_objects(chatroom.pk, user.username)
            else:
                recent_messages = get_preview_messages(chatroom.pk)
            chatroom_payloads.append({"chatroom": chatroom, "recent_messages": recent_messages})
        return {
            "chatrooms": chatrooms,
            "chatroom_payloads": chatroom_payloads,
        }

    def _post_login(self, request):
        form = LoginForm(request, data=request.POST, prefix="login")
        if form.is_valid():
            login(request, form.get_user())
            if is_ajax_request(request):
                return ajax_ok({"username": request.user.username})
            return self.render_to_response(self.get_context_data())
        if is_ajax_request(request):
            username = request.POST.get("login-username", "")
            password = request.POST.get("login-password", "")
            username_exists = User.objects.filter(username__iexact=username).exists()
            return ajax_json_response(
                {
                    "username_does_not_exist": bool(username) and not username_exists,
                    "invalid_password": username_exists and bool(username and password),
                },
                status=400,
            )
        return self.render_to_response(self.get_context_data())

    def _post_register(self, request):
        form = RegisterForm(request.POST, prefix="register")
        if form.is_valid():
            user = form.save()
            login(request, user)
            if is_ajax_request(request):
                return ajax_ok({"username": request.user.username})
            return self.render_to_response(self.get_context_data())
        if is_ajax_request(request):
            return ajax_json_response({"errors": form.errors}, status=400)
        return self.render_to_response(self.get_context_data())

    def _post_logout(self, request):
        logout(request)
        if is_ajax_request(request):
            return ajax_ok()
        return self.render_to_response(self.get_context_data())

    def _post_check_register(self, request):
        username = request.POST.get("username", "") or request.POST.get("register-username", "")
        password = request.POST.get("password", "") or request.POST.get("register-password", "")
        password_confirm = request.POST.get("password_confirm", "") or request.POST.get("register-password_confirm", "")
        username_is_empty = not username
        password_is_empty = not password
        return ajax_json_response(
            {
                "username_is_empty": username_is_empty,
                "username_is_taken": (
                    User.objects.filter(username__iexact=username).exists() if not username_is_empty else False
                ),
                "password_matches": (password == password_confirm if not password_is_empty else False),
            }
        )
