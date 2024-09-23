import sys


def findCapitalCity(state: str):
    state = state.capitalize()
    states = {"Oregon": "OR", "Alabama": "AL", "New Jersey": "NJ", "Colorado": "CO"}
    capital_cities = {"OR": "Salem", "AL": "Montgomery", "NJ": "Trenton", "CO": "Denver"}
    if state in states:
        return capital_cities[states[state]]
    else:
        return "Unknown state"


if __name__ == "__main__":
    if len(sys.argv) == 2:
        print(findCapitalCity(sys.argv[1]))
