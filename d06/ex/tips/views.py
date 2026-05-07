from django.shortcuts import render
from .models import Tip


# Ex02: Our Tips!
def tips(request, page_title):
    if request.method == "GET":
        tips = Tip.objects.all().order_by("-date")
        return render(
            request,
            "d06/templates/tips.html",
            {
                "title": page_title,
                "tips": tips,
            },
        )
