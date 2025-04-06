from django.shortcuts import render


def hub(request):
	return render(
		request,
		"d05/templates/hub.html",
		{
			"title": "Piscine Django - d05",
		},
	)
