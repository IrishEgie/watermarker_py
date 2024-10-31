from pathlib import Path
from tkinter import Label, Tk, Canvas, Button, PhotoImage, filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image, ImageTk
import os

import importlib.util

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"/run/media/ejarao/STORAGE/4 Dev Library/2 Python/watermarker_py/build/assets/frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def on_drop(event):
    file_path = event.data.strip('{}')  # Remove the curly braces from the dropped file path
    print(f"File dropped: {file_path}")
    messagebox.showinfo("File Uploaded", f"File uploaded: {file_path}")
    open_screen_2()

def select_file():
    # Set the initial directory based on the operating system
    if sys.platform.startswith('win'):
        initial_dir = "C:\\path\\to\\your\\images"  # Change this to your Windows image directory
    else:
        initial_dir = "/run/media/ejarao/STORAGE/4 Dev Library/2 Python/watermarker_py/img"  # Linux path

    file_path = filedialog.askopenfilename(
        initialdir=initial_dir,
        filetypes=[
            ("Image Files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp;*.tiff"),
            ("All Files", "*.*")
        ]
    )
    
    if file_path:
        print(f"File selected: {file_path}")
        messagebox.showinfo("File Selected", f"File selected: {file_path}")
        load_image(file_path)  # Load and display the image
        open_screen_2()
    else:
        print("No file selected.")

    # Print files in the initial directory for debugging
    print("Files in the initial directory:")
    for filename in os.listdir(initial_dir):
        print(filename)

def load_image(file_path):
    try:
        img = Image.open(file_path)
        img = img.resize((400, 300))  # Resize if necessary
        img = ImageTk.PhotoImage(img)

        img_window = Tk()
        img_label = Label(img_window, image=img)
        img_label.image = img  # Keep a reference to avoid garbage collection
        img_label.pack()
        img_window.mainloop()
    except Exception as e:
        print(f"Error loading image: {e}")
        messagebox.showerror("Error", "Could not load the image. Please check the file format.")


def open_screen_2():
    # Close the current window
    window.destroy()  
    
    # Import and run the gui1.py script
    gui1_path = "build/gui1.py"
    
    spec = importlib.util.spec_from_file_location("gui1", gui1_path)
    gui1 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gui1)

# Initialize main window for Screen 1
window = TkinterDnD.Tk()
window.geometry("800x600")
window.configure(bg="#FFFFFF")

canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=600,
    width=800,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)
image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(400.0, 300.0, image=image_image_1)

image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(400.0, 399.0, image=image_image_2)

canvas.create_text(
    230.0,
    134.0,
    anchor="nw",
    text="Add Watermark",
    fill="#000000",
    font=("Inter Bold", 36 * -1)
)

canvas.create_text(
    336.0,
    274.0,
    anchor="nw",
    text="or drag your files here",
    fill="#000000",
    font=("Inter", 12 * -1)
)

button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=select_file,
    relief="flat"
)
button_1.place(
    x=248.0,
    y=187.0,
    width=304.0,
    height=31.0
)

# Enable drag-and-drop on the window
window.drop_target_register(DND_FILES)
window.dnd_bind('<<Drop>>', on_drop)

window.resizable(False, False)
window.mainloop()
