import tkinter as tk
from tkinter import ttk

def update_font_size(value):
    try:
        new_font_size = int(float(value))
        label.config(font=("Roboto", new_font_size))
    except ValueError:
        pass  # Ignore non-integer values
parent = tk.Tk()
parent.title("Font Size Control")
# Create a Scale widget for font size control
font_size_scale = ttk.Scale(parent, from_=10, to=36, orient="horizontal", length=200, command=update_font_size)
font_size_scale.pack(pady=10)
# Create a label with initial font size
initial_font_size = 16
label = ttk.Label(parent, text="Font Size", font=("Roboto", initial_font_size))
label.pack(pady=10)
parent.mainloop()
