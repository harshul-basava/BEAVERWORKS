import tkinter as tk
import os
import math


# class
class Clock(object):
    def __init__(self, root, w, h, remainingTime):
        self.canvas = tk.Canvas(root, width=math.floor(0.22 * w), height=math.floor(0.3 * h), highlightbackground='lightgreen')
        self.canvas.place(x=math.floor(0.75 * w), y=50)
        self.canvas.configure(bg='lightgreen')
        self.image = None
        self.x = 150  # Center Point x
        self.y = 150  # Center Point
        

        self.render()
        self.update_time(remainingTime)

    def render(self):
        tk.Label(self.canvas, text="Remaining time", font=("Arial", 15), bg = 'lightgreen').place(x=80, y=50)
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
        tk.Label(self.canvas, text=hours, font=("Arial", 20)).place(x=xx, y=self.y-18)
        xx=(self.x+10)
        tk.Label(self.canvas, text=minutes, font=("Arial", 20)).place(x=xx, y=self.y-18)


        
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
