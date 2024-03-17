import math
import tkinter as tk
from typing import List
import copy


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

    def move_translation(self, x_factor, y_factor):
        self.x += x_factor
        self.y += y_factor

    def rotate(self, angle):
        self.x = round(self.x * math.cos(angle) - self.y * math.sin(angle))
        self.y = round(self.x * math.sin(angle) + self.y * math.cos(angle))


canvas_size = 400


class PointSelector:
    def __init__(self, root):

        self.root = root
        self.root.title("Canvas")

        # Define Sliders
        self.x_translation = tk.DoubleVar()
        self.y_translation = tk.DoubleVar()
        self.rotation_angle = tk.DoubleVar()

        # Define canvas
        self.canvas = tk.Canvas(root, width=canvas_size, height=canvas_size, bg="white")
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
        self.apply_rotation_btn = tk.Button(root, text="Apply", command=self.rotate_point)
        self.apply_rotation_btn.grid(row=3, column=2, columnspan=1)

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
        self.print_points()

        if factor != 0:
            # Clear previous points
            self.clear_canvas()
            for point in self.points:
                point.move_translation(factor, 0)
                self.plot_point(point)

            self.print_points()

    def apply_y_translation(self):
        if not self.has_defined_points():
            return

        factor = self.y_translation.get()

        print("FACTOR: " + str(factor))
        self.print_points()

        if factor != 0:
            # Clear previous points
            self.clear_canvas()
            for point in self.points:
                point.move_translation(0, factor)
                self.plot_point(point)

            self.print_points()

    def rotate_point(self):
        def translate_to_origin(polygon):
            centroid_x = sum(vertex.x for vertex in polygon) / len(polygon)
            centroid_y = sum(vertex.y for vertex in polygon) / len(polygon)

            translated_polygon = [Point(vertex.x - centroid_x, vertex.y - centroid_y) for vertex in polygon]

            return translated_polygon, (centroid_x, centroid_y)

        def rollback_translation(polygon, centroid_val):
            # Rollback translation
            rolled_back_polygon = [Point(vertex.x + centroid_val[0], vertex.y + centroid_val[1]) for vertex in polygon]

            return rolled_back_polygon

        if not self.has_defined_points():
            return

        print('ROTATION:')
        angle = self.rotation_angle.get()

        if angle == 0:
            return

        rot_angle_rad = angle * math.pi / 180.0
        print("ANGLE: " + str(angle))
        print(rot_angle_rad)
        self.print_points()

        # Translate to origin
        new_points, centroid = translate_to_origin(copy.copy(self.points))

        # Rotate points
        for point in new_points:
            point.rotate(rot_angle_rad)

        # Return to correct position
        self.points = rollback_translation(new_points, centroid)

        self.clear_canvas()
        for point in self.points:
            self.plot_point(point)


if __name__ == "__main__":
    root = tk.Tk()
    point_selector = PointSelector(root)
    root.mainloop()
