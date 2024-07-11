import random


class Snake():
    def __init__(self, entity_builder):
        #  Snake attributes
        self._head_position = None
        self._body_size = None
        self._id = 0
        #  game attributes
        self._entity_builder = entity_builder
        self._scenario = entity_builder._scenario
        #  snake events
        self._isDead = False
        self._eatedFruit = False

    def generate_position(self):
        self.last_col = len(self._scenario._total_cells) - 1
        self.last_row = len(self._scenario._total_cells[0]) - 1

        self._head_position = random.choice(
            self._entity_builder._available_positions
        )
        print(self._head_position)
