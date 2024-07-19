import math
import tkinter as tk


class Probability(object):
    def __init__(self, root, w, h, prob):
        self.canvas = tk.Canvas(root, width=math.floor(0.2 * w), height=math.floor(0.3 * h))
        self.canvas.place(x=math.floor(0.75 * w), y=math.floor(0.6 * h))
        self.render(prob)
        self.canvas.update()


    def render_Job(self, job):
        
        tk.Label(self.canvas, text="Job", font=("Arial", 15)).place(x=80, y=30)
        tk.Label(self.canvas, text=job, font=("Arial", 15)).place(x=80, y=50)
        self.canvas.update()
        return
    def render(self, probs):

        tk.Label(self.canvas, text="Probability", font=("Arial", 15)).place(x=80, y=30)
        i=0
        for job, prob in probs.items():
            tk.Label(self.canvas, text=job, font=("Arial", 10)).place(x=70, y=80 + 30 * i)
            tk.Label(self.canvas, text=str(prob)+"%", font=("Arial", 10)).place(x=160, y=80 + 30 * i)
            i+=.8
        return
    def update(self, probss):
        self.render(probss)
        self.canvas.update()
        return

