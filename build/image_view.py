import tkinter as tk
from PIL import Image, ImageTk
from tkinter import Canvas, Label, Scale, Entry, Frame

class CustomImageGallery(tk.Frame):
    def __init__(self, parent, img_path):
        super().__init__(parent)
        self.image = Image.open(img_path)
        self.zoom = 1.0
        self.dragging = False
        self.dragging_watermark = False
        self.watermark_alpha = 255  # Full opacity (0-255)
        self.watermark_color = "#000000"  # Default black
        self.has_watermark = False

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
        self.zoom_label.place(x=30, y=500, anchor='sw')

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

    def add_watermark_controls(self):
        """Add watermark controls to the interface"""
        if not self.has_watermark:
            # Create control panel frame
            self.control_panel = Frame(self, bg="white", relief="raised", borderwidth=1)
            self.control_panel.place(x=600, y=20, width=180, height=200)
            
            # Opacity controls
            Label(self.control_panel, text="Watermark Opacity", bg="white").pack(pady=(10,0))
            self.alpha_slider = Scale(
                self.control_panel,
                from_=0,
                to=100,
                orient="horizontal",
                command=self._update_watermark_alpha,
                length=150
            )
            self.alpha_slider.set(100)
            self.alpha_slider.pack(pady=(0,10))
            
            # Text input
            Label(self.control_panel, text="Watermark Text", bg="white").pack()
            self.watermark_entry = Entry(self.control_panel, width=20)
            self.watermark_entry.insert(0, "Watermark")
            self.watermark_entry.pack(pady=(0,10))
            self.watermark_entry.bind('<Return>', self._update_watermark_text)
            
            # Color input
            Label(self.control_panel, text="Watermark Color", bg="white").pack()
            self.color_entry = Entry(self.control_panel, width=20)
            self.color_entry.insert(0, "#FFFFFF")  # Default white
            self.color_entry.pack(pady=(0,10))
            self.color_entry.bind('<Return>', self._update_watermark_color)
            
            # Create watermark text on canvas
            self.watermark_id = self.canvas.create_text(
                400, 240,
                text=self.watermark_entry.get(),
                fill=self.color_entry.get(),
                font=('Arial', 24),
                tags="watermark"
            )
            
            # Bind watermark dragging events
            self.canvas.tag_bind("watermark", "<ButtonPress-1>", self._start_watermark_drag)
            self.canvas.tag_bind("watermark", "<B1-Motion>", self._handle_watermark_drag)
            self.canvas.tag_bind("watermark", "<ButtonRelease-1>", self._stop_watermark_drag)
            
            self.has_watermark = True

    def _update_watermark_alpha(self, value):
        """Update watermark opacity"""
        alpha_hex = format(int(int(value) * 2.55), '02x')  # Convert 0-100 to hex alpha
        color = self.color_entry.get()
        if len(color) == 7:  # If color is in #RRGGBB format
            color = color + alpha_hex
        elif len(color) == 9:  # If color already has alpha
            color = color[:7] + alpha_hex
        self.canvas.itemconfig(self.watermark_id, fill=color)

    def _update_watermark_color(self, event=None):
        """Update watermark color"""
        color = self.color_entry.get()
        if len(color) == 7:  # If color is in #RRGGBB format
            alpha_value = self.alpha_slider.get()
            alpha_hex = format(int(alpha_value * 2.55), '02x')
            color = color + alpha_hex
        self.canvas.itemconfig(self.watermark_id, fill=color)

    def _update_watermark_text(self, event=None):
        """Update watermark text"""
        self.canvas.itemconfig(self.watermark_id, text=self.watermark_entry.get())

    def _start_watermark_drag(self, event):
        self.dragging_watermark = True
        self.prev_x, self.prev_y = event.x, event.y
        return "break"

    def _handle_watermark_drag(self, event):
        if not self.dragging_watermark:
            return
            
        # Calculate new position
        dx, dy = event.x - self.prev_x, event.y - self.prev_y
        x, y = self.canvas.coords(self.watermark_id)
        
        # Get image bounds
        img_bbox = self.canvas.bbox(self.img_id)
        if not img_bbox:
            return
            
        new_x = x + dx
        new_y = y + dy
        
        # Constrain watermark within image bounds
        new_x = min(max(new_x, img_bbox[0]), img_bbox[2])
        new_y = min(max(new_y, img_bbox[1]), img_bbox[3])
        
        # Update position
        self.canvas.coords(self.watermark_id, new_x, new_y)
        self.prev_x, self.prev_y = event.x, event.y
        return "break"

    def _stop_watermark_drag(self, event):
        self.dragging_watermark = False
        return "break"
    
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
        if not self.dragging_watermark:  # Only start image drag if not dragging watermark
            self.prev_x, self.prev_y = event.x, event.y
            self.dragging = True
            self.canvas.config(cursor="hand2")

    def _handle_drag(self, event):
        if not self.dragging or self.dragging_watermark:
            return
        
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