from django.shortcuts import render

def init(request):
	return render(
		request,
		"d06/templates/form.html",
		{
			"label": "init",
		},
	)
