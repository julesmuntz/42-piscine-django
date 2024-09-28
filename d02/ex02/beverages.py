class HotBeverage:
	def __init__(self):
		self.name = "hot beverage"
		self.price = 0.3

	def description(self) -> str:
		return "Just some hot water in a cup."

	def __str__(self) -> str:
		return f"name: {self.name}\nprice: {self.price:.2f}\ndescription: {self.description()}\n"


class Coffee(HotBeverage):
	def __init__(self):
		self.name = "coffee"
		self.price = 0.4

	def description(self) -> str:
		return "A coffee, to stay awake."


class Tea(HotBeverage):
	def __init__(self):
		super().__init__()
		self.name = "tea"


class Chocolate(HotBeverage):
	def __init__(self):
		self.name = "chocolate"
		self.price = 0.5

	def description(self) -> str:
		return "Chocolate, sweet chocolate..."


class Cappuccino(HotBeverage):
	def __init__(self):
		self.name = "cappuccino"
		self.price = 0.45

	def description(self) -> str:
		return "Un po' di Italia nella sua tazza!"


if __name__ == "__main__":
	try:
		print(HotBeverage())
		print(Coffee())
		print(Tea())
		print(Chocolate())
		print(Cappuccino())
	except Exception as e:
		print(e)
