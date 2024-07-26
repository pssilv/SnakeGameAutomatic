import sys
sys.path.append("./game_files/")

from gamelogic import SnakeGame


def main():
    print("===== Configs =====")
    print("Map size")
    rows = int(input("Rows: "))
    cols = int(input("Cols: "))
    available_slots = rows * cols

    print("-------------------")
    print(f"You have {available_slots} positions for generating snakes")
    snakes = int(input("Snake quantity: "))

    if snakes > available_slots:
        print("The snake quantity is higher than available positions")
        snakes = int(input("Snake quantity: "))

    available_slots -= snakes

    print(f"You have: {available_slots} positions for generating fruits")
    fruits = int(input("Fruit generators quantity: "))

    if fruits > available_slots:
        print("The fruit generators quantity is higher than available positions")
        fruits = int(input("Fruit generators quantity: "))

    print("-------------------")

    SnakeGame(rows, cols, snakes, fruits)


main()
