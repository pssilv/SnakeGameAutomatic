from scenario import Scenario
from snake import Snake

# Entities will be listeners too


class EntityBuilder():
    def __init__(self, rows, cols, snakeQ, fruitG):
        self._id_increaser = 0
        self._rows = rows
        self._cols = cols
        self._scenario = Scenario(rows, cols)
        self._entities = []

        # Variables to add the snakes
        self._addedSnakeEntity = 0
        self._finalSnakeEntiyAdded = snakeQ

        # Initializes the listeners and build the instances
        self.generate_available_positions()
        self.add_snake_entities()
        self.build_entities()

        # Loop for closing the window
        self._scenario._win.wait_for_close()

    def add_entity(self, entity):
        self._id_increaser += 1
        entity._id += self._id_increaser
        print(f"Snake {entity._id}")
        self._entities.append(entity)

    def remove_entity(self, entity):
        self._entities.remove(entity)

    def update_entity(self, event):
        pass

    def add_snake_entities(self):
        while self._addedSnakeEntity != self._finalSnakeEntiyAdded:
            self._addedSnakeEntity += 1
            self.add_entity(Snake(self))

    def generate_available_positions(self):
        self._available_positions = []

        for col in range(0, self._cols):
            for row in range(0, self._rows):
                self._available_positions.append((col, row))

    def del_choosed_position(self, position):
        pos = self._available_positions.index(position)
        del self._available_positions[pos]

    def build_entities(self):
        for snake_instance in self._entities:
            if isinstance(snake_instance, Snake):
                snake_instance.build()
                self.del_choosed_position(snake_instance._head_position)
