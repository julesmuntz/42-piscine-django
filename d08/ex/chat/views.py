from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView
from .forms import MessageForm
from .models import ChatRoom, Message


class ConnectedUserRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(
                request,
                "d08/templates/chat_unavailable.html",
                status=403,
            )
        return super().dispatch(request, *args, **kwargs)


class ChatRoomListView(ConnectedUserRequiredMixin, ListView):
    model = ChatRoom
    template_name = "d08/templates/chatrooms.html"
    context_object_name = "chatrooms"

    def get_queryset(self):
        return ChatRoom.objects.all()


class ChatRoomDetailView(ConnectedUserRequiredMixin, DetailView):
    model = ChatRoom
    template_name = "d08/templates/chatroom.html"
    context_object_name = "chatroom"
    SYSTEM_SUFFIXES = (" has joined the chat", " has left the chat")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_is_member = self.object.members.filter(pk=self.request.user.pk).exists()
        if not user_is_member:
            recent_messages = []
            for message in self.object.message_set.select_related("user").order_by("-sent_at"):
                if any(message.content.endswith(suffix) for suffix in self.SYSTEM_SUFFIXES):
                    continue
                recent_messages.append(message)
                if len(recent_messages) == 3:
                    break
            context["recent_messages"] = list(reversed(recent_messages))
            return context

        last_join = self.object.message_set.filter(
            content=f"{self.request.user.username} has joined the chat"
        ).order_by("-sent_at").first()
        if last_join is None:
            recent_messages = []
            for message in self.object.message_set.select_related("user").order_by("-sent_at"):
                if any(message.content.endswith(suffix) for suffix in self.SYSTEM_SUFFIXES):
                    continue
                recent_messages.append(message)
                if len(recent_messages) == 3:
                    break
            context["recent_messages"] = list(reversed(recent_messages))
            return context

        messages_before_join = []
        before_join_queryset = self.object.message_set.select_related("user").filter(
            sent_at__lt=last_join.sent_at
        ).order_by("-sent_at")
        for message in before_join_queryset:
            if any(message.content.endswith(suffix) for suffix in self.SYSTEM_SUFFIXES):
                continue
            messages_before_join.append(message)
            if len(messages_before_join) == 3:
                break

        messages_after_join = [
            message
            for message in self.object.message_set.select_related("user").filter(
                sent_at__gte=last_join.sent_at
            ).order_by("sent_at")
        ]

        context["recent_messages"] = list(reversed(messages_before_join)) + messages_after_join
        return context


class MessageCreateView(ConnectedUserRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.room = get_object_or_404(ChatRoom, pk=self.kwargs["pk"])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("chatroom", kwargs={"pk": self.kwargs["pk"]})
