from django.shortcuts import render
from django.forms import Form, CharField
from django.conf import settings
import sys
import os
from datetime import datetime


class Ex02Form(Form):
	textfield = CharField(label="", max_length=100)


def writeLog(query: str) -> None:
	path = settings.LOG_FILE
	if not os.path.exists(path):
		open(path, "w").close()
	sys.stdout = open(path, "a")
	print(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} {query}")
	sys.stdout = sys.__stdout__


def readLog() -> list[str]:
	path = settings.LOG_FILE
	with open(path, "r") as file:
		return file.readlines()


def page(request):
	if request.method == "POST":
		form = Ex02Form(request.POST)
		if form.is_valid():
			writeLog(form.cleaned_data["textfield"])
	else:
		form = Ex02Form()

	context = {
		"form": form,
		"history": readLog()[::-1],
	}
	return render(
		request,
		"ex02/templates/form.html",
		context,
	)
