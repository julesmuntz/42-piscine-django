from django.db import models


class APlanets(models.Model):
	name = models.CharField(max_length=64, unique=True)
	climate = models.CharField(max_length=255, null=True)
	diameter = models.IntegerField(null=True)
	orbital_period = models.IntegerField(null=True)
	population = models.BigIntegerField(null=True)
	rotation_period = models.IntegerField(null=True)
	surface_water = models.FloatField(null=True)
	terrain = models.CharField(max_length=128, null=True)

	def __str__(self):
		return self.name

	class Meta:
		abstract = True


class Planets(APlanets):
	created = models.DateTimeField(auto_now_add=True, null=True)
	updated = models.DateTimeField(auto_now=True, null=True)

	class Meta:
		db_table = "ex09_planets"


class APeople(models.Model):
	name = models.CharField(max_length=64)
	birth_year = models.CharField(max_length=32, null=True)
	gender = models.CharField(max_length=32, null=True)
	eye_color = models.CharField(max_length=32, null=True)
	hair_color = models.CharField(max_length=32, null=True)
	height = models.IntegerField(null=True)
	mass = models.FloatField(null=True)

	def __str__(self):
		return self.name

	class Meta:
		abstract = True


class People(APeople):
	homeworld = models.ForeignKey(
		Planets,
		models.SET_NULL,
		blank=True,
		null=True,
		related_name="ex09_inhabitants",
	)
	created = models.DateTimeField(auto_now_add=True, null=True)
	updated = models.DateTimeField(auto_now=True, null=True)

	class Meta:
		db_table = "ex09_people"
