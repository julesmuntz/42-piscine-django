from django.shortcuts import render


def hub(request):
	exercises = []
	ex_modules = [
		"ex00",
	]

	for module_name in ex_modules:
		module = __import__(
			f"{module_name}.urls", fromlist=["urlpatterns"]
		)
		exercises.append({"name": module_name, "endpoints": module.urlpatterns})

	return render(request, "d06/templates/hub.html", {"exercises": exercises})
