import tkinter as tk
from typing import List


class Point:
    def __init__(self, x=-1, y=-1):
        self.x = x
        self.y = y

    def __str__(self):
        return f'({self.x}, {self.y})'

    def clear(self):
        self.x = -1
        self.y = -1

    def has_point(self) -> bool:
        return self.x != -1 and self.y != -1


class PointSelector:
    def __init__(self, root):
        self.root = root
        self.root.title("Canvas")

        # Define Sliders
        self.x_translation = tk.DoubleVar()
        self.y_translation = tk.DoubleVar()
        self.rotation_angle = tk.DoubleVar()

        # Define canvas
        self.canvas = tk.Canvas(root, width=400, height=400, bg="white")
        self.canvas.grid(row=0, column=0, columnspan=3)

        # Define initial variables
        self.points: List[Point] = []
        self.initial_point: Point
        self.final_point: Point

        # Slider and Apply Btn for Translation X
        tk.Label(root, text="X Translation").grid(row=1, column=0)
        self.x_slider = tk.Scale(root, variable=self.x_translation, from_=-200, to=200, orient=tk.HORIZONTAL)
        self.x_slider.grid(row=1, column=1)
        self.apply_x_translation_btn = tk.Button(root, text="Apply", command=self.apply_x_translation)
        self.apply_x_translation_btn.grid(row=1, column=2, columnspan=1)

        # Slider Translation Y
        tk.Label(root, text="Y Translation").grid(row=2, column=0)
        self.y_slider = tk.Scale(root, variable=self.y_translation, from_=-200, to=200, orient=tk.HORIZONTAL)
        self.y_slider.grid(row=2, column=1)
        self.apply_y_translation_btn = tk.Button(root, text="Apply", command=self.apply_y_translation)
        self.apply_y_translation_btn.grid(row=2, column=2, columnspan=1)

        # Slider for Rotation
        tk.Label(root, text="Rotation Angle").grid(row=3, column=0)
        self.rotation_slider = tk.Scale(root, variable=self.rotation_angle, from_=-180, to=180, orient=tk.HORIZONTAL)
        self.rotation_slider.grid(row=3, column=1)

        # Button to clear all points
        self.clear_button = tk.Button(root, text="Clear Points", command=self.clear_points)
        self.clear_button.grid(row=4, column=0, columnspan=2)

        # User interaction with interface
        self.canvas.bind("<Button-1>", self.on_click)

    # Handle user click on interface
    def on_click(self, event):
        x, y = event.x, event.y

        # Check if canvas is clean
        if len(self.points) >= 2:
            return

        # Check if canvas is waiting for first point to be defined
        if len(self.points) == 0:
            point = Point(x, y)
            self.initial_point = point
            # add initial point in array and plot it
            self.points.append(point)
            self.plot_point(point)

        # Check if canvas is waiting for final point to be defined
        elif len(self.points) == 1:
            point = Point(x, y)
            self.final_point = point
            # add final point in array and plot it
            self.points.append(point)
            self.plot_point(point)

    def plot_point(self, point: Point, color='red'):
        self.canvas.create_oval(point.x - 5, point.y - 5, point.x + 5, point.y + 5, fill=color)

    def has_defined_points(self):
        if len(self.points) >= 2:
            return True
        return False

    def rotate_point(self, x, y, angle):
        return

    def clear_points(self):
        self.points = []
        self.initial_point = None
        self.final_point = None
        self.clear_canvas()

    def clear_canvas(self):
        self.canvas.delete("all")

    def print_points(self):
        str_points = "[ "
        for point in self.points:
            str_points += str(point)
            str_points += " "
        str_points += "]"
        print(str_points)

    def apply_x_translation(self):
        if not self.has_defined_points():
            return

        factor = self.x_translation.get()

        print("FACTOR: " + str(factor))
        print(self.print_points())

        if factor != 0:
            # Clear previous points
            self.clear_canvas()
            for point in self.points:
                point.x += factor
                self.plot_point(point)

            print(self.print_points())

    def apply_y_translation(self):
        if not self.has_defined_points():
            return

        factor = self.y_translation.get()

        print("FACTOR: " + str(factor))
        print(self.print_points())

        if factor != 0:
            # Clear previous points
            self.clear_canvas()
            for point in self.points:
                point.y += factor
                self.plot_point(point)

            print(self.print_points())


if __name__ == "__main__":
    root = tk.Tk()
    point_selector = PointSelector(root)
    root.mainloop()
