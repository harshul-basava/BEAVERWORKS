import math
import tkinter as tk
from gameplay.enums import bgc
from os.path import join
from PIL import ImageTk, Image


class GameViewer(object):
    def __init__(self, root, w, h, data_fp, humanoid):
        self.canvas = tk.Canvas(root, width=math.floor(0.9 * 0.5 * w), height=math.floor(0.9 * 0.75 * h), highlightbackground='midnightblue')
        self.canvas.place(x=350, y=50)
        self.canvas.configure(bg=bgc)
        self.canvas.update()
        
        
        self.photo = None
        self.create_photo(join(data_fp, humanoid.fp))

    def delete_photo(self, event=None):
        self.canvas.delete('photo')

    def create_photo(self, fp):
        self.canvas.delete('photo')
        self.photo = display_photo(fp, self.canvas.winfo_width(), self.canvas.winfo_height())
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo, tags='photo')

        
    def display_score(self, score):
        tk.Label(self.canvas, text="FINAL SCORE", font=("Arial", 30), bg = bgc).pack(anchor=tk.NW)
        tk.Label(self.canvas, text="Killed {}".format(score["killed"]), font=("Arial", 15), bg = bgc).pack(anchor=tk.NW)
        tk.Label(self.canvas, text="Saved {}".format(score["saved"]), font=("Arial", 15), bg = bgc).pack(anchor=tk.NW)



def display_photo(img_path, w, h):
    img = Image.open(img_path)
    resized = img.resize((w, h), Image.LANCZOS)

    tk_img = ImageTk.PhotoImage(resized)
    return tk_img
