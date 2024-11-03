import tkinter as tk
from PIL import Image, ImageTk
from tkinter import Canvas, Label


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

class CustomImageGallery(tk.Frame):
    def __init__(self, parent, img_path):
        super().__init__(parent)
        self.image = Image.open(img_path)
        self.zoom = 1.0
        self.prev_x = self.prev_y = 0
        self.dragging = False

        self.canvas = Canvas(self, bg="white", height=480, width=800)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        canvas_ratio = 800 / 480
        img_ratio = self.image.width / self.image.height

        if img_ratio > canvas_ratio:
            new_width = 800
            new_height = int(800 / img_ratio)
        else:
            new_height = 480
            new_width = int(480 * img_ratio)

        self.image = self.image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        self.img_tk = ImageTk.PhotoImage(self.image)
        self.img_id = self.canvas.create_image(400, 240, image=self.img_tk, anchor='center')

        self.zoom_label = Label(self, text=f"Zoom: {int(self.zoom * 100)}%", bg="white")
        self.zoom_label.place(x=30, y=440, anchor='sw')

        # Bind events
        self.canvas.bind("<MouseWheel>", lambda e: self._handle_zoom(1.1 if e.delta > 0 else 0.9))
        self.canvas.bind("<Button-4>", lambda e: self._handle_zoom(1.1))
        self.canvas.bind("<Button-5>", lambda e: self._handle_zoom(0.9))
        self.canvas.bind("<ButtonPress-1>", self._start_drag)
        self.canvas.bind("<B1-Motion>", self._handle_drag)
        self.canvas.bind("<ButtonRelease-1>", self._stop_drag)
        self.canvas.bind("<Enter>", self._on_enter)
        self.canvas.bind("<Leave>", self._on_leave)

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
        self.dragging = True
        self.canvas.config(cursor="hand2")

    def _stop_drag(self, event):
        self.dragging = False
        self.canvas.config(cursor="arrow")

    def _on_enter(self, event):
        if not self.dragging:
            self.canvas.config(cursor="hand2")

    def _on_leave(self, event):
        if not self.dragging:
            self.canvas.config(cursor="arrow")

    def _handle_drag(self, event):
        if not self.dragging:
            return

        dx = event.x - self.prev_x
        dy = event.y - self.prev_y
        
        # Get current position and dimensions
        x, y = self.canvas.coords(self.img_id)
        img_width = int(self.image.width * self.zoom)
        img_height = int(self.image.height * self.zoom)
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        # Calculate new position
        new_x = x + dx
        new_y = y + dy

        # Define minimum visible portion (pixels)
        min_visible = 400

        # Apply constraints to ensure minimum visibility
        # Left boundary
        if new_x + img_width/2 < min_visible:
            new_x = min_visible - img_width/2
        # Right boundary
        elif new_x - img_width/2 > canvas_width - min_visible:
            new_x = canvas_width - min_visible + img_width/2
        # Top boundary
        if new_y + img_height/2 < min_visible:
            new_y = min_visible - img_height/2
        # Bottom boundary
        elif new_y - img_height/2 > canvas_height - min_visible:
            new_y = canvas_height - min_visible + img_height/2

        # Update position
        self.canvas.coords(self.img_id, new_x, new_y)
        
        # Update previous position
        self.prev_x = event.x
        self.prev_y = event.y

    def _center_image(self):
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        x = canvas_width // 2
        y = canvas_height // 2
        self.canvas.coords(self.img_id, x, y)