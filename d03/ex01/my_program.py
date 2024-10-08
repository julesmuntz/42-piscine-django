from local_lib.path import Path


def main():
	folder = Path("my_folder")
	if not folder.exists():
		folder.mkdir()
	file = Path("my_folder/my_file")
	if not file.exists():
		file.touch()
	file.write_text("something")
	print(file.read_text())


if __name__ == "__main__":
	try:
		main()
	except Exception as e:
		print(e)
		exit(1)
