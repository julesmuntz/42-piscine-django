import json
from datetime import datetime
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from . import database as chat_db
from .helpers import (
    chat_event_dict,
    join_message_text,
    leave_message_text,
    system_event_dict,
)
from .presence import PresenceTracker

presence = PresenceTracker()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]
        if not user.is_authenticated:
            await self.close()
            return

        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.room = await db_call(chat_db.get_room, self.room_id)
        if self.room is None:
            await self.close()
            return

        self.room_group_name = f"chatroom_{self.room_id}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        first_tab = await presence.user_connected(self.room_id, user.id)
        join_message = None
        if first_tab:
            await db_call(chat_db.add_member, self.room_id, user.id)
            join_message = await db_call(
                chat_db.create_message,
                self.room,
                user,
                join_message_text(user.username),
                is_system=True,
            )

        exclude_id = join_message.pk if join_message else None
        history = await db_call(
            chat_db.recent_messages_for_client,
            self.room_id,
            user.username,
            exclude_message_id=exclude_id,
        )
        await self.send_json("recent_messages", messages=history)

        if join_message is not None:
            await self.broadcast_system_message(user.username, join_message)

        if first_tab:
            members = await db_call(chat_db.list_member_usernames, self.room_id)
            await self.broadcast_members(members)

    async def disconnect(self, close_code):
        user = self.scope.get("user")
        room_id = getattr(self, "room_id", None)
        room_group_name = getattr(self, "room_group_name", None)

        if room_group_name:
            await self.channel_layer.group_discard(room_group_name, self.channel_name)

        if not self._can_process_leave(user, room_id, room_group_name):
            return

        last_tab = await presence.user_disconnected(room_id, user.id)
        if not last_tab:
            return

        removed = await db_call(chat_db.remove_member, room_id, user.id)
        if not removed:
            return

        leave_text = leave_message_text(user.username)
        room = await db_call(chat_db.get_room, room_id)
        db_user = await db_call(chat_db.get_user, user.id)
        if room is not None and db_user is not None:
            await db_call(chat_db.create_message, room, db_user, leave_text, is_system=True)

        await self.channel_layer.group_send(
            room_group_name,
            {
                "type": "chat_message",
                **system_event_dict(user.username, leave_text, datetime.now()),
            },
        )
        members = await db_call(chat_db.list_member_usernames, room_id)
        await self.broadcast_members(members)

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

        message = await db_call(chat_db.create_message, self.room, user, content)
        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "chat_message", **chat_event_dict(message)},
        )

    async def chat_message(self, event):
        await self.send_json(
            "chat_message",
            username=event["username"],
            message=event["content"],
            sent_at=event["sent_at"],
            message_type=event.get("message_type", "chat"),
        )

    async def members_update(self, event):
        await self.send_json("members_update", members=event["members"])

    async def broadcast_system_message(self, username, message):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                **system_event_dict(username, message.content, message.sent_at),
            },
        )

    async def broadcast_members(self, members):
        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "members_update", "members": members},
        )

    async def send_json(self, event_type, **fields):
        await self.send(text_data=json.dumps({"event_type": event_type, **fields}))

    def _can_process_leave(self, user, room_id, room_group_name):
        return room_id is not None and room_group_name is not None and user is not None and user.is_authenticated


async def db_call(func, *args, **kwargs):
    return await database_sync_to_async(func)(*args, **kwargs)
