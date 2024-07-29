import math
import tkinter as tk


class Serum(object):
    def __init__(self, root, w, h, count):
        self.canvas = tk.Canvas(root, width=math.floor(0.1 * w), height=math.floor(0.05 * h))
        self.canvas.place(x=math.floor(0.8 * w), y=math.floor(0.38 * h))
        self.serums=[]
        self.render(count)
        self.canvas.update()
    
    #creates the serum ui element
    def render(self, count):
        if len(self.serums)>0:
            for serum in self.serums:
                serum.destroy()
        

        self.serums.append(tk.Label(self.canvas, text="Serums: " + str(count), font=("Arial", 15)))
        self.serums[len(self.serums)-1].place(x=30, y=10)
        self.canvas.update()

        return
      
    def update(self, count):
        self.render(count)
        self.canvas.update()
        return
    
