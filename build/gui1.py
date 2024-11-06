import os
import sys
from pathlib import Path
import customtkinter as ctk
from config.config import Config
from config.watermark_handler import WatermarkHandler
from config.watermark_controls import WatermarkControls
from gui import WatermarkApp

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"/run/media/ejarao/STORAGE/4 Dev Library/2 Python/watermarker_py/build/assets/frame1")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def return_to_screen1():
    window.destroy()
    # Restart the application by running the initial gui.py
    python = sys.executable
    os.execl(python, python, os.path.join(OUTPUT_PATH, 'gui.py'))

def add_watermark():
    if hasattr(window, 'watermark_handler'):
        window.watermark_controls.add_watermark_controls()

# Initialize customtkinter window
window = ctk.CTk()
window.geometry("800x600")

# Create main canvas for the top bar and buttons
main_canvas = ctk.CTkCanvas(window, height=60, width=800, bg=Config.get_dynamic_bg_color(), bd=0)
main_canvas.place(x=0, y=0)

# Get the selected image path from the configuration
selected_image_path = Config.selected_file_path

if selected_image_path and os.path.exists(selected_image_path):
    try:
        # Initialize WatermarkHandler and place it in the window
        window.watermark_handler = WatermarkHandler(window, selected_image_path)
        window.watermark_handler.place(x=0, y=60, width=800, height=540)
        
        # Initialize WatermarkControls with the watermark handler
        window.watermark_controls = WatermarkControls(window.watermark_handler)
    except Exception as e:
        print(f"Error loading image: {str(e)}")
        import traceback
        traceback.print_exc()  # This will help debug any issues
else:
    print("Error: No selected image path found or file does not exist.")

# Button creation (no images, just text-based buttons)
buttons = [
    ("Return", (20.0, 20.0), 100.0, 25.0, return_to_screen1),  # Button to return to screen 1
    ("Save", (680.0, 20.0), 100.0, 25.0, lambda: print("button_2 clicked")),
    ("Add Watermark", (290.0, 20.0), 100.0, 25.0, add_watermark),  # Button to add watermark
    ("Button 4", (400.0, 20.0), 100.0, 25.0, lambda: print("button_4 clicked"))
]

def create_button(text, pos, width, height, cmd):
    button = ctk.CTkButton(window, text=text, width=width, height=height, command=cmd, bg_color=Config.get_dynamic_bg_color())
    button.place(x=pos[0], y=pos[1])

# Create and place all buttons
for text, pos, width, height, command in buttons:
    create_button(text, pos, width, height, command)

window.resizable(False, False)
window.mainloop()
