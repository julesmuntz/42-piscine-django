from .helpers import RECENT_CHAT_LIMIT, join_message_text
from .models import Message


def _last_chat_messages(room_id, before=None, limit=RECENT_CHAT_LIMIT):
    queryset = Message.objects.filter(room_id=room_id, is_system=False).select_related("user")
    if before is not None:
        queryset = queryset.filter(sent_at__lt=before)
    return list(queryset.order_by("-sent_at")[:limit][::-1])


def get_preview_messages(room_id, limit=RECENT_CHAT_LIMIT):
    return _last_chat_messages(room_id, limit=limit)


def _find_join_message(room_id, username, before=None):
    queryset = Message.objects.filter(
        room_id=room_id,
        is_system=True,
        content=join_message_text(username),
    )
    if before is not None:
        queryset = queryset.filter(sent_at__lt=before)
    return queryset.order_by("-sent_at").first()


def _show_in_member_history(message, username):
    if not message.is_system:
        return True
    return message.content == join_message_text(username)


def _messages_since(room_id, since, username, exclude_message_id=None):
    queryset = Message.objects.filter(room_id=room_id, sent_at__gte=since).select_related("user").order_by("sent_at")
    messages = []
    for message in queryset:
        if exclude_message_id is not None and message.pk == exclude_message_id:
            continue
        if _show_in_member_history(message, username):
            messages.append(message)
    return messages


def get_recent_message_objects(room_id, username, exclude_message_id=None):
    latest_join = _find_join_message(room_id, username)
    if latest_join is None:
        return get_preview_messages(room_id)

    preview = _last_chat_messages(room_id, before=latest_join.sent_at)
    current_session = _messages_since(
        room_id,
        latest_join.sent_at,
        username,
        exclude_message_id=exclude_message_id,
    )
    return preview + current_session
