import sys


def findState(capital_city: str):
    capital_city = capital_city.capitalize()
    states = {"Oregon": "OR", "Alabama": "AL", "New Jersey": "NJ", "Colorado": "CO"}
    capital_cities = {"OR": "Salem", "AL": "Montgomery", "NJ": "Trenton", "CO": "Denver"}
    if capital_city in capital_cities.values():
        for state, abbreviation in states.items():
            if capital_cities[abbreviation] == capital_city:
                return state
    else:
        return "Unknown capital city"


if __name__ == "__main__":
    if len(sys.argv) == 2:
        print(findState(sys.argv[1]))
