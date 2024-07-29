import math
import tkinter as tk


class Probability(object):
    def __init__(self, root, w, h, humanoid, probs):
        self.canvas = tk.Canvas(root, width=math.floor(0.2 * w), height=math.floor(0.3 * h))
        self.canvas.place(x=math.floor(0.75 * w), y=math.floor(0.45 * h))
        self.jobs=[]
        self.probab=[]
        self.revealed = False
        self.update(humanoid, probs)
        self.canvas.update()


    def render_Job(self, job):
        
        if len(self.jobs)>0:
            for jobb in self.jobs:
                jobb.destroy()
        if len(self.probab)>0:
            for pro in self.probab:
                pro.destroy()
        self.jobs.append(tk.Label(self.canvas, text="Job: " + job, font=("Arial", 15)))
        self.jobs[len(self.jobs)-1].place(x=80, y=30)
        self.revealed=True
        self.canvas.update()
        return
    def render(self, probs):
        if len(self.jobs)>0:
            for job in self.jobs:
                job.destroy()
        if len(self.probab)>0:
            for pro in self.probab:
                pro.destroy()

        self.probab.append(tk.Label(self.canvas, text="Probability", font=("Arial", 15)))
        self.probab[len(self.probab)-1].place(x=80, y=30)

        i=0
        for job, prob in sorted(probs.items(), key=lambda item: item[1], reverse=True):
            self.probab.append(tk.Label(self.canvas, text=job, font=("Arial", 10)))
            self.probab[len(self.probab)-1].place(x=70, y=80+30*i)

            
            self.probab.append(tk.Label(self.canvas, text=str(prob)+"%", font=("Arial", 10)))
            self.probab[len(self.probab)-1].place(x=160, y=80 + 30 * i)
            i+=.8
        return
      
    def update(self, humanoid, display_probs=True):
        if display_probs:
            self.render(humanoid.probability)
        else:
            self.render_Job(humanoid.job)
        self.canvas.update()
        return
