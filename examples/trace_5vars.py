from py_espresso.cube import Cube


def main():
    cube = Cube.from_minterm(5, n=5)

    print("Initial cube:")
    print(cube)
    print()

    cube = cube.expand_var(0)
    print("Expand x0:")
    print(cube)
    print()

    cube = cube.expand_var(1)
    print("Expand x1:")
    print(cube)
    print()

    print("Statistics:")
    print(f"literals = {cube.literal_count()}")
    print(f"dimension = {cube.dimension()}")
    print(f"size = {cube.size()}")


if __name__ == "__main__":
    main()
