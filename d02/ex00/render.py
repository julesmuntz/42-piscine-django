import os
import sys
import settings


def render(filePath):
	if len(sys.argv) != 2:
		raise ValueError("Wrong number of arguments")
	if not os.path.exists(filePath):
		raise FileNotFoundError("File not found")
	if not filePath.endswith(".template"):
		raise ValueError("File must end with .template")
	with open(filePath, "r") as file:
		template = file.read()
	template = template.replace("{title}", settings.title)
	template = template.replace("{name}", settings.name)
	template = template.replace("{surname}", settings.surname)
	template = template.replace("{age}", settings.age)
	template = template.replace("{profession}", settings.profession)
	with open(filePath.replace(".template", ".html"), "w") as file:
		file.write(template)


if __name__ == "__main__":
	try:
		render(sys.argv[1])
	except Exception as e:
		print(e)
		sys.exit(1)
