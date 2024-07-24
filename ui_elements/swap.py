import math
import tkinter as tk


class Swap(object):
    def __init__(self, root, w, h):
        self.canvas = tk.Canvas(root, width=math.floor(0.2 * w), height=math.floor(0.3 * h))
        self.canvas.place(x=math.floor(0.3 * w), y=math.floor(0.1 * h))
        self.buttons=[]
        self.canvas.update()
    
    #creates the serum ui element
    def render(self, people):
        for i in range (0, len(people)):
            button = tk.Button(self.canvas, text="seat "+str(i+1), command=lambda i=i: self.button_clicked(i))
            button.place(x=80 + 30*i, y=60 )
            self.buttons.append(button)
        
        

        return
    def button_clicked(self, i):
        for button in self.buttons:
            button.destroy()
        return i
        
      
    
    
