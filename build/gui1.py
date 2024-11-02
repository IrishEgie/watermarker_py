from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Frame
from PIL import Image, ImageTk
import os
from config import Config
import tkinter as tk

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"/run/media/ejarao/STORAGE/4 Dev Library/2 Python/watermarker_py/build/assets/frame1")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class CustomImageGallery(Frame):
    def __init__(self, parent, img_path):
        super().__init__(parent)  # Properly initialize Frame
        
        self.image = Image.open(img_path)
        self.zoom = 1.0
        self.prev_x = self.prev_y = 0
        self.limits = {'l': 150, 'r': 150, 't': 150, 'b': 150}
        
        # Create canvas with specific dimensions
        self.canvas = Canvas(self, bg="white", height=480, width=800)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Resize image to fit canvas while maintaining aspect ratio
        canvas_ratio = 800 / 480
        img_ratio = self.image.width / self.image.height
        
        if img_ratio > canvas_ratio:
            # Image is wider than canvas
            new_width = 800
            new_height = int(800 / img_ratio)
        else:
            # Image is taller than canvas
            new_height = 480
            new_width = int(480 * img_ratio)
            
        self.image = self.image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        self.img_tk = ImageTk.PhotoImage(self.image)
        self.img_id = self.canvas.create_image(400, 240, image=self.img_tk, anchor='center')
        
        self.zoom_label = tk.Label(self, text=f"Zoom: {int(self.zoom * 100)}%", bg="white")
        self.zoom_label.place(x=30, y=440, anchor='sw')  # Fixed position for zoom label
        
        # Bind events
        self.canvas.bind("<MouseWheel>", lambda e: self._handle_zoom(1.1 if e.delta > 0 else 0.9))
        self.canvas.bind("<Button-4>", lambda e: self._handle_zoom(1.1))
        self.canvas.bind("<Button-5>", lambda e: self._handle_zoom(0.9))
        self.canvas.bind("<ButtonPress-1>", self._start_drag)
        self.canvas.bind("<B1-Motion>", self._handle_drag)

    def _handle_zoom(self, factor):
        new_zoom = self.zoom * factor
        if 0.5 <= new_zoom <= 2.0:
            self.zoom = new_zoom
            new_size = tuple(int(d * self.zoom) for d in self.image.size)
            resized = self.image.resize(new_size, Image.Resampling.LANCZOS)
            self.img_tk = ImageTk.PhotoImage(resized)
            self.canvas.itemconfig(self.img_id, image=self.img_tk)
            self.zoom_label.config(text=f"Zoom: {int(self.zoom * 100)}%")
            self._center_image()

    def _start_drag(self, event):
        self.prev_x = event.x
        self.prev_y = event.y

    def _handle_drag(self, event):
        dx = event.x - self.prev_x
        dy = event.y - self.prev_y
        self.canvas.move(self.img_id, dx, dy)
        self.prev_x = event.x
        self.prev_y = event.y

    def _center_image(self):
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        img_width = int(self.image.width * self.zoom)
        img_height = int(self.image.height * self.zoom)
        x = (canvas_width - img_width) // 2
        y = (canvas_height - img_height) // 2
        self.canvas.coords(self.img_id, x + img_width//2, y + img_height//2)

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
    ("button_1.png", (19.0, 19.0), 63.0, 23.0, "button_1 clicked"),
    ("button_2.png", (717.0, 19.0), 63.0, 23.0, "button_2 clicked"),
    ("button_3.png", (312.0, 19.0), 78.0, 23.0, "button_3 clicked"),
    ("button_4.png", (400.0, 19.0), 77.9, 23.0, "button_4 clicked")
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