from django.urls import path
from .views import (
    ChatRoomListView,
    ChatRoomDetailView,
    MessageCreateView,
)


urlpatterns = [
    path(
        "chatrooms/",
        ChatRoomListView.as_view(),
        name="chatrooms",
    ),
    path(
        "chatroom/<int:pk>/",
        ChatRoomDetailView.as_view(),
        name="chatroom",
    ),
    path(
        "chatroom/<int:pk>/send_message/",
        MessageCreateView.as_view(),
        name="send_message",
    ),
]
