from django.contrib.auth.models import User
from .helpers import message_to_client_dict
from .message_history import get_recent_message_objects
from .models import ChatRoom, Message


def get_room(room_id):
    return ChatRoom.objects.filter(pk=room_id).first()


def get_user(user_id):
    return User.objects.filter(pk=user_id).first()


def create_message(room, user, content, *, is_system=False):
    return Message.objects.create(room=room, user=user, content=content, is_system=is_system)


def add_member(room_id, user_id):
    through = ChatRoom.members.through
    through.objects.get_or_create(chatroom_id=room_id, user_id=user_id)


def remove_member(room_id, user_id):
    through = ChatRoom.members.through
    deleted, _ = through.objects.filter(
        chatroom_id=room_id,
        user_id=user_id,
    ).delete()
    return deleted > 0


def list_member_usernames(room_id):
    return list(ChatRoom.objects.get(pk=room_id).members.values_list("username", flat=True))


def recent_messages_for_client(room_id, username, exclude_message_id=None):
    messages = get_recent_message_objects(room_id, username, exclude_message_id=exclude_message_id)
    return [message_to_client_dict(message) for message in messages]
