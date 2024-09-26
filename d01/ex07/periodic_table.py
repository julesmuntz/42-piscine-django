import sys


class Element:
	def __init__(self, name, position, number, small, molar, electron):
		self.name = name
		self.position = position
		self.number = number
		self.small = small
		self.molar = molar
		self.electron = electron


def parseElementData(line):
	name, data = line.split(" = ", 1)
	column = data.split(", ")

	position = int(column[0].split(":")[1])
	number = int(column[1].split(":")[1])
	small = column[2].split(": ")[1]
	molar = float(column[3].split(":")[1])
	electron = list(map(int, column[4].split(":")[1].split()))

	return Element(name, position, number, small, molar, electron)


def periodicTable():
	table = []
	try:
		with open("periodic_table.txt", "r") as file:
			for line in file:
				element = parseElementData(line.strip())
				table.append(element)
	except FileNotFoundError:
		return []
	return table


def generateHTMLTable(elements):
	html = """<!DOCTYPE html>
<html lang="en">

<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title>Periodic Table</title>
	<link rel="stylesheet" href="periodic_table.css">
</head>

<body>"""

	html += "\n<table border='1'>\n<tr>"

	i = 0
	for element in elements:
		while i < element.position:
			html += "<td></td>"
			i += 1
		if i > 17:
			html += "</tr>\n<tr>"
			i = 0
		html += f"<td><b>{element.name}</b><br>{element.small}<br>{element.number}</td>"
		i += 1

	html += """</tr>
</table>
</body>

</html>"""

	return html


def generateCSSTable():
	css = """table {
	border-collapse: collapse;
	width: 100%;
}

td {
	border: 1px solid black;
	padding: 10px;
	text-align: center;
	vertical-align: top;
}

h4 {
	margin: 0;
	font-size: 1.2em;
}

ul {
	list-style-type: none;
	padding: 0;
	margin: 0;
}

ul li {
	margin: 5px 0;
}"""
	return css


if __name__ == "__main__":
	elements = periodicTable()
	if not elements:
		print("periodic_table.txt not found")
		sys.exit(1)
	html_table = generateHTMLTable(elements)
	with open("periodic_table.html", "w") as file:
		file.write(html_table)
	css_table = generateCSSTable()
	with open("periodic_table.css", "w") as file:
		file.write(css_table)
