from django.shortcuts import render
from ex00.views import get_db_connection
from ex03.models import Movies
from datetime import datetime


def populate(request, table_name, use_sql=True):
	movies_data = [
		(
			1,
			"The Phantom Menace",
			"George Lucas",
			"Rick McCallum",
			"1999-05-19",
			"""Turmoil has engulfed the Galactic Republic. The taxation of trade routes to outlying star systems is in dispute.

Hoping to resolve the matter with a blockade of deadly battleships, the greedy Trade Federation has stopped all shipping to the small planet of Naboo.

While the Congress of the Republic endlessly debates this alarming chain of events, the Supreme Chancellor has secretly dispatched two Jedi Knights, the guardians of peace and justice in the galaxy, to settle the conflict...""",
		),
		(
			2,
			"Attack of the Clones",
			"George Lucas",
			"Rick McCallum",
			"2002-05-16",
			"""There is unrest in the Galactic Senate. Several thousand solar systems have declared their intentions to leave the Republic.

This separatist movement, under the leadership of the mysterious Count Dooku, has made it difficult for the limited number of Jedi Knights to maintain peace and order in the galaxy.

Senator Amidala, the former Queen of Naboo, is returning to the Galactic Senate to vote on the critical issue of creating an ARMY OF THE REPUBLIC to assist the overwhelmed Jedi...""",
		),
		(
			3,
			"Revenge of the Sith",
			"George Lucas",
			"Rick McCallum",
			"2005-05-19",
			"""War! The Republic is crumbling under attacks by the ruthless Sith Lord, Count Dooku. There are heroes on both sides. Evil is everywhere.

In a stunning move, the fiendish droid leader, General Grievous, has swept into the Republic capital and kidnapped Chancellor Palpatine, leader of the Galactic Senate.

As the Separatist Droid Army attempts to flee the besieged capital with their valuable hostage, two Jedi Knights lead a desperate mission to rescue the captive Chancellor...""",
		),
		(
			4,
			"A New Hope",
			"George Lucas",
			"Gary Kurtz, Rick McCallum",
			"1977-05-25",
			"""It is a period of civil war. Rebel spaceships, striking from a hidden base, have won their first victory against the evil Galactic Empire.

During the battle, Rebel spies managed to steal secret plans to the Empire's ultimate weapon, the DEATH STAR, an armored space station with enough power to destroy an entire planet.

Pursued by the Empire's sinister agents, Princess Leia races home aboard her starship, custodian of the stolen plans that can save her people and restore freedom to the galaxy...""",
		),
		(
			5,
			"The Empire Strikes Back",
			"Irvin Kershner",
			"Gary Kurtz, Rick McCallum",
			"1980-05-17",
			"""It is a dark time for the Rebellion. Although the Death Star has been destroyed, Imperial troops have driven the Rebel forces from their hidden base and pursued them across the galaxy.

Evading the dreaded Imperial Starfleet, a group of freedom fighters led by Luke Skywalker has established a new secret base on the remote ice world of Hoth.

The evil lord Darth Vader, obsessed with finding young Skywalker, has dispatched thousands of remote probes into the far reaches of space...""",
		),
		(
			6,
			"Return of the Jedi",
			"Richard Marquand",
			"Howard G. Kazanjian, George Lucas, Rick McCallum",
			"1983-05-25",
			"""Luke Skywalker has returned to his home planet of Tatooine in an attempt to rescue his friend Han Solo from the clutches of the vile gangster Jabba the Hutt.

Little does Luke know that the GALACTIC EMPIRE has secretly begun construction on a new armored space station even more powerful than the first dreaded Death Star.

When completed, this ultimate weapon will spell certain doom for the small band of rebels struggling to restore freedom to the galaxy...""",
		),
		(
			7,
			"The Force Awakens",
			"J.J. Abrams",
			"Kathleen Kennedy, J.J. Abrams, Bryan Burk",
			"2015-12-11",
			"""Luke Skywalker has vanished. In his absence, the sinister FIRST ORDER has risen from the ashes of the Empire and will not rest until Skywalker, the last Jedi, has been destroyed.

With the support of the REPUBLIC, General Leia Organa leads a brave RESISTANCE. She is desperate to find her brother Luke and gain his help in restoring peace and justice to the galaxy.

Leia has sent her most daring pilot on a secret mission to Jakku, where an old ally has discovered a clue to Luke's whereabouts...""",
		),
	]
	messages = []
	if request.method == "POST":
		if use_sql:
			try:
				conn = get_db_connection()
				with conn.cursor() as cur:
					for movie in movies_data:
						try:
							cur.execute(
								f"""
								INSERT INTO {table_name}
								(episode_nb, title, director, producer, release_date, opening_crawl)
								VALUES
								(%s, %s, %s, %s, %s, %s)
								""",
								(
									movie[0],
									movie[1],
									movie[2],
									movie[3],
									datetime.strptime(movie[4], "%Y-%m-%d"),
									movie[5],
								),
							)
							conn.commit()
							messages.append("OK")
						except Exception as e:
							messages.append(str(e))
							conn.rollback()
			except Exception as e:
				messages.append(str(e))
			finally:
				conn.close()
		else:
			for movie in movies_data:
				try:
					Movies.objects.create(
						episode_nb=movie[0],
						title=movie[1],
						director=movie[2],
						producer=movie[3],
						release_date=datetime.strptime(movie[4], "%Y-%m-%d"),
						opening_crawl=movie[5],
					)
					messages.append("OK")
				except Exception as e:
					messages.append(str(e))

	return render(
		request,
		"d05/templates/form.html",
		{"message": " ".join(messages) if messages else "", "label": f"Insert movies into {table_name}"},
	)


def to_roman(num):
	val = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
	syms = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]
	roman_num = ""
	i = 0
	while num > 0:
		for _ in range(num // val[i]):
			roman_num += syms[i]
			num -= val[i]
		i += 1
	return roman_num


def display(request, table_name, use_sql=True):
	if use_sql:
		try:
			conn = get_db_connection()
			with conn.cursor() as cur:
				cur.execute(
					f"SELECT episode_nb, title, director, producer, release_date, opening_crawl FROM {table_name} ORDER BY episode_nb;"
				)
				rows = cur.fetchall()
			if not rows:
				return render(request, "d05/templates/display.html", {"message": "No data available"})
			roman_rows = []
			for row in rows:
				producer_names = row[3].split(", ")
				formatted_producers = "<br>".join(producer_names)
				roman_row = (to_roman(row[0]),) + row[1:3] + (formatted_producers,) + row[4:]
				roman_rows.append(roman_row)
			return render(request, "d05/templates/display.html", {"rows": roman_rows})
		except Exception:
			return render(request, "d05/templates/display.html", {"message": "No data available"})
	else:
		try:
			movies = Movies.objects.all().order_by("episode_nb")
			if not movies:
				return render(request, "d05/templates/display.html", {"message": "No data available"})

			roman_rows = []
			for movie in movies:
				producer_names = movie.producer.split(", ")
				formatted_producers = "<br>".join(producer_names)
				roman_rows.append(
					(
						to_roman(movie.episode_nb),
						movie.title,
						movie.director,
						formatted_producers,
						movie.release_date,
						movie.opening_crawl,
					)
				)
			return render(request, "d05/templates/display.html", {"rows": roman_rows})
		except Exception:
			return render(request, "d05/templates/display.html", {"message": "No data available"})
