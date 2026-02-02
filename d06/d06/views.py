from django.shortcuts import render


def hub(request):
	exercises = []
	ex_modules = [
		"ex00",
	]

	for module_name in ex_modules:
		module = __import__(
			f"{module_name}.urls", fromlist=["page_title", "urlpatterns"]
		)
		title = module.page_title
		endpoints = []
		for pattern in module.urlpatterns:
			path = pattern.pattern.regex.pattern
			endpoint = (
				path.replace("^", "").replace("$", "").replace("\\Z", "").rstrip("/")
			)
			if endpoint:
				endpoints.append(endpoint)

		exercises.append({"name": module_name, "title": title, "endpoints": endpoints})

	return render(request, "d06/templates/hub.html", {"exercises": exercises})
