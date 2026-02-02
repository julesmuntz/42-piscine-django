from django.shortcuts import render
from d06.settings import USERNAMES
import random


def hello(request, page_title):
    # Session logic: assign username to session if not already set
    if "username" not in request.session:
        request.session["username"] = random.choice(USERNAMES)

    username = request.session["username"]

    if request.method == "GET":
        return render(
            request,
            "d06/templates/text.html",
            {
                "title": page_title,
                "message": f"Hello {username}!",
            },
        )
