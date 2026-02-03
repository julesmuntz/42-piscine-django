from django.shortcuts import render
from d06.settings import USERNAMES
from datetime import datetime
import random


def hello(request, page_title):
    if "username" not in request.session:
        request.session["username"] = random.choice(USERNAMES)
        request.session["_session_init_timestamp_"] = datetime.now().timestamp()

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
