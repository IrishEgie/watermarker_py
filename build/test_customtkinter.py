import os
import sys
from pathlib import Path
import customtkinter as ctk
from tkinter import filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
from config.config import Config  # Import the Config class

# Set up the output and asset paths
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

# Initialize main window for the application with dark theme
ctk.set_appearance_mode("auto")
ctk.set_default_color_theme("green")  # You can change the theme to your preference

window = TkinterDnD.Tk()
window.geometry("800x600")
window.title("Watermark Tool")

# Create a dark themed canvas-like container using CTkFrame
frame = ctk.CTkFrame(window, width=800, height=600)
frame.place(x=0, y=0)

# Label to replace "Add Watermark" text
title_label = ctk.CTkLabel(frame, text="Add Watermark", font=("Inter Bold", 36), text_color="white")
title_label.place(x=265.0, y=225.0)

# Subtitle text
subtitle_label = ctk.CTkLabel(frame, text="or drag your files here", font=("Inter", 12), text_color="white")
subtitle_label.place(x=335.0, y=355.0)

# Button to select files using CTkButton (replaces the old button with an image)
select_button = ctk.CTkButton(frame, text="Select File", width=305, height=60, command=select_file)
select_button.place(x=246.0, y=278.0)

# Footer text
footer_label = ctk.CTkLabel(frame, text="Files stay private. The program processes the files on the device.", font=("Inter", 12), text_color="gray")
footer_label.place(x=215.0, y=455.0)

# Enable drag-and-drop on the window
window.drop_target_register(DND_FILES)
window.dnd_bind('<<Drop>>', on_drop)

# Make the window non-resizable
window.resizable(False, False)

# Start the tkinter main loop
window.mainloop()
