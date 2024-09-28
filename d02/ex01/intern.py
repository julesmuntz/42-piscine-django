class Intern:
	def __init__(self, name: str = "My name? I'm intern_1, an intern, I have no name."):
		self.Name = name

	def __str__(self) -> str:
		return self.Name

	class Coffee:
		def __str__(self) -> str:
			return "This is the worst coffee you ever tasted."

	def work(self):
		raise Exception("I'm just an intern, I can't do that...")

	def make_coffee(self) -> Coffee:
		return self.Coffee()


if __name__ == "__main__":
	try:
		intern_1 = Intern()
		print(f"Name? {intern_1}")
		intern_2 = Intern("Mark")
		print(f"Name? {intern_2}.")
		coffee = intern_2.make_coffee()
		print(
			f"{intern_2}, don't make me fire you. {str(coffee).replace('you', 'I have')}"
		)
		intern_1.work()
	except Exception as e:
		print(e)
