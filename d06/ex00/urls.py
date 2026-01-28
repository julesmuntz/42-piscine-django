from django.urls import path
from .views import init


def get_urlpatterns():
	return [
		path(
			"init/",
			init,
		),
	]


urlpatterns = get_urlpatterns()
