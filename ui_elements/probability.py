import math
import tkinter as tk
from gameplay.enums import bgc
from PIL import ImageTk, Image


class Probability(object):
    def __init__(self, root, w, h, humanoid, probs):
        self.canvas = tk.Canvas(root, width=math.floor(0.3 * w), height=math.floor(0.4 * h), highlightbackground=bgc)
        self.canvas.place(x=math.floor(0.76 * w), y=math.floor(0.33 * h))
        self.canvas.configure(bg=bgc)

        image = Image.open(f"ui_elements/graphics/Probability_BG.png")

        dim = (270, 324)

        bg = Image.new('RGB', dim, bgc)
        image = image.resize(dim, Image.LANCZOS)
        bg.paste(image, (0, 0), image)
        image = bg

        self.tk_image = ImageTk.PhotoImage(image)
        self.panel = tk.Button(self.canvas, width=268, height=322, image=self.tk_image, highlightbackground=bgc)
        self.panel.place(x=0, y=0)

        empty = Image.open(f"ui_elements/graphics/empty.png").resize((100, 16), Image.LANCZOS)
        self.tk_empty = ImageTk.PhotoImage(empty)

        self.fill = Image.open(f"ui_elements/graphics/fill.png")
        self.tk_fills = []

        self.empties = []
        self.fills = []

        self.jobs=[]
        self.probab=[]
        self.revealed = False
        self.update(humanoid, probs)
        self.canvas.update()


    def render_Job(self, job):
        self.panel.place(x=0, y=0)
        if len(self.jobs)>0:
            for jobb in self.jobs:
                jobb.destroy()
        if len(self.probab)>0:
            for pro in self.probab:
                pro.destroy()
        self.jobs.append(tk.Label(self.canvas, text="Job: " + job, font=("Arial", 30), bg="#DAE2FF", fg="midnightblue"))
        self.jobs[len(self.jobs)-1].place(x=130, y=120, anchor="n")
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

        # self.probab.append(tk.Label(self.canvas, text="Probability", font=("Arial", 15), bg = bgc))
        # self.probab[len(self.probab)-1].place(x=80, y=30)

        i = 0
        for job, prob in sorted(probs.items(), key=lambda item: item[1], reverse=True):
            self.probab.append(tk.Label(self.canvas, text= f"{job.upper()}: {prob}%", font=("Roboto", 16), bg="#DAE2FF", fg="midnightblue"))
            self.probab[len(self.probab)-1].place(x=140, y=100 + i, anchor="ne")

            panel = tk.Label(self.canvas, image=self.tk_empty)
            panel.place(x=145, y=103 + i)
            self.empties.append(panel)

            self.tk_fills.append(ImageTk.PhotoImage(self.fill.resize((math.floor(prob), 16), Image.LANCZOS)))
            filling = tk.Label(self.canvas, image=self.tk_fills[-1])
            filling.place(x=145, y=103 + i)
            self.fills.append(filling)

            i += 35
        return
      
    def update(self, humanoid, display_probs=True):
        if display_probs:
            self.render(humanoid.probability)
        else:
            self.render_Job(humanoid.job)
        self.canvas.update()
        return
