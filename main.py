import sys
sys.path.append("./game_files/")

from entitybuilder import EntityBuilder


def main():
    print("===== Configs =====")
    print("Map size")
    rows = int(input("Rows: "))
    cols = int(input("Cols: "))
    available_slots = rows * cols

    print("-------------------")
    print(f"You have {available_slots} positions for generating snakes")
    snakes = int(input("Snake quantity: "))
    fruits = int(input("Fruit generators quantity: "))
    print("-------------------")

    if snakes > available_slots:
        print("The snake quantity is higher than available positions")
        snakes = int(input("Snake quantity: "))

    EntityBuilder(rows, cols, snakes, fruits)


main()
