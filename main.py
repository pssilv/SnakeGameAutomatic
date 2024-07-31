import sys
sys.path.append("./game_files/")

from gamelogic import SnakeGame


def main():
    print("===== Configs =====")
    print("Map size")
    rows = int(input("Rows: "))
    cols = int(input("Cols: "))
    if rows * cols <= 0:
        raise Exception("available_slots is equal or less than 0")
    available_slots = rows * cols

    print("-------------------")
    print(f"You have {available_slots} positions for generating snakes")
    snakes = int(input("Snake quantity: "))

    if snakes > available_slots or snakes == 0:
        raise Exception("Snake quantity is higher than available slots or zero")

    available_slots -= snakes

    if available_slots == 0:
        raise Exception("Snake quantity has occupied all slots and theres no more slots for fruits")

    print(f"You have: {available_slots} positions for generating fruits")
    fruits = int(input("Fruit generators quantity: "))

    if fruits > available_slots or fruits == 0:
        raise Exception("Fruits generators quantity is higher than available slots or zero")

    print("-------------------")

    SnakeGame(rows, cols, snakes, fruits)


main()
