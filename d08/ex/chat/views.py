from django.views.generic import TemplateView


class ChatView(TemplateView):
    template_name = "d08/templates/chat.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["chat"] = "chat"
        return context
