import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
from tkinter import Canvas, Label, Scale, Entry, Frame

class CustomImageGallery(tk.Frame):
    def __init__(self, parent, img_path):
        super().__init__(parent)
        self.image = Image.open(img_path)
        self.zoom = 1.0
        self.dragging = False
        self.dragging_watermark = False
        self.watermark_alpha = 255
        self.watermark_color = "#FFFFFF"
        self.watermark_size = 24  # Default font size
        self.has_watermark = False
        self.watermark_layer = None  # Store the watermark overlay
        
        # Convert image to RGBA if it isn't already
        if self.image.mode != 'RGBA':
            self.image = self.image.convert('RGBA')

        # Set up canvas and resize image to fit
        self.canvas = Canvas(self, bg="white", height=480, width=800)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Calculate initial image size to maintain aspect ratio
        canvas_ratio, img_ratio = 800 / 480, self.image.width / self.image.height
        new_size = (800, int(800 / img_ratio)) if img_ratio > canvas_ratio else (int(480 * img_ratio), 480)
        self.image = self.image.resize(new_size, Image.Resampling.LANCZOS)
        
        # Create and position image
        self.update_display()
        
        # Create zoom indicator
        self.zoom_label = Label(self, text="Zoom: 100%", bg="white")
        self.zoom_label.place(x=30, y=500, anchor='sw')

        # Bind all events
        self._bind_events()

    def _bind_events(self):
        """Bind all necessary events to the canvas"""
        event_bindings = {
            "<MouseWheel>": lambda e: self._handle_zoom(1.1 if e.delta > 0 else 0.9),
            "<Button-4>": lambda e: self._handle_zoom(1.1),
            "<Button-5>": lambda e: self._handle_zoom(0.9),
            "<ButtonPress-1>": self._start_drag,
            "<B1-Motion>": self._handle_drag,
            "<ButtonRelease-1>": self._stop_drag,
            "<Enter>": lambda e: self.canvas.config(cursor="hand2") if not self.dragging else None,
            "<Leave>": lambda e: self.canvas.config(cursor="arrow") if not self.dragging else None
        }
        
        for event, callback in event_bindings.items():
            self.canvas.bind(event, callback)
            
    def update_display(self):
        """Update the displayed image with watermark overlay"""
        if self.watermark_layer:
            # Composite the main image with the watermark layer
            composite = Image.alpha_composite(self.image.convert('RGBA'), self.watermark_layer)
            self.img_tk = ImageTk.PhotoImage(composite)
        else:
            self.img_tk = ImageTk.PhotoImage(self.image)
        
        if not hasattr(self, 'img_id'):
            self.img_id = self.canvas.create_image(400, 240, image=self.img_tk, anchor='center')
        else:
            self.canvas.itemconfig(self.img_id, image=self.img_tk)

    def add_watermark_controls(self):
        """Add watermark controls to the interface"""
        if not self.has_watermark:
            # Create control panel frame on the left side
            self.control_panel = Frame(self, bg="white", relief="raised", borderwidth=1)
            self.control_panel.place(x=20, y=20, width=180, height=300)
            
            # Opacity controls
            Label(self.control_panel, text="Watermark Opacity", bg="white").pack(pady=(10,0))
            self.alpha_slider = Scale(
                self.control_panel,
                from_=0,
                to=100,
                orient="horizontal",
                command=self._update_watermark,
                length=150
            )
            self.alpha_slider.set(100)
            self.alpha_slider.pack(pady=(0,10))
            
            # Text size controls
            Label(self.control_panel, text="Text Size", bg="white").pack()
            self.size_slider = Scale(
                self.control_panel,
                from_=12,
                to=72,
                orient="horizontal",
                command=lambda v: self._update_watermark(None),
                length=150
            )
            self.size_slider.set(self.watermark_size)
            self.size_slider.pack(pady=(0,10))
            
            # Text input
            Label(self.control_panel, text="Watermark Text", bg="white").pack()
            self.watermark_entry = Entry(self.control_panel, width=20)
            self.watermark_entry.insert(0, "Watermark")
            self.watermark_entry.pack(pady=(0,10))
            self.watermark_entry.bind('<Return>', self._update_watermark)
            
            # Color input
            Label(self.control_panel, text="Watermark Color", bg="white").pack()
            self.color_entry = Entry(self.control_panel, width=20)
            self.color_entry.insert(0, "#FFFFFF")
            self.color_entry.pack(pady=(0,10))
            self.color_entry.bind('<Return>', self._update_watermark)
            
            self.has_watermark = True
            self._create_watermark_layer()

    def _create_watermark_layer(self):
        """Create a transparent layer for the watermark"""
        self.watermark_layer = Image.new('RGBA', self.image.size, (0, 0, 0, 0))
        self._update_watermark()

    def _update_watermark(self, event=None):
        """Update watermark appearance"""
        if not self.has_watermark or not self.watermark_layer:
            return
            
        # Create new transparent layer
        self.watermark_layer = Image.new('RGBA', self.image.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(self.watermark_layer)
        
        # Get current settings
        text = self.watermark_entry.get()
        color = self.color_entry.get()
        alpha = int(self.alpha_slider.get() * 2.55)  # Convert 0-100 to 0-255
        size = int(self.size_slider.get())
        
        # Convert color to RGBA
        if len(color) == 7:  # #RRGGBB format
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)
            color = (r, g, b, alpha)
        
        # Calculate text position (center of image)
        try:
            from PIL import ImageFont
            font = ImageFont.truetype("arial.ttf", size)
        except:
            font = ImageFont.load_default()
            
        # Get text size for centering
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        x = (self.image.width - text_width) // 2
        y = (self.image.height - text_height) // 2
        
        # Draw text
        draw.text((x, y), text, font=font, fill=color)
        
        # Update display
        self.update_display()

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