from elem import Elem, Text
from elements import (
	Html,
	Head,
	Body,
	Title,
	Meta,
	Img,
	Table,
	Th,
	Tr,
	Td,
	Ul,
	Ol,
	Li,
	H1,
	H2,
	P,
	Div,
	Span,
	Hr,
	Br,
	hex_to_256,
)


class Page:
	def __init__(self, elem: Elem):
		self.elem = elem

	def is_valid(self) -> bool:

		# Rule 1: Page must only contain the following types:
		# html, head, body, title, meta, img, table, th, tr,
		# td, ul, ol, li, h1, h2, p, div, span, hr, br or Text.
		if not isinstance(
			self.elem,
			(
				Html,
				Head,
				Body,
				Title,
				Meta,
				Img,
				Table,
				Th,
				Tr,
				Td,
				Ul,
				Ol,
				Li,
				H1,
				H2,
				P,
				Div,
				Span,
				Hr,
				Br,
				Text,
			),
		):
			return False

		# Rule 2: Html must strictly contain a Head, then a Body.
		if isinstance(self.elem, Html):
			content = self.elem.content
			if len(content) != 2:
				return False
			head_first = isinstance(content[0], Head)
			body_second = isinstance(content[1], Body)
			if not (head_first and body_second):
				return False

		# Rule 3: Head must only contain one Title and only one Title.
		if isinstance(self.elem, Head):
			content = self.elem.content
			if len(content) != 1:
				return False
			if not isinstance(content[0], Title):
				return False

		# Rule 4: Body and Div must only contain the following types:
		# H1, H2, Div, Table, Ul, Ol, Span, or Text.
		if isinstance(self.elem, (Body, Div)):
			content = self.elem.content
			for child in content:
				if not isinstance(child, (H1, H2, Div, Table, Ul, Ol, Span, Text)):
					return False

		# Rule 5: Title, H1, H2, Li, Th, Td must only contain one Text and only this Text.
		if isinstance(self.elem, (Title, H1, H2, Li, Th, Td)):
			content = self.elem.content
			if len(content) != 1:
				return False
			if not isinstance(content[0], Text):
				return False

		# Rule 6: P must only contain Text.
		if isinstance(self.elem, P):
			content = self.elem.content
			for child in content:
				if not isinstance(child, Text):
					return False

		# Rule 7: Span must only contain Text or some P.
		if isinstance(self.elem, Span):
			content = self.elem.content
			for child in content:
				if not isinstance(child, (Text, P)):
					return False

		# Rule 8: Ul and Ol must contain at least one Li and only some Li.
		if isinstance(self.elem, (Ul, Ol)):
			content = self.elem.content
			if len(content) < 1:
				return False
			for child in content:
				if not isinstance(child, Li):
					return False

		# Rule 9: Tr must contain at least one Th or Td and only some Th or Td.
		# The Th and the Td must be mutually exclusive.
		if isinstance(self.elem, Tr):
			content = self.elem.content
			if len(content) < 1:
				return False
			th, td = False, False
			for child in content:
				if not isinstance(child, (Th, Td)):
					return False
				if isinstance(child, Th):
					th = True
				if isinstance(child, Td):
					td = True
			if th and td:
				return False

		# Rule 10: Table must only contain Tr and only some Tr.
		if isinstance(self.elem, Table):
			content = self.elem.content
			for child in content:
				if not isinstance(child, Tr):
					return False
		return True

	def __str__(self):
		if self.is_valid():
			if isinstance(self.elem, Html):
				return "<!DOCTYPE html>\n" + str(self.elem)
			return str(self.elem)
		return ""

	def write_to_file(self, filename: str):
		with open(filename, "w") as f:
			f.write(str(self))


def print_status(page: Page, rule: int):
	if page.is_valid():
		print(f"{hex_to_256('#00FF00')}The page is valid (Rule {rule})\033[0m")
	else:
		print(f"{hex_to_256('#FF0000')}The page is invalid (Rule {rule})\033[0m")


if __name__ == "__main__":
	valid_cases = [
		(Page(Div()), 1),
		(Page(Html(content=[Head(), Body()])), 2),
		(Page(Head(content=[Title()])), 3),
		(Page(Body(content=[H1()])), 4),
		(Page(Title(content=[Text("Hello")])), 5),
		(Page(P(content=[Text("Hello")])), 6),
		(Page(Span(content=[Text("Hello")])), 7),
		(Page(Ul(content=[Li()])), 8),
		(Page(Tr(content=[Th()])), 9),
		(Page(Table(content=[Tr()])), 10),
	]
	invalid_cases = [
		(Page(Html()), 1),
		(Page(Html(content=[Body(), Head()])), 2),
		(Page(Head(content=[Div()])), 3),
		(Page(Body(content=[H1(), P()])), 4),
		(Page(Title(content=[Div()])), 5),
		(Page(P(content=[Div()])), 6),
		(Page(Span(content=[Div()])), 7),
		(Page(Ul(content=[Div()])), 8),
		(Page(Tr(content=[Th(), Td()])), 9),
		(Page(Table(content=[Div()])), 10),
	]
	for page, rule in valid_cases:
		print_status(page, rule)
	for page, rule in invalid_cases:
		print_status(page, rule)

	page = Page(
		Html(
			content=[
				Head(content=[Title(content=[Text("test")])]),
				Body(
					content=[
						H1(content=[Text("test")]),
						H2(content=[Text("test")]),
					]
				),
			],
		)
	)
	page.write_to_file("test.html")
	print(page)
