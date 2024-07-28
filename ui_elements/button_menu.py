import tkinter as tk
import os
from PIL import ImageTk, Image

from gameplay.enums import ActionCost


class ButtonMenu(object):
    def __init__(self, root, items, probs=True):
        self.canvas = tk.Canvas(root, width=500, height=80)

        rgb = tuple((c//256 for c in root.winfo_rgb(root.cget("bg"))))

        names = ["Skip", "Squish", "Save", "Scram", "Reveal"]
        disabled_names = [f"Disabled_{name}" for name in names]

        images = [Image.open(f"ui_elements/button_icons/{name}.png") for name in names]
        disabled_images = [Image.open(f"ui_elements/button_icons/Disabled_{name}.png") for name in names]

        for i, img in enumerate(images):
            bg = Image.new('RGB', (288, 80), rgb)
            img = img.resize((288, 80), Image.LANCZOS)
            bg.paste(img, (0, 0), img)
            images[i] = bg

        for i, img in enumerate(disabled_images):
            bg = Image.new('RGB', (288, 80), rgb)
            img = img.resize((288, 80), Image.LANCZOS)
            bg.paste(img, (0, 0), img)
            disabled_images[i] = bg

        self.tk_images = [ImageTk.PhotoImage(img) for img in images]

        self.photos = dict(zip(names, self.tk_images))
        self.disabled_photos = [ImageTk.PhotoImage(img) for img in disabled_images]

        self.canvas.place(x=20, y=90)
        self.buttons = self.create_buttons(self.canvas, items)
        self.probs = probs
        create_menu(self.buttons)

    def disable_buttons(self, remaining_time, remaining_humanoids, at_capacity):
        if remaining_humanoids == 0 or remaining_time <= 0:
            for i in range(0, len(self.buttons)):
                self.buttons[i].config(state="disabled", image=self.disabled_photos[i])
        #  Not enough time left? Disable action
        if (remaining_time - ActionCost.SCRAM.value) < ActionCost.SKIP.value:
            self.buttons[0].config(state="disabled", image=self.disabled_photos[0])
        else:
            self.buttons[0].config(state="normal", image=self.tk_images[0])
        if (remaining_time - ActionCost.SCRAM.value) < ActionCost.SQUISH.value:
            self.buttons[1].config(state="disabled", image=self.disabled_photos[1])
        else:
            self.buttons[1].config(state="normal", image=self.tk_images[1])
        if (remaining_time - ActionCost.SCRAM.value) < ActionCost.SAVE.value:
            self.buttons[2].config(state="disabled", image=self.disabled_photos[2])
        else:
            self.buttons[2].config(state="normal", image=self.tk_images[2])
        if (remaining_time - ActionCost.SCRAM.value) < ActionCost.REVEAL.value:
            self.buttons[4].config(state="disabled", image=self.disabled_photos[4])
        else:
            self.buttons[4].config(state="normal", image=self.tk_images[4])
        if at_capacity or (remaining_time - ActionCost.SCRAM.value) <= 0:
            self.buttons[0].config(state="disabled", image=self.disabled_photos[0])
            self.buttons[1].config(state="disabled", image=self.disabled_photos[1])
            self.buttons[2].config(state="disabled", image=self.disabled_photos[2])
            self.buttons[4].config(state="disabled", image=self.disabled_photos[3])
        if not self.probs:
            self.buttons[4].config(state="disabled", image=self.disabled_photos[4])

    def create_buttons(self, canvas, items):
        buttons = []
        for item in items:
            (text, action) = item
            buttons.append(tk.Button(canvas,
                                     height=78,
                                     width=286,
                                     image=self.photos[text],
                                     command=action,
                                     highlightthickness=0,
                                     bd=0))
        return buttons

    def disable_reveal(self):
        self.buttons[4].config(state="disabled", image=self.disabled_photos[4])

def create_menu(buttons):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'graphics', 'logo.png')
    logo = ImageTk.PhotoImage(Image.open(path).resize((300, 50), Image.LANCZOS))
    label = tk.Label(image=logo)
    label.image = logo

    # Position image
    label.place(x=10, y=10)

    for button in buttons:
        button.pack(side=tk.TOP, pady=10)

