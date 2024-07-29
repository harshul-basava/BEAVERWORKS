import math
import tkinter as tk
from gameplay.enums import bgc


class Serum(object):
    def __init__(self, root, w, h, count):
        self.canvas = tk.Canvas(root, width=math.floor(0.2 * w), height=math.floor(0.05 * h), highlightbackground=bgc)
        self.canvas.place(x=math.floor(0.785 * w), y=math.floor(0.23 * h))
        self.canvas.configure(bg=bgc)
        self.serums=[]
        self.render(count)
        self.canvas.update()
    
    #creates the serum ui element
    def render(self, count):
        if len(self.serums)>0:
            for serum in self.serums:
                serum.destroy()
        

        self.serums.append(tk.Label(self.canvas, text="Serums: " + str(count), font=("Arial", 30), bg = bgc))
        self.serums[len(self.serums)-1].place(x=30, y=10)
        self.canvas.update()

        return
      
    def update(self, count):
        self.render(count)
        self.canvas.update()
        return
    
