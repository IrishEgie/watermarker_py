import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image, ImageDraw, ImageFont

def create_main_window():
    window = TkinterDnD.Tk()
    window.title("Image Watermarking Tool")
    window.geometry("400x300")
    return window

def upload_image(file_path=None):
    if not file_path:
        file_path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    
    if file_path:
        img = Image.open(file_path)
        return img
    return None

def add_watermark(image, text="Sample Watermark"):
    watermark = Image.new("RGBA", image.size)
    draw = ImageDraw.Draw(watermark)
    font = ImageFont.load_default()
    text_width, text_height = draw.textsize(text, font)
    position = (image.width - text_width - 10, image.height - text_height - 10)
    draw.text(position, text, fill=(255, 255, 255, 128), font=font)
    watermarked = Image.alpha_composite(image.convert("RGBA"), watermark)
    return watermarked.convert("RGB")

def save_image(image):
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
    if file_path:
        image.save(file_path)
        messagebox.showinfo("Success", "Image saved successfully!")

def drop(event):
    file_path = event.data
    img = upload_image(file_path)
    if img:
        messagebox.showinfo("Success", "Image loaded successfully!")

def main():
    window = create_main_window()

    # Bind drag-and-drop functionality
    window.drop_target_register(DND_FILES)
    window.dnd_bind('<<Drop>>', drop)

    upload_btn = tk.Button(window, text="Upload Image", command=lambda: upload_image())
    upload_btn.pack(pady=10)

    watermark_btn = tk.Button(window, text="Add Watermark", command=lambda: add_watermark(img))
    watermark_btn.pack(pady=10)

    save_btn = tk.Button(window, text="Save Image", command=lambda: save_image(img))
    save_btn.pack(pady=10)

    window.mainloop()

if __name__ == "__main__":
    main()
