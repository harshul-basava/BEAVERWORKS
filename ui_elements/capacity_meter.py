import math
import tkinter as tk
from tkmacosx import Button

# TODO - need to install: pip install tkinter-tooltip
from tktooltip import ToolTip


class CapacityMeter(object):
    def __init__(self, root, w, h, max_cap):
        self.root = root
        self.canvas = tk.Canvas(root, width=math.floor(0.2 * w), height=math.floor(0.3 * h))
        self.canvas.place(x=math.floor(0.75 * w), y=math.floor(0.4 * h))
        self.__units = []
        self.unit_size = 34  # resized in order to make two rows of 5
        self.canvas.update()
        self.render(max_cap, self.unit_size)

    def render(self, max_cap, size):
        tk.Label(self.canvas, text="Capacity", font=("Arial", 15)).place(x=100, y=0)

        x = 3
        y = 50
        for i in range(0, max_cap):
            self.__units.append(create_unit(self.canvas, x, y, size))
            x += size * 1.5
            if (x + size * 1.5) > self.canvas.winfo_width():
                x = 3
                y += size * 1.5

    def update_fill(self, index):
        if index != 0:
            # self.root.itemconfig(self.__units[index-1], fill="midnightblue", activefill='red', stipple="")
            curr = self.__units[index-1]
            curr.config(bg="midnightblue", state="normal", activebackground='midnightblue')  # changing the color of the button and adding tooltip
            ToolTip(curr, msg="important info")

        else:
            for unit in self.__units:
                # self.root.itemconfig(unit, fill="white", activefill='white', stipple="gray25")
                unit.config(bg="white", state="disabled", activebackground='white')
                unit.unbind("<Enter>")  # removing the tooltip from the button when empty
                unit.unbind("<Leave>")


def create_unit(canvas, x, y, size):
    bn = Button(canvas, bg='white', height=size, width=size, state="disabled", activebackground='white')
    bn.place(x=x, y=y)  # replaced the rectangle with a button
    bn.pack
    return bn  # canvas.create_rectangle(x, y, x+size, y+size, fill='white', stipple="gray25")
