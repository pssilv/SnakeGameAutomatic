from snake import Snake

# Entities will be listeners too


class EntityManager():
    def __init__(self, rows, cols, snakeQ, fruitG, game_logic):
        # Scenario attributes
        self._rows = rows
        self._cols = cols
        self._scenario = game_logic._scenario

        # Available entities: snake, fruit
        self._id_increaser = 0
        self._entities = []

        # Methods to generate positions and add entities
        self.generate_available_positions()
        self.add_entity(Snake(self), snakeQ)
        self.build_entities()

    def add_entity(self, entity, quantity):
        for i in range(0, quantity):
            self._id_increaser += 1
            entity._id = self._id_increaser

            print(f"{type(entity).__name__} {entity._id}")
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
        col = entity._head_position[0]
        row = entity._head_position[1]

        entity_cell = self._scenario._total_cells[col][row]

        factor_x = self._scenario._cell_size / 4
        factor_y = self._scenario._cell_col_size / 4
        x1 = entity_cell._x1 + factor_x
        y1 = entity_cell._y1 + factor_y
        x2 = entity_cell._x2 - factor_x
        y2 = entity_cell._y2 - factor_y
        print(x1)
        print(y1)
        print(x2)
        print(y2)

        entity_cell.draw(x1, y1, x2, y2)
        self._scenario._win.redraw()

    def build_entities(self):
        for snake_instance in self._entities:
            if isinstance(snake_instance, Snake):
                snake_instance.generate_position()
                self.del_choosed_position(snake_instance._head_position)
                self.draw_entity(snake_instance)
