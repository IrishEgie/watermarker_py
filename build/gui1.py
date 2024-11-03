from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Frame
from PIL import Image, ImageTk
import os
from config import Config
import tkinter as tk
from image_view import CustomImageGallery

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"/run/media/ejarao/STORAGE/4 Dev Library/2 Python/watermarker_py/build/assets/frame1")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def return_to_screen1():
    window.destroy()
    import gui  # Import and run Screen 1


window = Tk()
window.geometry("800x600")
window.configure(bg="#FFFFFF")

# Create main canvas for the top bar and buttons
main_canvas = Canvas(window, bg="#FFFFFF", height=60, width=800, bd=0, highlightthickness=0, relief="ridge")
main_canvas.place(x=0, y=0)

selected_image_path = Config.selected_file_path

if selected_image_path and os.path.exists(selected_image_path):
    try:
        # Create and place the ImageGallery instance
        image_gallery = CustomImageGallery(window, selected_image_path)
        image_gallery.place(x=0, y=60, width=800, height=540)  # Place below the top bar
    except Exception as e:
        print(f"Error loading image: {str(e)}")
else:
    print("Error: No selected image path found or file does not exist.")

# Create watermark positions on the main canvas
watermark_positions = [(40.0, 85.0), (700.0, 85.0), (700.0, 560.0), (40.0, 560.0), (375.0, 277.0)]
for pos in watermark_positions:
    main_canvas.create_text(pos[0], pos[1], anchor="nw", text="Watermark", fill="#FFFFFF", font=("Inter", 12 * -1))

main_canvas.create_rectangle(0.0, 0.0, 800.0, 60.0, fill="#FFFFFF", outline="")

# Button creation
buttons = [
    ("button_1.png", (19.0, 19.0), 63.0, 23.0, return_to_screen1),  # Modified to use return_to_screen1 function
    ("button_2.png", (717.0, 19.0), 63.0, 23.0, lambda: print("button_2 clicked")),
    ("button_3.png", (312.0, 19.0), 78.0, 23.0, lambda: print("button_3 clicked")),
    ("button_4.png", (400.0, 19.0), 77.9, 23.0, lambda: print("button_4 clicked"))
]
button_images = []

def create_button(img, pos, width, height, cmd):
    button_image = PhotoImage(file=relative_to_assets(img))
    button_images.append(button_image)
    button = Button(window, image=button_image, borderwidth=0, highlightthickness=0,
                   command=lambda: print(cmd), relief="flat")
    button.place(x=pos[0], y=pos[1], width=width, height=height)

for img, pos, width, height, command in buttons:
    create_button(img, pos, width, height, command)

window.resizable(False, False)
window.mainloop()