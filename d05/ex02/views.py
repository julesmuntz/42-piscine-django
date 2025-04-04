from django.shortcuts import render
import psycopg2
from decouple import config


def get_db_connection():
	"""Create and return a database connection"""
	return psycopg2.connect(
		dbname=config("DB_NAME"),
		user=config("DB_USER"),
		password=config("DB_PASSWORD"),
		host=config("DB_HOST"),
		port=config("DB_PORT"),
	)


def create_movies_table(conn):
	try:
		commands = (
			"""
			CREATE TABLE ex02_movies (
				title VARCHAR(64) NOT NULL,
				episode_nb INTEGER PRIMARY KEY,
				opening_crawl TEXT,
				director VARCHAR(32) NOT NULL,
				producer VARCHAR(128) NOT NULL,
				release_date DATE NOT NULL
			)
			""",
		)
		with conn.cursor() as cur:
			for command in commands:
				cur.execute(command)
		return "OK"
	except (psycopg2.DatabaseError, Exception) as error:
		return error


def populate_movies_table(conn):
	try:
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
		with conn.cursor() as cur:
			cur.executemany(
				"""
				INSERT INTO ex02_movies (
					episode_nb,
					title,
					director,
					producer,
					release_date,
					opening_crawl
				)
				VALUES (%s, %s, %s, %s, %s, %s)
			""",
				movies_data,
			)
		return "OK"
	except (psycopg2.DatabaseError, Exception) as error:
		return error


def init(request):
	message = "OK"
	try:
		with get_db_connection() as conn:
			cur = conn.cursor()
			cur.execute("SELECT EXISTS(SELECT relname FROM pg_class WHERE relname='ex02_movies')")
			exist = cur.fetchone()[0]
			if not exist:
				message = 'relation "ex02_movies" does not exist'
			if request.method == "POST":
				message = create_movies_table(conn)
	except psycopg2.Error as e:
		message = str(e)

	return render(
		request,
		"d05/templates/init.html",
		{
			"title": "SQL - Building a Table",
			"message": message,
		},
	)


def populate(request):
	message = "OK"
	try:
		with get_db_connection() as conn:
			if request.method == "POST":
				message = populate_movies_table(conn)
	except psycopg2.Error as e:
		message = str(e)

	return render(
		request,
		"d05/templates/populate.html",
		{
			"title": "SQL - Populating a Table",
			"message": message,
		},
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


def display(request):
	message = ""
	rows = []
	try:
		with get_db_connection() as conn:
			with conn.cursor() as cur:
				cur.execute(
					"""
					SELECT episode_nb, title, director, producer, release_date, opening_crawl 
					FROM ex02_movies 
					ORDER BY episode_nb
				"""
				)
				rows = cur.fetchall()
	except psycopg2.Error as e:
		message = str(e)
	if not rows:
		message = "No data available"

	roman_rows = []
	for row in rows:
		producer_names = row[3].split(", ")
		formatted_producers = "<br>".join(producer_names)
		roman_row = (to_roman(row[0]),) + row[1:3] + (formatted_producers,) + row[4:]
		roman_rows.append(roman_row)

	return render(
		request,
		"d05/templates/display.html",
		{
			"title": "SQL - Displaying a Table",
			"rows": roman_rows,
			"message": message,
		},
	)
