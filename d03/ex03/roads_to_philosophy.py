from bs4 import BeautifulSoup
import requests
import sys


def get_wikipedia_page(query: str):
	if not query:
		return ""
	page = requests.get(f"https://en.wikipedia.org/wiki/{query}")
	if page.status_code != 200:
		page = requests.get(f"https://fr.wikipedia.org/wiki/{query}")
	if page.status_code != 200:
		return ""
	soup = BeautifulSoup(page.content, "html.parser")
	return soup


def find_first_link(query: str, visited: set):
	soup = get_wikipedia_page(query)
	if not soup:
		return ""
	content_div = soup.find("div", class_="mw-content-ltr mw-parser-output")
	title_span = soup.find("h1", id="firstHeading")
	print(title_span.text)
	for paragraph in content_div.find_all(
		["p", "ul", "ol", "li", "dl", "dt"], recursive=False
	):
		for skip in paragraph.find_all(
			["sup", "span", "table", "h1", "h2", "h3", "h4", "h5", "h6"]
		):
			skip.decompose()
		for link in paragraph.find_all("a", href=True):
			if link["href"].startswith("/wiki/Help:"):
				continue
			link_title = link["href"].split("/")[-1].replace("_", " ")
			if link_title not in visited:
				return link_title
	return ""


def roads_to_philosophy(query: str):
	visited = set()
	query = query.replace(" ", "_").title()
	soup = get_wikipedia_page(query)
	if not soup:
		return ""
	title_span = soup.find("h1", id="firstHeading")
	query = title_span.text
	count = 0
	while query not in visited:
		visited.add(query)
		query = find_first_link(query, visited)
		if not query:
			raise Exception(f'No results for "{query}".')
		count += 1
		if query == "Philosophy":
			print(query)
			print(f"{count} roads from {title_span.text} to philosophy !")
			return query
	if query in visited:
		raise Exception("It leads to an infinite loop !")
	return ""


if __name__ == "__main__":
	try:
		if len(sys.argv) != 2:
			print("Usage: python roads_to_philosophy.py <query>")
			exit(1)
		result = roads_to_philosophy(sys.argv[1])
		if result == "":
			raise Exception("It leads to a dead end !")
	except Exception as e:
		print(e)
		exit(1)
