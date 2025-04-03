import os
import ast
import sys

MIGRATIONS_DIR = "ex00/migrations"


class RemoveFieldRemover(ast.NodeTransformer):
	def visit_ClassDef(self, node):
		if node.name == "Migration":
			for item in node.body:
				if isinstance(item, ast.Assign):
					# Check if 'operations' is being defined
					for target in item.targets:
						if isinstance(target, ast.Name) and target.id == "operations":
							# Assume it's a list
							new_elts = []
							for op in item.value.elts:
								if isinstance(op, ast.Call):
									# Handle different ways RemoveField can be called
									if isinstance(op.func, ast.Attribute):
										if op.func.attr == "RemoveField":
											print("Removing RemoveField operation")
											continue
									elif isinstance(op.func, ast.Name):
										if op.func.id == "RemoveField":
											print("Removing RemoveField operation")
											continue
								new_elts.append(op)
							item.value.elts = new_elts
		return self.generic_visit(node)


def remove_removefield_operations(migration_path):
	with open(migration_path, "r", encoding="utf-8") as file:
		try:
			tree = ast.parse(file.read())
		except SyntaxError as e:
			print(f"Syntax error in {migration_path}: {e}")
			return

	remover = RemoveFieldRemover()
	tree = remover.visit(tree)
	ast.fix_missing_locations(tree)

	# Write back only if changes were made
	new_content = ast.unparse(tree)
	with open(migration_path, "r", encoding="utf-8") as file:
		original_content = file.read()

	if new_content != original_content:
		with open(migration_path, "w", encoding="utf-8") as file:
			file.write(new_content)
		print(f"Updated {migration_path} to exclude RemoveField operations.")
	else:
		print(f"No RemoveField operations found in {migration_path}.")


def main():
	remove_fields = False
	if len(sys.argv) > 1 and sys.argv[1] == "make":
		remove_fields = True

	if not os.path.isdir(MIGRATIONS_DIR):
		print(f"Migrations directory '{MIGRATIONS_DIR}' does not exist.")
		sys.exit(1)

	migration_files = [
		f
		for f in os.listdir(MIGRATIONS_DIR)
		if f.endswith(".py") and not f.startswith("__")
	]

	if not migration_files:
		print(f"No migration files found in '{MIGRATIONS_DIR}'.")
	else:
		for filename in migration_files:
			migration_path = os.path.join(MIGRATIONS_DIR, filename)
			remove_removefield_operations(migration_path)

	if remove_fields:
		print("Running makemigrations...")
		result = os.system("python3 manage.py makemigrations")
		if result != 0:
			print("Error running makemigrations.")
			sys.exit(result)

	print("Running migrate...")
	result = os.system("python3 manage.py migrate")
	if result != 0:
		print("Error running migrate.")
		sys.exit(result)


if __name__ == "__main__":
	main()
