import math
import tkinter as tk


class Probability(object):
    def __init__(self, root, w, h, classes, probs):
        self.canvas = tk.Canvas(root, width=math.floor(0.2 * w), height=math.floor(0.3 * h))
        self.canvas.place(x=math.floor(0.75 * w), y=math.floor(0.7 * h))
        self.render(classes, probs)
        self.canvas.update()



    def render(self, type, prob):
        tk.Label(self.canvas, text="Probability", font=("Arial", 15)).place(x=80, y=30)
        for i in range(len(type)):
            tk.Label(self.canvas, text=type[i], font=("Arial", 10)).place(x=50, y=80 + 30 * i)
            tk.Label(self.canvas, text=prob[i]+"%", font=("Arial", 10)).place(x=140, y=80 + 30 * i)
        return
    def update(self, type, prob):
        self.render(type, prob)
        self.canvas.update()
        return

