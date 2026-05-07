from django.shortcuts import render


def is_logged_in(request):
    return bool(request.session.get("username"))


def homepage(request, page_title):
    return render(
        request,
        "d06/templates/home.html",
        {
            "title": page_title,
            "logged_in": is_logged_in(request),
        },
    )
