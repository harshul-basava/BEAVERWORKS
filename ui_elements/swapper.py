import math
import tkinter as tk


class Swapper(object):
    def __init__(self, root, w, h):
        self.canvas = tk.Canvas(root, width=math.floor(0.6 * w), height=math.floor(0.1 * h))
        self.canvas.place(x=math.floor(0.3 * w), y=math.floor(0.01 * h))
        self.canvas.update()
        self.user_index = None

    def render(self, root, carrying):

        def get_number():
            try:
                number = int(entry.get())
                if 1 <= number <= len(carrying):
                    self.user_index = number - 1  
                    root.quit()  
                else:
                    print(f"Number is out of range. Please enter a number between 1 and {len(carrying)}.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

        entry = tk.Entry(self.canvas)
        self.canvas.create_window(math.floor(0.1 * self.canvas.winfo_width()), math.floor(0.1 * self.canvas.winfo_height()), window=entry)

        button = tk.Button(self.canvas, text="Submit", command=get_number)
        self.canvas.create_window(math.floor(0.3 * self.canvas.winfo_width()), math.floor(0.1 * self.canvas.winfo_height()), window=button)

        root.mainloop()

        entry.destroy()
        button.destroy()
        index=self.user_index
        self.user_index = None
        return index
    
