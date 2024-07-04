from graphics import Line, Point


class Cell:
    def __init__(self, win):
        self.has_right_wall = True
        self.has_bottom_wall = True
        self.has_left_wall = True
        self.has_top_wall = True
        self._has_collision = False
        self._x1 = None
        self._y1 = None
        self._x2 = None
        self._y2 = None
        self._win = win

    def draw(self, x1, y1, x2, y2):
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2

        if self.has_right_wall:

            self._win.draw_line(Line(
                Point(self._x2, self._y1), Point(self._x2, self._y2))
            )

        if self.has_bottom_wall:

            self._win.draw_line(Line(
                Point(self._x1, self._y2), Point(self._x2, self._y2))
            )

        if self.has_left_wall:

            self._win.draw_line(Line(
                Point(self._x1, self._y1), Point(self._x1, self._y2))
            )

        if self.has_top_wall:

            self._win.draw_line(Line(
                Point(self._x1, self._y1), Point(self._x2, self._y1))
            )
