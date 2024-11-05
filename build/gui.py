import os
import sys
from pathlib import Path
import customtkinter as ctk
from tkinter import filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
from config.config import Config
from PIL import Image, ImageTk
from customtkinter import CTkImage 

class WatermarkApp(TkinterDnD.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.selected_image_path = Config.selected_file_path
        self.output_path = Path(__file__).parent
        self.assets_path = self.output_path / Path(r"/run/media/ejarao/STORAGE/4 Dev Library/1 Src/build/assets/frame0")
        self._set_appearance_mode(Config.appearance_mode)
        self._set_default_theme(Config.theme)

        # Setup window
        self.geometry("800x600")
        self.title("Watermark Tool")
        self._create_widgets()
        self._bind_drag_and_drop()

    def _set_appearance_mode(self, mode):
        ctk.set_appearance_mode(mode)  # Set appearance mode: "dark" or "light"

    def _set_default_theme(self, theme):
        ctk.set_default_color_theme(theme)

    def _create_widgets(self):
        # Create a frame and other UI elements (buttons, labels, etc.)
        self.frame = ctk.CTkFrame(self, width=800, height=600)
        self.frame.place(x=0, y=0)

        self._add_image()
        self._add_labels()
        self._add_buttons()

    def _add_image(self):
        image_path = "build/assets/frame0/image_1.png"
        img = Image.open(image_path).convert("RGBA")
        image_resized = img.resize((600, 450), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image_resized)
        
        label = ctk.CTkLabel(self.frame, text='', image=photo)
        label.place(x=100.0, y=75.0)
        label.image = photo

    def _add_labels(self):
        title_color, subtitle_color, footer_color = Config._update_label_colors()

        # Title label
        title_label = ctk.CTkLabel(self.frame, text="Add Watermark", font=("Inter Bold", 36), text_color=title_color)
        title_label.place(x=265.0, y=225.0)

        # Subtitle label
        subtitle_label = ctk.CTkLabel(self.frame, text="or drag your files here", font=("Inter", 12), text_color=subtitle_color)
        subtitle_label.place(x=335.0, y=355.0)

        # Footer label
        footer_label = ctk.CTkLabel(self.frame, text="Files stay private. The program processes the files on the device.", font=("Inter", 12), text_color=footer_color)
        footer_label.place(x=215.0, y=455.0)

    def _add_buttons(self):
        # Select file button
        image_path = "build/assets/frame0/image.png"
        img = Image.open(image_path).resize((15, 15))
        tk_image = CTkImage(img)
        
        select_button = ctk.CTkButton(self.frame, text="Select File", width=305, height=60, text_color="black", image=tk_image, compound="left", command=self.select_file)
        select_button.place(x=246.0, y=278.0)

    def _bind_drag_and_drop(self):
        # Enable drag-and-drop
        self.drop_target_register(DND_FILES)
        self.dnd_bind('<<Drop>>', self.on_drop)



    def on_drop(self, event):
        file_path = event.data.strip('{}')
        print(f"File dropped: {file_path}")
        messagebox.showinfo("File Uploaded", f"File uploaded: {file_path}")
        Config.selected_file_path = file_path  # Update the global variable
        self.open_screen_2()

    def select_file(self):
        initial_dir = os.path.join(os.environ['USERPROFILE'], 'Pictures') if sys.platform.startswith('win') else os.path.expanduser('~/Pictures')
        file_path = filedialog.askopenfilename(initialdir=initial_dir, filetypes=[("All Files", "*.*")])
        
        if file_path and any(file_path.lower().endswith(ext) for ext in {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff'}):
            Config.selected_file_path = file_path
            print(f"File selected: {file_path}")
            messagebox.showinfo("File Selected", f"File selected: {file_path}")
            self.open_screen_2()
        else:
            messagebox.showwarning("Invalid File Type", "The selected file is not an image. Please select a valid image file.")

    def open_screen_2(self):
        print(f"Transitioning to Screen 2 with selected_file_path: {Config.selected_file_path}")
        self.destroy()
        import gui1  # Import and run Screen 2

if __name__ == "__main__":
    app = WatermarkApp()
    app.mainloop()
