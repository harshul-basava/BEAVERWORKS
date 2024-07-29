import math
import tkinter as tk
from tkmacosx import Button

# TODO - need to install: pip install tkinter-tooltip
from tktooltip import ToolTip


class CapacityMeter(object):
    def __init__(self, root, w, h, max_cap, probs):
        self.root = root
        self.w = w
        self.h = h

        self.canvas = tk.Canvas(root, width=math.floor(1.0 * w), height=math.floor(0.1 * h), highlightbackground='lightgreen')
        self.canvas.place(x=math.floor(0.06 * w), y=math.floor(0.8 * h))
        self.canvas.configure(bg='lightgreen')
        self.__units = []
        self.unit_size = 77  # resized in order to make two rows of 5
        self.canvas.update()
        self.render(max_cap, self.unit_size)
        self.probs = probs


    def render(self, max_cap, size):
        title = tk.Label(self.root, text="capacity", font=("Arial", 30), bg = 'lightgreen')
        title.pack(side='bottom', anchor='center', pady=30)
        # title.place(x=(self.root.winfo_width() - title.winfo_width()) // 2, y=math.floor(0.95 * self.h))

        x = 3
        y = 0
        for i in range(0, max_cap):
            self.__units.append(create_unit(self.canvas, x, y, size))
            x += size * 1.5
            if (x + size * 1.5) > self.canvas.winfo_width():
                x = 3
                y += size * 1.5

    def update_fill(self, index, log=None, probs=None, jobs=None):
        if index != 0:
            # self.root.itemconfig(self.__units[index-1], fill="midnightblue", activefill='red', stipple="")
            curr = self.__units[index-1]
            curr.config(bg="midnightblue", state="normal", activebackground='midnightblue')  # changing the color of the button and adding tooltip

            if log and log["action"] == "save":
                probs = log["humanoid_probs"]  # Example: {"Normal": 0.25, "Doctor": 0.25, "Engineer": 0.25, "Time-Wizard": 0.25}
                jobs = log["humanoid_job"]   # Class Name as a string
                self.toolTipCreator(curr, probs, jobs)  # create the toolTip

        else:
            for unit in self.__units:
                # self.root.itemconfig(unit, fill="white", activefill='white', stipple="gray25")
                unit.config(bg="white", state="disabled", activebackground='white')
                unit.unbind("<Enter>")  # removing the tooltip from the button when empty
                unit.unbind("<Leave>")

    def toolTipCreator(self, unit, probability, job):  # assigns the relevant toolTip information
        if not self.probs and type(job) is str:
            ToolTip(unit, msg=job, font=("Arial", 20))  # displays the job class of the humanoid just saved if known
        elif self.probs and type(probability) is dict:
            msg = ""
            for k, v in probability.items():
                msg += f"{k}: {v}%\n"
            ToolTip(unit, msg=msg.rstrip('\n'), font=("Arial", 15))  # displays a list of probabilities
        else:
            ToolTip(unit, msg="Error: No class info")



def create_unit(canvas, x, y, size):
    bn = Button(canvas, bg='white', height=size, width=size, state="disabled", activebackground='white')
    bn.place(x=x, y=y)  # replaced the rectangle with a button
    bn.pack
    return bn  # canvas.create_rectangle(x, y, x+size, y+size, fill='white', stipple="gray25")
