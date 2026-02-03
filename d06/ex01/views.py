from django.shortcuts import render
from d06.settings import USERNAMES
from django.contrib.auth.models import User
from datetime import datetime
from django.contrib.auth import authenticate
from django.shortcuts import redirect


def is_logged_in(request):
    return bool(request.session.get("username"))

def auth(request, page_title, action):
    if action in ("Register", "Login") and is_logged_in(request):
        return redirect("/")
    if request.method == "GET":
        if request.path == "/ex01/register/":
            action = "Register"
        elif request.path == "/ex01/login/":
            action = "Login"
        return render(
            request,
            "d06/templates/auth.html",
            {
                "title": page_title,
                "username": "",
                "password": "",
                "password_confirm": "",
                "action": action,
                "is_logged_in": is_logged_in(request),
            },
        )

    elif request.method == "POST":
        if is_logged_in(request):
            action = "Logout"
        elif request.path == "/ex01/register/":
            action = "Register"
        elif request.path == "/ex01/login/":
            action = "Login"

        if action == "Logout":
            return logout(request)
        elif action == "Register":
            try:
                username = request.POST.get("username") or ""
                password = request.POST.get("password") or ""
                password_confirm = request.POST.get("password_confirm") or ""
                if not username:
                    raise Exception("Username is required")
                if username and User.objects.filter(username=username).exists():
                    raise Exception("User already exists")
                if not password:
                    raise Exception("Password is required")
                if not password_confirm:
                    raise Exception("Password confirmation is required")
                if password != password_confirm:
                    raise Exception("Passwords do not match")

                user = User.objects.create_user(username, password=password)
                user.save()
                request.session["username"] = username
                request.session["_session_init_timestamp_"] = datetime.now().timestamp()
                return redirect("/")
            except Exception as e:
                return render(
                    request,
                    "d06/templates/auth.html",
                    {
                        "title": page_title,
                        "username": username,
                        "password": password,
                        "password_confirm": password_confirm,
                        "message": str(e),
                        "action": action,
                    },
                )
        elif action == "Login":
            try:
                username = request.POST.get("username") or ""
                password = request.POST.get("password") or ""
                if not username:
                    raise Exception("Username is required")
                if not password:
                    raise Exception("Password is required")
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    request.session["username"] = username
                    request.session["_session_init_timestamp_"] = (
                        datetime.now().timestamp()
                    )
                    return redirect("/")
                else:
                    raise Exception("Invalid username or password")
            except Exception as e:
                return render(
                    request,
                    "d06/templates/auth.html",
                    {
                        "title": page_title,
                        "username": username,
                        "password": password,
                        "message": str(e),
                        "action": action,
                    },
                )


def logout(request):
    request.session.flush()
    return redirect("/")
