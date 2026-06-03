from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import render


class ConnectedUserRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(
                request,
                "d08/templates/chat_unavailable.html",
                status=403,
            )
        return super().dispatch(request, *args, **kwargs)
