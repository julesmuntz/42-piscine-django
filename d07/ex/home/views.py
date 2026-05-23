from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import get_user_model
from .models import Article, User, UserFavoriteArticle
from datetime import datetime
from django.contrib.auth import authenticate, login, logout as auth_logout


def is_logged_in(request):
    return bool(request.session.get("username"))


def _get_current_user(request):
    if not is_logged_in(request):
        return None
    username = request.session.get("username")
    if not username:
        return None
    return get_user_model().objects.filter(username=username).first()


def homepage(request, page_title):

    return render(
        request,
        "d07/templates/home.html",
        {
            "title": page_title,
            "logged_in": is_logged_in(request),
        },
    )


def auth(request, page_title, action):
    if action in ("Register", "Login") and is_logged_in(request):
        return redirect("/")
    if request.method == "GET":
        if request.path == "/register/":
            action = "Register"
        elif request.path == "/login/":
            action = "Login"
        return render(
            request,
            "d07/templates/auth.html",
            {
                "title": page_title,
                "username": "",
                "password": "",
                "password_confirm": "",
                "action": action,
            },
        )

    elif request.method == "POST":
        if is_logged_in(request):
            action = "Logout"
        elif request.path == "/register/":
            action = "Register"
        elif request.path == "/login/":
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
                request.session["anonymous"] = False
                request.session["_session_init_timestamp_"] = datetime.now().timestamp()
                request.session.set_expiry(None)
                login(request, user)
                return redirect("/")
            except Exception as e:
                return render(
                    request,
                    "d07/templates/auth.html",
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
                    request.session["anonymous"] = False
                    request.session["_session_init_timestamp_"] = (
                        datetime.now().timestamp()
                    )
                    request.session.set_expiry(None)
                    login(request, user)
                    return redirect("/")
                else:
                    raise Exception("Invalid username or password")
            except Exception as e:
                return render(
                    request,
                    "d07/templates/auth.html",
                    {
                        "title": page_title,
                        "username": username,
                        "password": password,
                        "message": str(e),
                        "action": action,
                    },
                )


def logout(request):
    auth_logout(request)
    return redirect("/")


def _update_author_reputation(author, user, vote_value, upvote_delta, downvote_delta):
    if author.id != user.id:
        if vote_value == Vote.UPVOTE:
            author.reputation += upvote_delta
        elif vote_value == Vote.DOWNVOTE:
            author.reputation += downvote_delta
        author.save(update_fields=["reputation"])


def delete_tip(request, tip_id):
    if request.method != "POST" or not is_logged_in(request):
        return redirect("/")

    current_user = _get_current_user(request)
    if not current_user:
        return redirect("/")

    tip = get_object_or_404(Tip, id=tip_id)
    can_delete = tip.upvotes - tip.downvotes <= -1 and (
        current_user.is_superuser
        or tip.author_id == current_user.id
        or current_user.reputation >= 30
    )
    if can_delete:
        votes = Vote.objects.filter(tip=tip)
        for vote in votes:
            _update_author_reputation(tip.author, vote.user, vote.value, -5, 2)
        tip.delete()
    return redirect("/")
