import random
from color_set import pick_random_color


class Snake():
    def __init__(self, entity_manager):
        #  Snake attributes
        self._head_position = None
        self._body_parts_pos = []
        self._color = None
        self._eyes_color = None
        self._id = 0
        #  game attributes
        self._entity_manager = entity_manager
        self._scenario = entity_manager._scenario
        #  Snake events
        self._isDead = False
        self._eatedFruit = False
        # Snake moving algorithm
        self._path_to_fruit = []

    def generate_attributes(self):
        self._head_position = random.choice(
            self._entity_manager._available_positions
        )

        self._color = pick_random_color()
        self._eyes_color = pick_random_color()


class Fruit():
    def __init__(self, entity_manager):
        # Fruit attributes
        self._pos = None
        self._color = None
        self._id = 0

        # game attributes
        self._entity_manager = entity_manager
        self._scenario = entity_manager._scenario

        # Fruit events
        self._isEated = False

    def generate_attributes(self):
        self._pos = random.choice(
            self._entity_manager._available_positions
        )

        self._color = "white"
