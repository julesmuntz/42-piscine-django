from django.contrib import admin

from .models import User, Tip, Vote

admin.site.register(User)
admin.site.register(Tip)
admin.site.register(Vote)