from ex01.models import AMovies
from ex09.models import APlanets, APeople
from django.db import models


class Planets(APlanets):
	class Meta:
		db_table = "ex10_planets"


class People(APeople):
	homeworld = models.ForeignKey(
		Planets,
		models.SET_NULL,
		blank=True,
		null=True,
		related_name="ex10_inhabitants",
	)

	class Meta:
		db_table = "ex10_people"


class Movies(AMovies):
	characters = models.ManyToManyField(People, related_name="movies")

	class Meta:
		db_table = "ex10_movies"
