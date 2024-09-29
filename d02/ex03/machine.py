from beverages import HotBeverage, Coffee, Tea, Cappuccino, Chocolate
import random


class CoffeeMachine:
	def __init__(self):
		self.servings = 10

	class EmptyCup(HotBeverage):
		def __init__(self):
			self.name = "empty cup"
			self.price = 0.9

		def description(self) -> str:
			return "An empty cup?! Gimme my money back!"

	class BrokenMachineException(Exception):
		def __init__(self):
			super().__init__("This coffee machine has to be repaired.")

	def repair(self):
		self.servings = 10

	def serve(self, beverage: HotBeverage):
		if self.servings <= 0:
			raise self.BrokenMachineException()
		self.servings -= 1
		return beverage()


if __name__ == "__main__":
	coffeeMachine = CoffeeMachine()
	for i in range(10):
		print(f"[ORDER {i + 1} - {coffeeMachine.servings} servings left]")
		try:
			print(
				f"{coffeeMachine.serve(random.choice([Coffee, Tea, Cappuccino, Chocolate]))}"
			)
		except CoffeeMachine.BrokenMachineException as e:
			print(f"error: {e}")
			coffeeMachine.repair()
		print()
