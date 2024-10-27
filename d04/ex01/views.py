from django.shortcuts import render


def pages():
	return {
		"Django": "/ex01/django",
		"Display": "/ex01/display",
		"Templates": "/ex01/templates",
	}


def django(request):
	context = {
		"style": 1,
		"pages": pages(),
	}
	return render(request, "ex01/templates/django.html", context)


def display(request):
	context = {
		"style": 1,
		"pages": pages(),
	}
	return render(request, "ex01/templates/display.html", context)


def templates(request):
	context = {
		"style": 2,
		"pages": pages(),
	}
	return render(request, "ex01/templates/templates.html", context)
