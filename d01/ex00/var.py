def my_var():
    print(f"42 has type of {type(42)}")
    print(f"42 has type of {type("42")}")
    print(f"quarante-deux has type of {type("quarante-deux")}")
    print(f"42.0 has type of {type(42.0)}")
    print(f"True has type of {type(True)}")
    print(f"[42] has type of {type([42])}")
    print(f"{{42: 42}} has type of {type({42: 42})}")
    print(f"(42,) has type of {type((42,))}")
    print(f"set() has type of {type(set())}")
    return


if __name__ == "__main__":
    my_var()
