from entities import Snake, Fruit
from cell import Cell
# Entities will be listeners too


class EntityManager():
    def __init__(self, rows, cols, snakeQ, fruitG, game_logic):
        # Scenario attributes
        self._rows = rows
        self._cols = cols
        self._scenario = game_logic._scenario

        # Available entities: snake, fruit
        self._id_increaser = 0
        self._total_ids = 0
        self._entities_ids = {}
        self._entities = []

        # Methods to generate positions and add entities
        self.generate_available_positions()
        self.add_entity(Snake, snakeQ)
        self.add_entity(Fruit, fruitG)
        self.build_entities()
        self.display_entities_data()

    def add_entity(self, entity_type, quantity):
        entity_name = type(entity_type(self)).__name__
        self._entities_ids[entity_name] = 0

        for i in range(0, quantity):
            entity = entity_type(self)

            self._id_increaser += 1
            entity._id = self._id_increaser
            self._total_ids += 1

            self._entities.append(entity)

    def remove_entity(self, entity):
        self._entities.remove(entity)

    def update_entity(self, event):
        pass

    def generate_available_positions(self):
        self._available_positions = []

        for col in range(0, self._cols):
            for row in range(0, self._rows):
                self._available_positions.append((col, row))

    def del_choosed_position(self, position):
        pos = self._available_positions.index(position)
        del self._available_positions[pos]

    def draw_entity(self, entity):
        if isinstance(entity, Snake):
            col = entity._head_position[0]
            row = entity._head_position[1]

        elif isinstance(entity, Fruit):
            col = entity._pos[0]
            row = entity._pos[1]

        entity_assigned_cell = self._scenario._total_cells[col][row]
        entity_cell = Cell(self._scenario._win)

        factor_x = self._scenario._cell_size / 8
        factor_y = self._scenario._cell_col_size / 8

        x1 = entity_assigned_cell._x1 + factor_x
        y1 = entity_assigned_cell._y1 + factor_y
        x2 = entity_assigned_cell._x2 - factor_x
        y2 = entity_assigned_cell._y2 - factor_y

        entity_cell.draw(x1, y1, x2, y2)
        entity_cell.generate_color([x1, y1, x2, y2], entity._color)
        self._scenario._win.redraw()

        eyes_drawed = False

        if isinstance(entity, Snake) and eyes_drawed is False:
            entity_cell.draw_eyes(entity._eyes_color)
            self._scenario._win.redraw()
            eyes_drawed = True

    def build_entities(self):
        for entity_instance in self._entities:
            self._entities_ids[type(entity_instance).__name__] += 1
            id = self._entities_ids[type(entity_instance).__name__]

            if isinstance(entity_instance, Snake):
                entity_instance.generate_attributes()

                self.del_choosed_position(entity_instance._head_position)
                self.draw_entity(entity_instance)

                position = entity_instance._head_position
                print(f"Snake {id} generated at {position}")

            elif isinstance(entity_instance, Fruit):
                entity_instance.generate_attributes()

                self.del_choosed_position(entity_instance._pos)
                self.draw_entity(entity_instance)

                position = entity_instance._pos
                print(f"Fruit {id} generated at {position}")

    def display_entities_data(self):
        print("===== Entities data =====")
        for entity_key in self._entities_ids:
            print(f"total {entity_key}s: {self._entities_ids[entity_key]}")

        print(f"Total entities: {self._total_ids}")
        print("-------------------")
