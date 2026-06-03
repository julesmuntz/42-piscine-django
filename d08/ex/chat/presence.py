import asyncio


class PresenceTracker:
    def __init__(self):
        self._lock = asyncio.Lock()
        self._counts = {}

    @staticmethod
    def key(room_id, user_id):
        return f"{room_id}:{user_id}"

    async def user_connected(self, room_id, user_id):
        presence_key = self.key(room_id, user_id)
        async with self._lock:
            count = self._counts.get(presence_key, 0)
            self._counts[presence_key] = count + 1
            return count == 0

    async def user_disconnected(self, room_id, user_id):
        presence_key = self.key(room_id, user_id)
        async with self._lock:
            count = self._counts.get(presence_key, 0)
            if count <= 1:
                self._counts.pop(presence_key, None)
                return True
            self._counts[presence_key] = count - 1
            return False
