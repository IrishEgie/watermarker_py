import tkinter as tk
from PIL import Image, ImageTk

class ImageGallery(tk.Tk):
    def __init__(self, image_path):
        super().__init__()
        self.image_path = image_path
        self.image = Image.open(self.image_path)
        self.zoom_factor = 1.0

        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.img_tk = ImageTk.PhotoImage(self.image)
        self.image_id = self.canvas.create_image(0, 0, image=self.img_tk, anchor='nw')

        self.bind("<MouseWheel>", self.zoom)
        self.canvas.bind("<ButtonPress-1>", self.start_drag)
        self.canvas.bind("<B1-Motion>", self.do_drag)

        self.prev_x = 0
        self.prev_y = 0

    def zoom(self, event):
        if event.delta > 0:  # Zoom in
            self.zoom_factor *= 1.1
        else:  # Zoom out
            self.zoom_factor /= 1.1
        
        new_size = (int(self.image.width * self.zoom_factor), int(self.image.height * self.zoom_factor))
        resized_image = self.image.resize(new_size, Image.LANCZOS)
        self.img_tk = ImageTk.PhotoImage(resized_image)
        self.canvas.itemconfig(self.image_id, image=self.img_tk)

    def start_drag(self, event):
        self.prev_x = event.x
        self.prev_y = event.y

    def do_drag(self, event):
        dx = event.x - self.prev_x
        dy = event.y - self.prev_y
        self.canvas.move(self.image_id, dx, dy)
        self.prev_x = event.x
        self.prev_y = event.y

if __name__ == "__main__":
    app = ImageGallery("build/assets/frame0/image_1.png")
    app.geometry("800x600")
    app.mainloop()
