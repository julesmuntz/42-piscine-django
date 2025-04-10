from django.shortcuts import render
from .models import Movies, Planets, People


def search(request, page_title):
	try:
		Movies._meta.db_table
		Planets._meta.db_table
		People._meta.db_table

		if not Movies.objects.exists() or not Planets.objects.exists() or not People.objects.exists():
			return render(
				request,
				"d05/templates/search.html",
				{"title": page_title, "no_data": True},
			)
	except Exception:
		return render(
			request,
			"d05/templates/search.html",
			{"title": page_title, "no_data": True},
		)

	genders = list(People.objects.values_list("gender", flat=True).distinct().exclude(gender__isnull=True))
	sorted_genders = sorted(genders, key=lambda x: ({"male": 0, "female": 1}.get(x, 2), x))
	context = {"title": page_title, "genders": sorted_genders, "has_searched": False}

	if request.method == "POST":
		min_date = request.POST.get("min_date")
		max_date = request.POST.get("max_date")
		min_diameter = request.POST.get("min_diameter")
		gender = request.POST.get("gender")

		results = []
		if all([min_date, max_date, min_diameter, gender]):
			characters = People.objects.filter(
				gender=gender,
				homeworld__diameter__gte=min_diameter,
				movies__release_date__range=[min_date, max_date],
			).distinct()

			for character in characters:
				movies = character.movies.filter(release_date__range=[min_date, max_date]).order_by("release_date")

				results.append(
					{
						"character_name": character.name,
						"gender": character.gender,
						"homeworld_name": character.homeworld.name if character.homeworld else "Unknown",
						"homeworld_diameter": character.homeworld.diameter if character.homeworld else "Unknown",
						"movies": [{"title": movie.title} for movie in movies],
						"rowspan": movies.count(),
					}
				)

		context.update({"has_searched": True, "results": results, "no_results": len(results) == 0})

	return render(request, "d05/templates/search.html", context)
