import tkinter as tk
import os
import math
from gameplay.enums import bgc


# class
class Clock(object):
    def __init__(self, root, w, h, remainingTime):
        self.canvas = tk.Canvas(root, width=math.floor(0.22 * w), height=math.floor(0.3 * h), highlightbackground=bgc)
        self.canvas.place(x=math.floor(0.75 * w), y=0)
        self.canvas.configure(bg=bgc)
        self.image = None
        self.x = 150  # Center Point x
        self.y = 120  # Center Point
        

        self.render()
        self.update_time(remainingTime)

    def render(self):
        tk.Label(self.canvas, text="Remaining time", font=("Arial", 20), bg=bgc).place(x=90, y=50)
        self.generate_bg()
        return

    def generate_bg(self):
        self.image = tk.PhotoImage(file=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'graphics', 'DigitalClock.png'))  #'/home/ly30959/catkin_ws/SGAI_2023/data/clock.gif')
        self.image=self.image.subsample(3,3)
        self.canvas.create_image(self.x, self.y, image=self.image)
        return


    def update_time(self,remainingTime):
        hours = str(int(remainingTime/60))

        if len(hours)<2:
            hours='0'+hours
        minutes = str(remainingTime%60)
        if len(minutes)<2:
            minutes='0'+minutes
        if(remainingTime<=0):
            hours = '00'
            minutes = '00'
        xx=(self.x-45)
        tk.Label(self.canvas, text=hours, font=("Roboto", 25), bg="#fcf4f4", fg="black").place(x=xx, y=self.y-16)
        xx=(self.x+13)
        tk.Label(self.canvas, text=minutes, font=("Roboto", 25), bg="#fcf4f4", fg="black").place(x=xx, y=self.y-16)


        
        return


# # Main Function Trigger
# if __name__ == '__main__':
#     root = Clock()
#
#     # Creating Main Loop
#     while True:
#         root.update()
#         root.update_idletasks()
#         root.update_class(12, 15)
