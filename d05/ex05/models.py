from ex01.models import AMovies


class Movies(AMovies):
	class Meta:
		db_table = "ex05_movies"
