from django.forms import CharField, Form


class Form(Form):
	textfield = CharField(label="", max_length=100)
