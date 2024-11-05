from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage
import os
from config.config import Config
from custom_image_gallery import CustomImageGallery
import sys

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"/run/media/ejarao/STORAGE/4 Dev Library/2 Python/watermarker_py/build/assets/frame1")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def return_to_screen1():
    window.destroy()
    # Instead of importing, restart the application
    python = sys.executable
    os.execl(python, python, os.path.join(OUTPUT_PATH, 'gui.py'))

def add_watermark():
    if hasattr(window, 'image_gallery'):
        window.image_gallery.add_watermark_controls()

window = Tk()
window.geometry("800x600")
window.configure(bg="#FFFFFF")

# Create main canvas for the top bar and buttons
main_canvas = Canvas(window, bg="#FFFFFF", height=60, width=800, bd=0, highlightthickness=0, relief="ridge")
main_canvas.place(x=0, y=0)

# Get the selected image path from the configuration
selected_image_path = Config.selected_file_path

if selected_image_path and os.path.exists(selected_image_path):
    try:
        # Create and place the ImageGallery instance
        window.image_gallery = CustomImageGallery(window, selected_image_path)
        window.image_gallery.place(x=0, y=60, width=800, height=540)
    except Exception as e:
        print(f"Error loading image: {str(e)}")
        import traceback
        traceback.print_exc()  # This will help debug any issues
else:
    print("Error: No selected image path found or file does not exist.")

main_canvas.create_rectangle(0.0, 0.0, 800.0, 60.0, fill="#FFFFFF", outline="")

# Button creation
buttons = [
    ("button_1.png", (19.0, 19.0), 63.0, 23.0, return_to_screen1),  # Button to return to screen 1
    ("button_2.png", (717.0, 19.0), 63.0, 23.0, lambda: print("button_2 clicked")),
    ("button_3.png", (312.0, 19.0), 78.0, 23.0, add_watermark),  # Button to add watermark
    ("button_4.png", (400.0, 19.0), 77.9, 23.0, lambda: print("button_4 clicked"))
]

button_images = []

def create_button(img, pos, width, height, cmd):
    button_image = PhotoImage(file=relative_to_assets(img))
    button_images.append(button_image)
    button = Button(window, image=button_image, borderwidth=0, highlightthickness=0, command=cmd, relief="flat", cursor="hand2")
    button.place(x=pos[0], y=pos[1], width=width, height=height)

for img, pos, width, height, command in buttons:
    create_button(img, pos, width, height, command)

window.resizable(False, False)
window.mainloop()
