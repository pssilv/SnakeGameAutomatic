from graphics import Window
from cell import Cell


class Scenario:
    def __init__(self, rows, cols):
        self._rows = rows
        self._cols = cols
        self._win = Window()

        self._resolution = self._win.get_display_size()
        self._width = self._resolution[0]
        self._height = self._resolution[1]

        # Optimzed for zoomed resolution
        self._x1 = (self._width * 99.048 / 100) * 5 / 100
        self._x2 = (self._width * 99.048 / 100) * 95 / 100
        self._y1 = (self._height * 91.666 / 100) * 5 / 100
        self._y2 = (self._height * 91.666 / 100) * 95 / 100

        self.build()

        self._win.wait_for_close()

    def build(self):
        self._area = Cell(self._win)
        self._area.draw(self._x1, self._y1, self._x2, self._y2)

        self.set_hitboxes()

    def set_hitboxes(self):
        cell_size = ((self._x2 - self._x1) / self._rows)  # The offset should works here too
        cell_col_size = ((self._y2 - self._y1) / self._cols)  # The offset should works here too

        total_cells = []

        for cell_col in range(self._cols):

            cell_set = []

            for cell in range(self._rows):
                cell_set.append(Cell(self._win))
                self._win.redraw()

            total_cells.append(cell_set)

        y1 = self._y1
        y2 = cell_col_size + self._y1  # Small issue because here the offset only works here

        for cell_col in total_cells:

            x1, x2 = self._x1, cell_size + self._x1  # Small issue here because the offset only works here

            for cell in cell_col:
                cell.draw(x1, y1, x2, y2)
                print(cell._x1, cell._y1, cell._x2, cell._y2)

                if cell != cell_col[-1]:
                    x1, x2 = x1 + cell_size, x2 + cell_size

            y1, y2 = y1 + cell_col_size, y2 + cell_col_size
