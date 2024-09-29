class HotBeverage:
	def __init__(self):
		self.name = "hot beverage"
		self.price = 0.3

	def description(self) -> str:
		return "Just some hot water in a cup."

	def __str__(self) -> str:
		return f"name: {self.name}\nprice: {self.price:.2f}\ndescription: {self.description()}"


class Coffee(HotBeverage):
	def __init__(self):
		self.name = "coffee"
		self.price = 0.4

	def description(self) -> str:
		return "A coffee, to stay awake."

	def __str__(self) -> str:
		return f"{hex_to_256('#A88A64')}{super().__str__()}\033[0m"


class Tea(HotBeverage):
	def __init__(self):
		super().__init__()
		self.name = "tea"

	def __str__(self) -> str:
		return f"{hex_to_256('#929B74')}{super().__str__()}\033[0m"


class Chocolate(HotBeverage):
	def __init__(self):
		self.name = "chocolate"
		self.price = 0.5

	def description(self) -> str:
		return "Chocolate, sweet chocolate..."

	def __str__(self) -> str:
		return f"{hex_to_256('#B5774D')}{super().__str__()}\033[0m"


class Cappuccino(HotBeverage):
	def __init__(self):
		self.name = "cappuccino"
		self.price = 0.45

	def description(self) -> str:
		return "Un po' di Italia nella sua tazza!"

	def __str__(self) -> str:
		return f"{hex_to_256('#C1AA8B')}{super().__str__()}\033[0m"


def hex_to_256(hex_color: str) -> str:
	hex_color = hex_color.lstrip("#")
	r = int(hex_color[0:2], 16)
	g = int(hex_color[2:4], 16)
	b = int(hex_color[4:6], 16)
	return f"\033[1;38;2;{r};{g};{b}m"


if __name__ == "__main__":
	try:
		print(HotBeverage())
		print(Coffee())
		print(Tea())
		print(Chocolate())
		print(Cappuccino())
	except Exception as e:
		print(e)
