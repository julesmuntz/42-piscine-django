import requests
import sys


def request_wikipedia(query: str, country: str):
	response = requests.get(
		f"http://{country}.wikipedia.org/w/api.php?action=query&query=search&list=search&srsearch={query}&format=json"
	)
	if len(response.json()["query"]["search"]) == 0:
		return ""
	query = response.json()["query"]["search"][0]["title"]
	response = requests.get(
		f"http://{country}.wikipedia.org/w/api.php?action=query&prop=extracts&titles={query}&redirects=1&format=json&explaintext=1"
	)
	page_id = list(response.json()["query"]["pages"].keys())[0]
	if "extract" not in response.json()["query"]["pages"][page_id]:
		return ""
	result = f"{response.json()['query']['pages'][page_id]['title'].upper()}\n\n"
	result += f"{response.json()['query']['pages'][page_id]['extract']}"
	return result


if __name__ == "__main__":
	try:
		if len(sys.argv) != 3:
			print("Usage: python request_wikipedia.py <query> <country>")
			exit(1)
		if sys.argv[2].lower() not in ["en", "fr"]:
			print('Country must be "en" or "fr".')
			exit(1)
		result = request_wikipedia(sys.argv[1], sys.argv[2])
		if result == "":
			raise Exception('No results for "{sys.argv[1]}".')
		with open(f"{sys.argv[1].replace(' ', '_').lower()}.wiki", "w") as file:
			file.write(result)
	except Exception as e:
		print(e)
		exit(1)
