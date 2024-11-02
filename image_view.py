import tkinter as tk
from PIL import Image, ImageTk

class ImageGallery(tk.Tk):
    def __init__(self, img_path):
        super().__init__()
        self.image = Image.open(img_path)
        self.zoom = 1.0
        self.prev_x = self.prev_y = 0
        self.limits = {'l': 150, 'r': 150, 't': 150, 'b': 150}
        
        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.img_tk = ImageTk.PhotoImage(self.image)
        self.img_id = self.canvas.create_image(0, 0, image=self.img_tk, anchor='nw')
        
        self.zoom_label = tk.Label(self, text=f"Zoom: {int(self.zoom * 100)}%", bg="white")
        self.zoom_label.place(x=30, y=self.winfo_height() - 30, anchor='sw')
        
        self.bind("<MouseWheel>", lambda e: self._handle_zoom(1.1 if e.delta > 0 else 0.9))
        self.bind("<Button-4>", lambda e: self._handle_zoom(1.1))
        self.bind("<Button-5>", lambda e: self._handle_zoom(0.9))
        self.bind("<Configure>", lambda e: self.zoom_label.place(x=30, y=self.winfo_height() - 30, anchor='sw'))
        self.canvas.bind("<ButtonPress-1>", lambda e: setattr(self, 'prev_x', e.x) or setattr(self, 'prev_y', e.y))
        self.canvas.bind("<B1-Motion>", self._handle_drag)

    def _handle_zoom(self, factor):
        new_zoom = self.zoom * factor
        if 0.5 <= new_zoom <= 2.0:
            self.zoom = new_zoom
            new_size = tuple(int(d * self.zoom) for d in (self.image.width, self.image.height))
            self.img_tk = ImageTk.PhotoImage(self.image.resize(new_size, Image.LANCZOS))
            self.canvas.itemconfig(self.img_id, image=self.img_tk)
            self.zoom_label.config(text=f"Zoom: {int(self.zoom * 100)}%")
            self._center_image()

    def _handle_drag(self, event):
        dx, dy = event.x - self.prev_x, event.y - self.prev_y
        self.canvas.move(self.img_id, dx, dy)
        
        x, y = self.canvas.coords(self.img_id)
        w, h = map(int, (self.image.width * self.zoom, self.image.height * self.zoom))
        cw, ch = self.canvas.winfo_width(), self.canvas.winfo_height()
        
        adjustments = [
            (x > self.limits['l'], self.limits['l'] - x, 0),
            (x + w < cw - self.limits['r'], cw - self.limits['r'] - (x + w), 0),
            (y > self.limits['t'], 0, self.limits['t'] - y),
            (y + h < ch - self.limits['b'], 0, ch - self.limits['b'] - (y + h))
        ]
        
        for condition, dx, dy in adjustments:
            if condition:
                self.canvas.move(self.img_id, dx, dy)
        
        self.prev_x, self.prev_y = event.x, event.y

    def _center_image(self):
        x, y = self.canvas.coords(self.img_id)
        w, h = map(int, (self.image.width * self.zoom, self.image.height * self.zoom))
        self.canvas.coords(self.img_id, (self.canvas.winfo_width() - w) // 2, (self.canvas.winfo_height() - h) // 2)

if __name__ == "__main__":
    app = ImageGallery("build/assets/frame0/image_1.png")
    app.geometry("800x600")
    app.mainloop()