from django.db import models


class Movies(models.Model):
	title = models.CharField(unique=True, max_length=64, default="")
	episode_nb = models.PositiveIntegerField(primary_key=True, default=0)
	opening_crawl = models.TextField(null=True)
	director = models.CharField(max_length=32, default="")
	producer = models.CharField(max_length=128, default="")
	release_date = models.DateField(default="")

	def __str__(self):
		return self.title
