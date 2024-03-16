import tkinter as tk


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
        self.points = []
        self.initial_point = -1
        self.final_point = -1

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
        if len(self.points) == 0:
            self.initial_point = {x, y}
            self.points.append({x, y})
            self.plot_point(x, y)
        # Check if canvas is waiting for final point to be defined
        elif len(self.points) == 1 and self.final_point == -1:
            self.final_point = {x, y}
            self.plot_point(x, y)

    def plot_point(self, x, y, color='red'):
        self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill=color)

    def rotate_point(self, x, y, angle):
        return

    def clear_points(self):
        self.points = []
        self.initial_point = -1
        self.final_point = -1
        self.canvas.delete("all")  # Clear canvas

    def apply_x_translation(self):
        print(self.x_translation.get())
        pass

    def apply_y_translation(self):
        print(self.y_translation.get())
        pass


if __name__ == "__main__":
    root = tk.Tk()
    point_selector = PointSelector(root)
    root.mainloop()
