# Section 1: Initialization & Configuration, Canvas & Image Display, Zooming & Dragging
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import Canvas, Label
import os

class CustomImageGallery(tk.Frame):
    def __init__(self, parent, img_path):
        super().__init__(parent)
        self.image = Image.open(img_path).convert('RGBA')
        self.zoom, self.dragging, self.dragging_watermark = 1.0, False, False
        self.watermark_alpha, self.watermark_color = 255, "#FFFFFF"
        self.watermark_size = 36
        self.has_watermark = False
        self.watermark_layer = None
        self.original_image = self.image.copy()
        self.control_panel_dragging = False  # New variable for control panel dragging
        
        # Set up canvas and initial image
        self.canvas = Canvas(self, bg="#2b2b2b", height=480, width=800)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Calculate initial image size
        canvas_ratio = 800 / 480
        img_ratio = self.image.width / self.image.height
        new_size = (800, int(800 / img_ratio)) if img_ratio > canvas_ratio else (int(480 * img_ratio), 480)
        self.base_image = self.image.resize(new_size, Image.Resampling.LANCZOS)
        self.image = self.base_image.copy()
        self.watermark_x, self.watermark_y = self.image.width // 2, self.image.height // 2
        
        # Initialize the image position at the center
        self.canvas_center_x = self.canvas.winfo_reqwidth() // 2
        self.canvas_center_y = self.canvas.winfo_reqheight() // 2
        
        self.update_display()
        self.zoom_label = Label(self, text="Zoom: 100%", bg="white")
        self.zoom_label.place(x=30, y=500, anchor='sw')
        
        # Initialize font
        self.font = self._get_default_font()
        
        # Bind events
        self._bind_events()
        
        # Bind canvas resize event to keep image centered
        self.canvas.bind('<Configure>', self._on_canvas_resize)

    def _get_default_font(self):
        """Try to load a system font, fallback to default if none available"""
        try:
            font_paths = [
                "C:/Windows/Fonts/arial.ttf",
                "C:/Windows/Fonts/segoeui.ttf",
                "/Library/Fonts/Arial.ttf",
                "/System/Library/Fonts/Helvetica.ttc",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                "/usr/share/fonts/TTF/arial.ttf"
            ]
            
            for font_path in font_paths:
                if os.path.exists(font_path):
                    return font_path
            return None
        except:
            return None


    def _on_canvas_resize(self, event):
        """Handle canvas resize to keep image centered"""
        if hasattr(self, 'img_id'):
            self.canvas_center_x = event.width // 2
            self.canvas_center_y = event.height // 2
            self.canvas.coords(self.img_id, self.canvas_center_x, self.canvas_center_y)

    def _bind_events(self):
        """Bind all necessary events"""
        events = {
            "<MouseWheel>": lambda e: self._handle_zoom(1.1 if e.delta > 0 else 0.9),
            "<Button-4>": lambda e: self._handle_zoom(1.1),
            "<Button-5>": lambda e: self._handle_zoom(0.9),
            "<ButtonPress-1>": self._start_drag,
            "<B1-Motion>": self._handle_drag,
            "<ButtonRelease-1>": self._stop_drag,
            "<Enter>": lambda e: self.canvas.config(cursor="hand2") if not self.dragging else None,
            "<Leave>": lambda e: self.canvas.config(cursor="arrow") if not self.dragging else None
        }
        for event, callback in events.items():
            self.canvas.bind(event, callback)

    def update_display(self):
        """Update the display with current image and watermark"""
        if self.watermark_layer:
            # Resize watermark layer to match current image size
            resized_watermark = self.watermark_layer.resize(self.image.size, Image.Resampling.LANCZOS)
            composite = Image.alpha_composite(self.image.convert('RGBA'), resized_watermark)
        else:
            composite = self.image
            
        self.img_tk = ImageTk.PhotoImage(composite)
        
        if not hasattr(self, 'img_id'):
            # Initialize image at the center of the canvas
            self.img_id = self.canvas.create_image(
                self.canvas.winfo_reqwidth() // 2,
                self.canvas.winfo_reqheight() // 2,
                image=self.img_tk,
                anchor='center'
            )
        else:
            self.canvas.itemconfig(self.img_id, image=self.img_tk)


    def _handle_zoom(self, factor):
        """Handle zoom with proper image scaling"""
        if self.has_watermark:
            return  # Disable zoom when control panel is open
            
        new_zoom = self.zoom * factor
        if 0.5 <= new_zoom <= 2.0:
            self.zoom = new_zoom
            self.zoom_label.config(text=f"Zoom: {int(self.zoom * 100)}%")
            
            # Calculate new image size based on zoom
            new_width = int(self.base_image.width * self.zoom)
            new_height = int(self.base_image.height * self.zoom)
            
            # Resize the image
            self.image = self.base_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            self.update_display()

    def _start_drag(self, event):
        self.prev_x, self.prev_y = event.x, event.y
        if self.has_watermark:
            img_bbox = self.canvas.bbox(self.img_id)
            if img_bbox:
                wx = self.watermark_x * self.zoom + img_bbox[0]
                wy = self.watermark_y * self.zoom + img_bbox[1]
                if abs(event.x - wx) < 50 and abs(event.y - wy) < 50:
                    self.dragging_watermark = True
                    return
        self.dragging = True
        self.canvas.config(cursor="hand2")

    def _handle_drag(self, event):
        if self.dragging_watermark:
            dx, dy = (event.x - self.prev_x) / self.zoom, (event.y - self.prev_y) / self.zoom
            self.watermark_x = max(0, min(self.watermark_x + dx, self.base_image.width))
            self.watermark_y = max(0, min(self.watermark_y + dy, self.base_image.height))
            self._update_watermark()
        elif self.dragging:
            x, y = self.canvas.coords(self.img_id)
            self.canvas.coords(self.img_id, x + event.x - self.prev_x, y + event.y - self.prev_y)
        self.prev_x, self.prev_y = event.x, event.y

    def _stop_drag(self, event):
        self.dragging = self.dragging_watermark = False
        self.canvas.config(cursor="arrow")


    def _start_control_panel_drag(self, event):
        """Start dragging the control panel"""
        self.control_panel_dragging = True
        widget = event.widget
        widget._drag_start_x = event.x
        widget._drag_start_y = event.y

    def _handle_control_panel_drag(self, event):
        """Handle control panel dragging"""
        if self.control_panel_dragging:
            widget = event.widget
            x = self.control_panel.winfo_x() + (event.x - widget._drag_start_x)
            y = self.control_panel.winfo_y() + (event.y - widget._drag_start_y)
            
            # Keep the control panel within the window bounds
            max_x = self.winfo_width() - self.control_panel.winfo_width()
            max_y = self.winfo_height() - self.control_panel.winfo_height()
            x = max(0, min(x, max_x))
            y = max(0, min(y, max_y))
            
            self.control_panel.place(x=x, y=y)

    def _stop_control_panel_drag(self, event):
        """Stop dragging the control panel"""
        self.control_panel_dragging = False
