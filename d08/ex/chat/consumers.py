import json
import asyncio
import datetime

from django.contrib.auth.models import User
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import ChatRoom, Message


class ChatConsumer(AsyncWebsocketConsumer):
    DISCONNECT_GRACE_SECONDS = 0.5
    _presence_lock = asyncio.Lock()
    _presence_counts = {}
    _pending_disconnects = {}
    _system_suffixes = (" has joined the chat", " has left the chat")

    async def connect(self):
        user = self.scope["user"]
        if not user.is_authenticated:
            await self.close()
            return

        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.room = await self._get_room(self.room_id)
        if self.room is None:
            await self.close()
            return

        self.room_group_name = f"chatroom_{self.room_id}"
        self.presence_key = self._build_presence_key(self.room_id, user.id)

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        await self._cancel_pending_disconnect(self.presence_key)
        is_first_connection = await self._increment_presence(self.presence_key)
        is_new_member = False
        join_message = None
        if is_first_connection:
            is_new_member = await self._add_member_if_new(self.room_id, user.id)
            if is_new_member:
                join_text = f"{user.username} has joined the chat"
                join_message = await self._create_message(self.room, user, join_text)

        initial_messages = await self._get_recent_messages(self.room_id, user.username)

        await self.send(
            text_data=json.dumps(
                {
                    "event_type": "recent_messages",
                    "messages": initial_messages,
                }
            )
        )

        if join_message is not None:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "username": user.username,
                    "content": join_message.content,
                    "sent_at": join_message.sent_at.strftime("%H:%M"),
                    "message_type": "system",
                },
            )

        if is_first_connection:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "members_update",
                    "members": await self._get_member_usernames(self.room_id),
                },
            )

    async def disconnect(self, close_code):
        user = self.scope.get("user")
        room_id = getattr(self, "room_id", None)
        room_group_name = getattr(self, "room_group_name", None)
        presence_key = getattr(self, "presence_key", None)

        if room_group_name:
            await self.channel_layer.group_discard(room_group_name, self.channel_name)

        if (
            room_id is not None
            and room_group_name is not None
            and presence_key is not None
            and user is not None
            and user.is_authenticated
        ):
            is_last_connection = await self._decrement_presence(presence_key)
            if is_last_connection:
                await self._schedule_disconnect_cleanup(
                    room_id=room_id,
                    room_group_name=room_group_name,
                    user_id=user.id,
                    username=user.username,
                    presence_key=presence_key,
                )

    async def _schedule_disconnect_cleanup(
        self, room_id, room_group_name, user_id, username, presence_key
    ):
        task = asyncio.create_task(
            self._finalize_disconnect_after_grace(
                room_id=room_id,
                room_group_name=room_group_name,
                user_id=user_id,
                username=username,
                presence_key=presence_key,
            )
        )
        async with self._presence_lock:
            existing_task = self._pending_disconnects.get(presence_key)
            if existing_task and not existing_task.done():
                existing_task.cancel()
            self._pending_disconnects[presence_key] = task

    async def _finalize_disconnect_after_grace(
        self, room_id, room_group_name, user_id, username, presence_key
    ):
        try:
            await asyncio.sleep(self.DISCONNECT_GRACE_SECONDS)
        except asyncio.CancelledError:
            return

        async with self._presence_lock:
            if self._presence_counts.get(presence_key, 0) > 0:
                self._pending_disconnects.pop(presence_key, None)
                return

        user_removed = await self._remove_member(room_id, user_id)
        if user_removed:
            leave_text = f"{username} has left the chat"
            room = await self._get_room(room_id)
            user = await self._get_user(user_id)
            if room is not None and user is not None:
                await self._create_message(room, user, leave_text)
            await self.channel_layer.group_send(
                room_group_name,
                {
                    "type": "chat_message",
                    "username": username,
                    "content": leave_text,
                    "sent_at": datetime.datetime.now().strftime("%H:%M"),
                    "message_type": "system",
                },
            )
            await self.channel_layer.group_send(
                room_group_name,
                {
                    "type": "members_update",
                    "members": await self._get_member_usernames(room_id),
                },
            )

        async with self._presence_lock:
            self._pending_disconnects.pop(presence_key, None)

    async def _cancel_pending_disconnect(self, presence_key):
        task = None
        async with self._presence_lock:
            task = self._pending_disconnects.pop(presence_key, None)

        if task and not task.done():
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass

    async def _increment_presence(self, presence_key):
        async with self._presence_lock:
            current_count = self._presence_counts.get(presence_key, 0)
            self._presence_counts[presence_key] = current_count + 1
            return current_count == 0

    async def _decrement_presence(self, presence_key):
        async with self._presence_lock:
            current_count = self._presence_counts.get(presence_key, 0)
            if current_count <= 1:
                self._presence_counts.pop(presence_key, None)
                return True
            self._presence_counts[presence_key] = current_count - 1
            return False

    def _build_presence_key(self, room_id, user_id):
        return f"{room_id}:{user_id}"

    async def receive(self, text_data):
        user = self.scope["user"]
        if not user.is_authenticated:
            await self.close()
            return

        try:
            payload = json.loads(text_data)
        except json.JSONDecodeError:
            return

        content = str(payload.get("message", "")).strip()
        if not content:
            return

        message = await self._create_message(self.room, user, content)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "username": message.user.username,
                "content": message.content,
                "sent_at": message.sent_at.strftime("%H:%M"),
                "message_type": "chat",
            },
        )

    async def chat_message(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "event_type": "chat_message",
                    "username": event["username"],
                    "message": event["content"],
                    "sent_at": event["sent_at"],
                    "message_type": event.get("message_type", "chat"),
                }
            )
        )

    async def members_update(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "event_type": "members_update",
                    "members": event["members"],
                }
            )
        )

    @database_sync_to_async
    def _get_room(self, room_id):
        return ChatRoom.objects.filter(pk=room_id).first()

    @database_sync_to_async
    def _create_message(self, room, user, content):
        return Message.objects.create(room=room, user=user, content=content)

    @database_sync_to_async
    def _get_user(self, user_id):
        return User.objects.filter(pk=user_id).first()

    @database_sync_to_async
    def _add_member_if_new(self, room_id, user_id):
        through_model = ChatRoom.members.through
        _, created = through_model.objects.get_or_create(
            chatroom_id=room_id,
            user_id=user_id,
        )
        return created

    @database_sync_to_async
    def _get_member_usernames(self, room_id):
        return list(
            ChatRoom.objects.get(pk=room_id).members.values_list("username", flat=True)
        )

    @database_sync_to_async
    def _remove_member(self, room_id, user_id):
        through_model = ChatRoom.members.through
        deleted, _ = through_model.objects.filter(
            chatroom_id=room_id,
            user_id=user_id,
        ).delete()
        return deleted > 0

    @database_sync_to_async
    def _get_recent_messages(self, room_id, username):
        last_join = (
            Message.objects.filter(
                room_id=room_id,
                content=f"{username} has joined the chat",
            )
            .order_by("-sent_at")
            .first()
        )
        if last_join is None:
            recent_messages = []
            ordered_messages = Message.objects.filter(room_id=room_id).select_related(
                "user"
            ).order_by("-sent_at")
            for message in ordered_messages:
                if self._is_system_message(message.content):
                    continue
                recent_messages.append(message)
                if len(recent_messages) == 3:
                    break
            return [
                self._serialize_chat_message(message)
                for message in reversed(recent_messages)
            ]

        messages_before_join = []
        before_join_queryset = (
            Message.objects.filter(room_id=room_id, sent_at__lt=last_join.sent_at)
            .select_related("user")
            .order_by("-sent_at")
        )
        for message in before_join_queryset:
            if self._is_system_message(message.content):
                continue
            messages_before_join.append(message)
            if len(messages_before_join) == 3:
                break

        messages_after_join = list(
            Message.objects.filter(room_id=room_id, sent_at__gte=last_join.sent_at)
            .select_related("user")
            .order_by("sent_at")
        )
        initial_messages = list(reversed(messages_before_join)) + messages_after_join
        return [self._serialize_chat_message(message) for message in initial_messages]

    def _is_system_message(self, content):
        return any(content.endswith(suffix) for suffix in self._system_suffixes)

    def _serialize_chat_message(self, message):
        return {
            "username": message.user.username,
            "message": message.content,
            "sent_at": message.sent_at.strftime("%H:%M"),
            "message_type": "system"
            if self._is_system_message(message.content)
            else "chat",
        }
