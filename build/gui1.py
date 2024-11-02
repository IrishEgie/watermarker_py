from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from PIL import Image, ImageTk
import os
from config import Config  # Import the Config class

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"/run/media/ejarao/STORAGE/4 Dev Library/2 Python/watermarker_py/build/assets/frame1")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

window = Tk()
window.geometry("800x600")
window.configure(bg="#FFFFFF")

canvas = Canvas(window, bg="#FFFFFF", height=600, width=800, bd=0, highlightthickness=0, relief="ridge")
canvas.place(x=0, y=0)

image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
canvas.create_image(400.0, 300.0, image=image_image_1)

selected_image_path = Config.selected_file_path

# Debugging output to check the selected file path
print("Selected image path:", selected_image_path)

if selected_image_path and os.path.exists(selected_image_path):
    try:
        # Use PIL to open the image
        pil_image = Image.open(selected_image_path)
        
        # Get the original dimensions
        original_width, original_height = pil_image.size
        
        # Desired dimensions for the canvas
        canvas_width = 800
        canvas_height = 600
        
        # Calculate the aspect ratio
        aspect_ratio = original_width / original_height
        
        # Determine the new dimensions while maintaining the aspect ratio
        if canvas_width / canvas_height > aspect_ratio:
            # Fit to height
            new_height = canvas_height
            new_width = int(new_height * aspect_ratio)
        else:
            # Fit to width
            new_width = canvas_width
            new_height = int(new_width / aspect_ratio)
        
        # Resize the image
        pil_image = pil_image.resize((new_width, new_height), Image.ANTIALIAS)
        
        # Convert to PhotoImage for Tkinter
        img = ImageTk.PhotoImage(pil_image)
        
        # Center the image on the canvas
        canvas.create_image((canvas_width - new_width) // 2, (canvas_height - new_height) // 2, image=img, anchor="nw")
        canvas.image = img  # Keep a reference to avoid garbage collection
    except Exception as e:
        print(f"Error loading image: {e}")
else:
    print("Error: No selected image path found or file does not exist.")
watermark_positions = [(40.0, 85.0), (700.0, 85.0), (700.0, 560.0), (40.0, 560.0), (375.0, 277.0)]
for pos in watermark_positions:
    canvas.create_text(pos[0], pos[1], anchor="nw", text="Watermark", fill="#FFFFFF", font=("Inter", 12 * -1))
canvas.create_rectangle(0.0, 0.0, 800.0, 60.0, fill="#FFFFFF", outline="")

buttons = [
    ("button_1.png", (19.0, 19.0), 63.0, 23.0, "button_1 clicked"),
    ("button_2.png", (717.0, 19.0), 63.0, 23.0, "button_2 clicked"),
    ("button_3.png", (312.0, 19.0), 78.0, 23.0, "button_3 clicked"),
    ("button_4.png", (400.0, 19.0), 77.9, 23.0, "button_4 clicked")
]

# Store references to images
button_images = []

def create_button(img, pos, width, height, cmd):
    button_image = PhotoImage(file=relative_to_assets(img))
    button_images.append(button_image)  # Keep a reference to avoid garbage collection
    button = Button(image=button_image, borderwidth=0, highlightthickness=0,
                    command=lambda: print(cmd), relief="flat")
    button.place(x=pos[0], y=pos[1], width=width, height=height)

for img, pos, width, height, command in buttons:
    create_button(img, pos, width, height, command)

window.resizable(False, False)
window.mainloop()
