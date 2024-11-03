import tkinter as tk
from PIL import Image, ImageTk
from tkinter import Canvas, Label

class CustomImageGallery(tk.Frame):
    def __init__(self, parent, img_path):
        super().__init__(parent)
        self.image = Image.open(img_path)
        self.zoom = 1.0
        self.dragging = False

        # Set up canvas and resize image to fit
        self.canvas = Canvas(self, bg="white", height=480, width=800)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Calculate initial image size to maintain aspect ratio
        canvas_ratio, img_ratio = 800 / 480, self.image.width / self.image.height
        new_size = (800, int(800 / img_ratio)) if img_ratio > canvas_ratio else (int(480 * img_ratio), 480)
        self.image = self.image.resize(new_size, Image.Resampling.LANCZOS)
        
        # Create and position image
        self.img_tk = ImageTk.PhotoImage(self.image)
        self.img_id = self.canvas.create_image(400, 240, image=self.img_tk, anchor='center')
        
        # Create zoom indicator
        self.zoom_label = Label(self, text="Zoom: 100%", bg="white")
        self.zoom_label.place(x=30, y=440, anchor='sw')
        
        # Bind all events
        for event, callback in {
            "<MouseWheel>": lambda e: self._handle_zoom(1.1 if e.delta > 0 else 0.9),
            "<Button-4>": lambda e: self._handle_zoom(1.1),
            "<Button-5>": lambda e: self._handle_zoom(0.9),
            "<ButtonPress-1>": self._start_drag,
            "<B1-Motion>": self._handle_drag,
            "<ButtonRelease-1>": self._stop_drag,
            "<Enter>": lambda e: self.canvas.config(cursor="hand2") if not self.dragging else None,
            "<Leave>": lambda e: self.canvas.config(cursor="arrow") if not self.dragging else None
        }.items():
            self.canvas.bind(event, callback)

    def _handle_zoom(self, factor):
        # Update zoom and resize image if within bounds
        new_zoom = self.zoom * factor
        if 0.5 <= new_zoom <= 2.0:
            self.zoom = new_zoom
            new_size = tuple(int(d * self.zoom) for d in self.image.size)
            self.img_tk = ImageTk.PhotoImage(self.image.resize(new_size, Image.Resampling.LANCZOS))
            self.canvas.itemconfig(self.img_id, image=self.img_tk)
            self.zoom_label.config(text=f"Zoom: {int(self.zoom * 100)}%")
            self._center_image()

    def _start_drag(self, event):
        self.prev_x, self.prev_y = event.x, event.y
        self.dragging = True
        self.canvas.config(cursor="hand2")

    def _handle_drag(self, event):
        if not self.dragging: return
        
        # Calculate new position
        dx, dy = event.x - self.prev_x, event.y - self.prev_y
        x, y = self.canvas.coords(self.img_id)
        img_width, img_height = int(self.image.width * self.zoom), int(self.image.height * self.zoom)
        canvas_width, canvas_height = self.canvas.winfo_width(), self.canvas.winfo_height()
        new_x, new_y = x + dx, y + dy
        min_visible = 450  # Minimum pixels that must remain visible
        
        # Apply boundary constraints
        new_x = min(canvas_width - min_visible + img_width/2, max(min_visible - img_width/2, new_x))
        new_y = min(canvas_height - min_visible + img_height/2, max(min_visible - img_height/2, new_y))
        
        # Update position
        self.canvas.coords(self.img_id, new_x, new_y)
        self.prev_x, self.prev_y = event.x, event.y

    def _stop_drag(self, event):
        self.dragging = False
        self.canvas.config(cursor="arrow")

    def _center_image(self):
        self.canvas.coords(self.img_id, self.canvas.winfo_width() // 2, self.canvas.winfo_height() // 2)