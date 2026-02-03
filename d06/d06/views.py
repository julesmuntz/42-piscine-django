from django.shortcuts import render


def hub(request):
	exercises = []
	ex_modules = [
		"ex00",
		"ex01",
	]

	for module_name in ex_modules:
		module = __import__(
			f"{module_name}.urls", fromlist=["page_title", "urlpatterns"]
		)
		title = module.page_title
		endpoints = []
		for pattern in module.urlpatterns:
			default_args = getattr(pattern, "default_args", {}) or {}
			if not default_args.get("page_title"):
				continue
			path = pattern.pattern.regex.pattern
			endpoint = (
				path.replace("^", "").replace("$", "").replace("\\Z", "").rstrip("/")
			)
			endpoint_title = default_args.get("page_title") or title
			endpoints.append({"path": endpoint, "title": endpoint_title})

		exercises.append({"name": module_name, "title": title, "endpoints": endpoints})

	return render(request, "d06/templates/hub.html", {"exercises": exercises})
