import sys


def get_states():
    return {"Oregon": "OR", "Alabama": "AL", "New Jersey": "NJ", "Colorado": "CO"}


def get_capital_cities():
    return {"OR": "Salem", "AL": "Montgomery", "NJ": "Trenton", "CO": "Denver"}


def to_lowercase_dict(d: dict):
    return {k.lower(): v.lower() for k, v in d.items()}


def find_capital_city(state: str):
    states = get_states()
    capital_cities = get_capital_cities()
    states_lower = to_lowercase_dict(states)

    state = state.lower()
    if state in states_lower:
        abbreviation = states_lower[state]
        return capital_cities[abbreviation.upper()]
    else:
        return None


def find_state(capital_city: str):
    states = get_states()
    capital_cities = get_capital_cities()
    capital_cities_lower = to_lowercase_dict(capital_cities)

    capital_city = capital_city.lower()
    if capital_city in capital_cities_lower.values():
        for state, abbreviation in states.items():
            if capital_cities_lower[abbreviation.lower()] == capital_city:
                return state
    else:
        return None


def all_in(arg: str):
    arguments = [word.strip() for word in arg.split(",") if word.strip()]
    for arg in arguments:
        capital_city = find_capital_city(arg)
        state = find_state(arg)
        if capital_city:
            print(f"{capital_city} is the capital of {find_state(capital_city)}")
        elif state:
            print(f"{find_capital_city(state)} is the capital of {state}")
        else:
            print(f"{arg} is neither a capital city nor a state")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        all_in(sys.argv[1])
