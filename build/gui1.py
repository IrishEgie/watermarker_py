from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage

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

image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(400.0, 330.0, image=image_image_2)
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
