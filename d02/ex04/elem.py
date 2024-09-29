class Elem:
	def __init__(self, tag="div", attr={}, content=None, tag_type="double"):
		self.tag = tag
		self.attr = attr
		self.content = []
		self.level = 0
		if tag_type not in ["double", "simple"]:
			raise self.ValidationError("Type must be 'double' or 'simple'")
		self.tag_type = tag_type
		if content is not None:
			if self.tag_type == "simple":
				raise self.ValidationError("Simple tags cannot have content")
			self.add_content(content)

	def __str__(self):
		if self.tag_type == "double":
			result = "  " * self.level
			result += "<" + self.tag + self.__make_attr() + ">"
			result += self.__make_content()
			if len(self.content) > 0:
				result += "  " * self.level
			result += "</" + self.tag + ">"
		elif self.tag_type == "simple":
			result = "  " * self.level
			result += "<" + self.tag + self.__make_attr() + " />"
		return result

	def __make_attr(self):
		result = ""
		for pair in sorted(self.attr.items()):
			result += " " + str(pair[0]) + '="' + str(pair[1]) + '"'
		return result

	def __make_content(self):
		if len(self.content) == 0:
			return ""
		result = "\n"
		level = self.level + 1
		for elem in self.content:
			elem.level = level
			if isinstance(elem, Text):
				result += f"{'  ' * level}{elem}\n"
			else:
				result += f"{elem}\n"
				if elem.tag == "double":
					level += 1
		return result

	def add_content(self, content):
		if not Elem.check_type(content):
			raise Elem.ValidationError
		if type(content) is list:
			self.content += [elem for elem in content if elem != Text("")]
		elif content != Text(""):
			self.content.append(content)

	@staticmethod
	def check_type(content):
		return (
			isinstance(content, Elem)
			or type(content) is Text
			or (
				type(content) is list
				and all(
					[type(elem) is Text or isinstance(elem, Elem) for elem in content]
				)
			)
		)

	class ValidationError(Exception):
		def __init__(self, message="Validation error"):
			self.message = message
			super().__init__(self.message)


class Text(str):
	def __str__(self):
		return (
			super()
			.__str__()
			.replace("<", "&lt;")
			.replace(">", "&gt;")
			.replace('"', "&quot;")
			.replace("\n", "\n<br />\n")
		)


if __name__ == "__main__":
	try:
		elem = Elem(
			tag="html",
			tag_type="double",
			content=[
				Elem(
					tag="head",
					tag_type="double",
					content=[
						Elem(
							tag="title",
							tag_type="double",
							content=[Text("Hello ground!")],
						)
					],
				),
				Elem(
					tag="body",
					tag_type="double",
					content=[
						Elem(
							tag="h1",
							tag_type="double",
							content=[Text("Oh no, not again!")],
						),
						Elem(
							tag="img",
							tag_type="simple",
							attr={"src": "http://i.imgur.com/pfp3T.jpg"},
						),
					],
				),
			],
		)
		print(elem)
	except Elem.ValidationError as e:
		print(e)
