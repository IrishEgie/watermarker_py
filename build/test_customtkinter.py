import customtkinter as ctk
from pathlib import Path
from tkinter import filedialog, messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES
import os
import sys
from config.config import Config  # Import the Config class
from PIL import Image, ImageTk  # Import PIL.Image and ImageTk to handle images

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"/run/media/ejarao/STORAGE/4 Dev Library/1 Src/build/assets/frame0")

selected_image_path = Config.selected_file_path

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def on_drop(event):
    global selected_image_path
    file_path = event.data.strip('{}')
    print(f"File dropped: {file_path}")
    messagebox.showinfo("File Uploaded", f"File uploaded: {file_path}")
    Config.selected_file_path = file_path  # Update the global variable
    open_screen_2()

def select_file():
    global selected_image_path
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

# Initialize main window for the application
window = TkinterDnD.Tk()
window.geometry("800x600")
# Set the title
window.title("Watermarking Tool")

# Set appearance mode to system default (auto will adjust to the system's theme)
ctk.set_appearance_mode("auto")

# Load the background image using PIL and convert it to PhotoImage for Tkinter
image_path = relative_to_assets("image_1.png")
pil_image = Image.open(image_path)  # Open the image using PIL
background_image = ImageTk.PhotoImage(pil_image)  # Convert to PhotoImage for Tkinter
# Store the image in a global variable to prevent garbage collection
window.background_image = background_image  # Persist the image object

# Create a Canvas widget for background and positioning
canvas = ctk.CTkCanvas(window, height=600, width=800, bd=0, highlightthickness=0, relief="ridge")
canvas.pack(fill="both", expand=True)

# Set the background image on the canvas, ensuring it is centered
canvas.create_image(400, 300, anchor="center", image=window.background_image)

# Add background image and texts
canvas.create_text(265.0, 225.0, anchor="nw", text="Add Watermark", fill="#000000", font=("Inter Bold", 36 * -1))
canvas.create_text(335.0, 355.0, anchor="nw", text="or drag your files here", fill="#000000", font=("Inter", 12 * -1))

button_1 = ctk.CTkButton(
    window,
    text="Select Image File",
    height=60,
    width=305,
    font=("Inter", 14),
    command=select_file,
    fg_color="#FFD700",  # Yellow background
    hover_color="#FFCC00",  # Slightly darker yellow when hovering
    text_color="black"  # Black text color
)

button_1.place(x=246.0, y=278.0)
# Footer text
canvas.create_text(215.0, 455.0, anchor="nw", text="Files stay private. The program processes the files on the device.", fill="#575757", font=("Inter", 12 * -1))

# Enable drag-and-drop on the window
window.drop_target_register(DND_FILES)
window.dnd_bind('<<Drop>>', on_drop)

# Run the application
window.resizable(False, False)
window.mainloop()
