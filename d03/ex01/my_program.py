from path import Path


def main():
	path = Path("my_script.sh")
	print(path.read_text())


if __name__ == "__main__":
	main()
