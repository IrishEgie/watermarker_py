from pathlib import Path
from tkinter import Label, Tk, Canvas, Button, PhotoImage, filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image, ImageTk
import os
import sys
from config import Config  # Import the Config class

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"/run/media/ejarao/STORAGE/4 Dev Library/2 Python/watermarker_py/build/assets/frame0")

selected_image_path = Config.selected_file_path

def relative_to_assets(path: str) -> Path: return ASSETS_PATH / Path(path)

def on_drop(event):
    global selected_file_path
    file_path = event.data.strip('{}')
    print(f"File dropped: {file_path}")
    messagebox.showinfo("File Uploaded", f"File uploaded: {file_path}")
    selected_file_path = file_path  # Update the global variable
    open_screen_2()

def select_file():
    global selected_file_path
    initial_dir = os.path.join(os.environ['USERPROFILE'], 'Pictures') if sys.platform.startswith('win') else os.path.expanduser('~/Pictures')
    file_path = filedialog.askopenfilename(initialdir=initial_dir, filetypes=[("All Files", "*.*")])
    if file_path and any(file_path.lower().endswith(ext) for ext in {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff'}):
        Config.selected_file_path = file_path
        print(f"File selected: {file_path}")
        messagebox.showinfo("File Selected", f"File selected: {file_path}")
        open_screen_2()
    else:
        messagebox.showwarning("Invalid File Type", "The selected file is not an image. Please select a valid image file.")

def open_screen_2():
    print(f"Transitioning to Screen 2 with selected_file_path: {Config.selected_file_path}")  # Debugging output
    window.destroy()
    import gui1  # Import and run Screen 2


# Initialize main window for Screen 1
window = TkinterDnD.Tk()
window.geometry("800x600")
window.configure(bg="#FFFFFF")

canvas = Canvas(window, bg="#FFFFFF", height=600, width=800, bd=0, highlightthickness=0, relief="ridge")
canvas.place(x=0, y=0)
image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(400.0, 300.0, image=image_image_1)

image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(400.0, 400.0, image=image_image_2)

canvas.create_text(265.0, 134.0, anchor="nw", text="Add Watermark", fill="#000000", font=("Inter Bold", -36))
canvas.create_text(336.0, 274.0, anchor="nw", text="or drag your files here", fill="#000000", font=("Inter", -12))
#Button
button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(image=button_image_1, borderwidth=0, highlightthickness=0, command=select_file, relief="flat")
button_1.place(x=248.0, y=187.0, width=305.0, height=30.0)

# Enable drag-and-drop on the window
window.drop_target_register(DND_FILES)
window.dnd_bind('<<Drop>>', on_drop)

window.resizable(False, False)
window.mainloop()
