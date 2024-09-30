from elem import Elem, Text


class Html(Elem):
	def __init__(self, content=None, attr={}):
		super().__init__("html", attr, content, "double")


class Body(Elem):
	def __init__(self, content=None, attr={}):
		super().__init__("body", attr, content, "double")


class Head(Elem):
	def __init__(self, content=None, attr={}):
		super().__init__("head", attr, content, "double")


class Title(Elem):
	def __init__(self, content=None, attr={}):
		super().__init__("title", attr, content, "double")


class Meta(Elem):
	def __init__(self, content=None, attr={}):
		super().__init__("meta", attr, content, "simple")


class Img(Elem):
	def __init__(self, content=None, attr={}):
		super().__init__("img", attr, content, "simple")


class Table(Elem):
	def __init__(self, content=None, attr={}):
		super().__init__("table", attr, content, "double")


class Th(Elem):
	def __init__(self, content=None, attr={}):
		super().__init__("th", attr, content, "double")


class Tr(Elem):
	def __init__(self, content=None, attr={}):
		super().__init__("tr", attr, content, "double")


class Td(Elem):
	def __init__(self, content=None, attr={}):
		super().__init__("td", attr, content, "double")


class Ul(Elem):
	def __init__(self, content=None, attr={}):
		super().__init__("ul", attr, content, "double")


class Ol(Elem):
	def __init__(self, content=None, attr={}):
		super().__init__("ol", attr, content, "double")


class Li(Elem):
	def __init__(self, content=None, attr={}):
		super().__init__("li", attr, content, "double")


class H1(Elem):
	def __init__(self, content=None, attr={}):
		super().__init__("h1", attr, content, "double")


class H2(Elem):
	def __init__(self, content=None, attr={}):
		super().__init__("h2", attr, content, "double")


class P(Elem):
	def __init__(self, content=None, attr={}):
		super().__init__("p", attr, content, "double")


class Div(Elem):
	def __init__(self, content=None, attr={}):
		super().__init__("div", attr, content, "double")


class Span(Elem):
	def __init__(self, content=None, attr={}):
		super().__init__("span", attr, content, "double")


class Hr(Elem):
	def __init__(self, content=None, attr={}):
		super().__init__("hr", attr, content, "simple")


class Br(Elem):
	def __init__(self, content=None, attr={}):
		super().__init__("br", attr, content, "simple")


def hex_to_256(hex_color: str) -> str:
	hex_color = hex_color.lstrip("#")
	r = int(hex_color[0:2], 16)
	g = int(hex_color[2:4], 16)
	b = int(hex_color[4:6], 16)
	return f"\033[38;2;{r};{g};{b}m"


if __name__ == "__main__":
	elements = (
		Html(),
		Head(),
		Body(),
		Title(),
		Meta(),
		Img(),
		Table(),
		Th(),
		Tr(),
		Td(),
		Ul(),
		Ol(),
		Li(),
		H1(),
		H2(),
		P(),
		Div(),
		Span(),
		Hr(),
		Br(),
	)
	print(f"{hex_to_256('#c5976a')}Default elements:")
	for elem in elements:
		print(elem)
	print("\033[0m")

	elements_with_content = (
		Html(content=[Text("42")]),
		Head(content=[Text("42")]),
		Body(content=[Text("42")]),
		Title(content=[Text("42")]),
		Meta(),
		Img(),
		Table(content=[Text("42")]),
		Th(content=[Text("42")]),
		Tr(content=[Text("42")]),
		Td(content=[Text("42")]),
		Ul(content=[Text("42")]),
		Ol(content=[Text("42")]),
		Li(content=[Text("42")]),
		H1(content=[Text("42")]),
		H2(content=[Text("42")]),
		P(content=[Text("42")]),
		Div(content=[Text("42")]),
		Span(content=[Text("42")]),
		Hr(),
		Br(),
	)
	print(f"{hex_to_256('#6aa7c5')}Elements with content:")
	for elem in elements_with_content:
		print(elem)
	print("\033[0m")

	elements_with_attr = (
		Html(attr={"class": "html,", "lang": "en"}),
		Head(attr={"class": "head"}),
		Body(attr={"class": "body"}),
		Title(attr={"class": "title"}),
		Meta(attr={"class": "meta"}),
		Img(attr={"class": "img"}),
		Table(attr={"class": "table"}),
		Th(attr={"class": "th"}),
		Tr(attr={"class": "tr"}),
		Td(attr={"class": "td"}),
		Ul(attr={"class": "ul"}),
		Ol(attr={"class": "ol"}),
		Li(attr={"class": "li"}),
		H1(attr={"class": "h1"}),
		H2(attr={"class": "h2"}),
		P(attr={"class": "p"}),
		Div(attr={"class": "div"}),
		Span(attr={"class": "span"}),
		Hr(attr={"class": "hr"}),
		Br(attr={"class": "br"}),
	)
	print(f"{hex_to_256('#6a6dc5')}Elements with attributes:")
	for elem in elements_with_attr:
		print(elem)
	print("\033[0m")

	elements_with_content_and_attr = (
		Html(content=[Text("42")], attr={"class": "html"}),
		Head(content=[Text("42")], attr={"class": "head"}),
		Body(content=[Text("42")], attr={"class": "body"}),
		Title(content=[Text("42")], attr={"class": "title"}),
		Meta(attr={"class": "meta"}),
		Img(attr={"class": "img"}),
		Table(content=[Text("42")], attr={"class": "table"}),
		Th(content=[Text("42")], attr={"class": "th"}),
		Tr(content=[Text("42")], attr={"class": "tr"}),
		Td(content=[Text("42")], attr={"class": "td"}),
		Ul(content=[Text("42")], attr={"class": "ul"}),
		Ol(content=[Text("42")], attr={"class": "ol"}),
		Li(content=[Text("42")], attr={"class": "li"}),
		H1(content=[Text("42")], attr={"class": "h1"}),
		H2(content=[Text("42")], attr={"class": "h2"}),
		P(content=[Text("42")], attr={"class": "p"}),
		Div(content=[Text("42")], attr={"class": "div"}),
		Span(content=[Text("42")], attr={"class": "span"}),
		Hr(attr={"class": "hr"}),
		Br(attr={"class": "br"}),
	)
	print(f"{hex_to_256('#c56a6a')}Elements with content and attributes:")
	for elem in elements_with_content_and_attr:
		print(elem)
	print("\033[0m")
