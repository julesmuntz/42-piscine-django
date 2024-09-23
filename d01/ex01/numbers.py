def printNumbers():
    try:
        numbers = open("numbers.txt").read().split(",")
    except FileNotFoundError:
        print("File not found")
        return
    for number in numbers:
        print(number)
    return


if __name__ == "__main__":
    printNumbers()
