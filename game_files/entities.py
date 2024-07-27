import random
from color_set import pick_random_color


class Snake():
    def __init__(self, entity_manager):
        #  Snake attributes
        self._head_position = (None, None)
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
        self._past_movement = (None, None)
        self._past_polygons = None

        self._available_paths = []
        self._direction = None

    def generate_attributes(self):
        self._head_position = random.choice(
            self._scenario._available_positions
        )

        self._color = pick_random_color()
        self._eyes_color = pick_random_color()


class Fruit():
    def __init__(self, entity_manager):
        # Fruit attributes
        self._pos = None
        self._color = None
        self._id = 0

        self._past_polygons = None

        # game attributes
        self._entity_manager = entity_manager
        self._scenario = entity_manager._scenario

    def generate_attributes(self):
        self._pos = random.choice(
            self._scenario._available_positions
        )

        self._color = "white"
