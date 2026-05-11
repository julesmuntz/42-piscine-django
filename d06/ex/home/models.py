from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class User(AbstractUser):
    reputation = models.IntegerField(default=0)

    def __str__(self):
        return self.username


class Tip(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)

    def __str__(self):
        return self.content


class Vote(models.Model):
    UPVOTE = 1
    DOWNVOTE = -1
    VALUE_CHOICES = (
        (UPVOTE, "upvote"),
        (DOWNVOTE, "downvote"),
    )

    tip = models.ForeignKey(Tip, on_delete=models.CASCADE, related_name="votes")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.SmallIntegerField(choices=VALUE_CHOICES)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["tip", "user"], name="unique_tip_vote_per_user")
        ]
