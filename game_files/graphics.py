from tkinter import Tk, BOTH, Canvas
import ctypes


try:  # Windows 8.1 and later
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except Exception as e:
    pass
try:  # Before Windows 8.1
    ctypes.windll.user32.SetProcessDPIAware()
except:  # Windows 8 or before
    pass


class Window:
    def __init__(self):
        self.__root = Tk()
        self.__height = self.__root.winfo_screenheight()
        self.__width = self.__root.winfo_screenwidth()
        self.__root.title("Snake Game")
        self.__root.attributes("-zoomed", True)
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.__canvas = Canvas(self.__root,
                               bg="black",
                               height=self.__height,
                               width=self.__width)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__running = False

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()
        print("Window closed")

    def draw_line(self, line, fill_color="white"):
        line.draw(self.__canvas, fill_color)

    def generate_polygon_color(self, points, color):
        self.__canvas.create_polygon(
            points, outline="black", fill=color, width=2
        )

    def draw_oval(self, x1, y1, x2, y2, color):
        self.__canvas.create_oval(x1, y1, x2, y2,
                                  outline="black", fill=color,
                                  width=2)

    def close(self):
        self.__running = False

    def get_display_size(self):
        #  print(f"{self.__width} x {self.__height}")
        return self.__width, self.__height


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line:
    def __init__(self, p1, p2):
        self.x1 = p1.x
        self.y1 = p1.y
        self.x2 = p2.x
        self.y2 = p2.y

    def draw(self, canvas, fill_color="blue"):
        canvas.create_line(
            self.x1, self.y1, self.x2, self.y2, fill=fill_color, width=2,
        )
