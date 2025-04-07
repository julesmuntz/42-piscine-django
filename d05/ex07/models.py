from ex01.models import AMovies
from django.db import models


class Movies(AMovies):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "ex07_movies"
