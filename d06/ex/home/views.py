from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import get_user_model
from .models import Tip, User, Vote
from .forms import TipForm
from d06.settings import USERNAMES
from datetime import datetime
from django.contrib.auth import authenticate
import random


def is_logged_in(request):
    return bool(request.session.get("username"))


def is_anonymous_session(request):
    return bool(request.session.get("anonymous"))


def _get_current_user(request):
    if not is_logged_in(request) or is_anonymous_session(request):
        return None
    username = request.session.get("username")
    if not username:
        return None
    return get_user_model().objects.filter(username=username).first()


def homepage(request, page_title):
    form = TipForm()
    if (
        request.method == "POST"
        and is_logged_in(request)
        and not is_anonymous_session(request)
    ):
        form = TipForm(request.POST)
        username = request.session.get("username")
        if form.is_valid() and username:
            user_model = get_user_model()
            user = user_model.objects.filter(username=username).first()
            if user:
                tip = form.save(commit=False)
                tip.author = user
                tip.save()
        return redirect("/")

    tips = list(Tip.objects.all().order_by("-date"))
    current_user = None
    user_votes_by_tip_id = {}
    current_user = _get_current_user(request)
    if current_user:
        user_votes_by_tip_id = {
            vote.tip_id: vote.value
            for vote in Vote.objects.filter(user=current_user, tip__in=tips)
        }
    for tip in tips:
        tip.score = tip.upvotes - tip.downvotes
        tip.user_vote = user_votes_by_tip_id.get(tip.id, 0)
        tip.can_downvote = bool(
            current_user
            and (current_user.is_superuser or tip.author_id == current_user.id)
        )
        tip.can_delete = bool(
            current_user
            and tip.score <= -1
            and (current_user.is_superuser or tip.author_id == current_user.id)
        )

    return render(
        request,
        "d06/templates/home.html",
        {
            "title": page_title,
            "logged_in": is_logged_in(request),
            "anonymous": is_anonymous_session(request),
            "tip_form": form,
            "tips": tips,
        },
    )


# Ex00: Anonymous Sessions
def status(request, page_title):
    if "username" not in request.session:
        request.session["username"] = random.choice(USERNAMES)
        request.session["anonymous"] = True
        request.session["_session_init_timestamp_"] = datetime.now().timestamp()
        request.session.set_expiry(42)

    username = request.session["username"]

    if request.method == "GET":
        return render(
            request,
            "d06/templates/status.html",
            {
                "title": page_title,
                "message": f"Hello {username}!",
            },
        )


# Ex01: User Creation
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
                    request.session["anonymous"] = False
                    request.session["_session_init_timestamp_"] = (
                        datetime.now().timestamp()
                    )
                    request.session.set_expiry(None)
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


def delete_tip(request, tip_id):
    if (
        request.method != "POST"
        or not is_logged_in(request)
        or is_anonymous_session(request)
    ):
        return redirect("/")

    current_user = _get_current_user(request)
    if not current_user:
        return redirect("/")

    tip = get_object_or_404(Tip, id=tip_id)
    can_delete = tip.upvotes - tip.downvotes <= -1 and (
        current_user.is_superuser or tip.author_id == current_user.id
    )
    if can_delete:
        tip.delete()
    return redirect("/")


def _refresh_tip_vote_counts(tip):
    tip.upvotes = Vote.objects.filter(tip=tip, value=Vote.UPVOTE).count()
    tip.downvotes = Vote.objects.filter(tip=tip, value=Vote.DOWNVOTE).count()
    tip.save(update_fields=["upvotes", "downvotes"])


def _toggle_tip_vote(request, tip_id, vote_value):
    if (
        request.method != "POST"
        or not is_logged_in(request)
        or is_anonymous_session(request)
    ):
        return redirect("/")

    username = request.session.get("username")
    if not username:
        return redirect("/")

    user = get_user_model().objects.filter(username=username).first()
    if not user:
        return redirect("/")

    tip = get_object_or_404(Tip, id=tip_id)
    if vote_value == Vote.DOWNVOTE and not (
        user.is_superuser or tip.author_id == user.id
    ):
        return redirect("/")

    vote = Vote.objects.filter(tip=tip, user=user).first()
    if vote is None:
        Vote.objects.create(tip=tip, user=user, value=vote_value)
    elif vote.value == vote_value:
        vote.delete()
    else:
        vote.value = vote_value
        vote.save(update_fields=["value"])

    _refresh_tip_vote_counts(tip)
    return redirect("/")


def upvote(request, tip_id):
    return _toggle_tip_vote(request, tip_id, Vote.UPVOTE)


def downvote(request, tip_id):
    return _toggle_tip_vote(request, tip_id, Vote.DOWNVOTE)
