from django.shortcuts import render
import string


def color(r, g, b, index):
	result = f"rgb(	{int(r * (1 - index / 50))},\
					{int(g * (1 - index / 50))},\
					{int(b * (1 - index / 50))})"
	return result


def table():
	result = """
	<table>
		<tr style="color: white; text-align: center; height: 40px; width: 80px">
			<th style="color: black; text-align: right">1</th>
			<th style="background-color: rgb(55, 55, 55)">a</th>
			<th style="background-color: rgb(255, 0, 0)">a</th>
			<th style="background-color: rgb(0, 0, 255)">a</th>
			<th style="background-color: rgb(0, 128, 0)">a</th>
		</tr>
	"""

	alphabet = list(string.ascii_letters)[1:-1]

	for i, letter in enumerate(alphabet, start=2):
		result += f"""
		<tr style="color: white; text-align: center; height: 40px; width: 80px">
			<th style="color: black; text-align: right">{i}</th>
		"""
		columns = [
			{"style": f"background-color: {color(55, 55, 55, i)}"},
			{"style": f"background-color: {color(255, 0, 0, i)}"},
			{"style": f"background-color: {color(0, 0, 255, i)}"},
			{"style": f"background-color: {color(0, 128, 0, i)}"},
		]
		for column in columns:
			result += f'<td style="{column["style"]}">{letter}</td>'
		result += "</tr>"
	result += "</table>"
	return result


def page(request):
	context = {"table": table}
	return render(request, "ex03/templates/table.html", context)
