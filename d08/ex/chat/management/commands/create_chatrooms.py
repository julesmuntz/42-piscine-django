from django.core.management.base import BaseCommand

from chat.models import ChatRoom


class Command(BaseCommand):
    help = "Create the default chatrooms (Alpha, Beta, Gamma)."

    def handle(self, *args, **options):
        room_names = ("Alpha", "Beta", "Gamma")
        missing = [
            name
            for name in room_names
            if not ChatRoom.objects.filter(name=name).exists()
        ]

        if not missing:
            return

        for name in missing:
            ChatRoom.objects.create(name=name)
            self.stdout.write(self.style.SUCCESS(f"Created chatroom: {name}"))
