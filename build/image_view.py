import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageFont
from tkinter import Canvas, Label, Scale, Entry, Frame
import os

class CustomImageGallery(tk.Frame):
    def __init__(self, parent, img_path):
        super().__init__(parent)
        self.image = Image.open(img_path).convert('RGBA')
        self.zoom, self.dragging, self.dragging_watermark = 1.0, False, False
        self.watermark_alpha, self.watermark_color, self.watermark_size = 255, "#FFFFFF", 24
        self.has_watermark = False
        self.watermark_layer = None
        
        # Set up canvas and initial image
        self.canvas = Canvas(self, bg="white", height=480, width=800)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Calculate initial image size
        canvas_ratio = 800 / 480
        img_ratio = self.image.width / self.image.height
        new_size = (800, int(800 / img_ratio)) if img_ratio > canvas_ratio else (int(480 * img_ratio), 480)
        self.base_image = self.image.resize(new_size, Image.Resampling.LANCZOS)
        self.image = self.base_image.copy()
        self.watermark_x, self.watermark_y = self.image.width // 2, self.image.height // 2
        
        self.update_display()
        self.zoom_label = Label(self, text="Zoom: 100%", bg="white")
        self.zoom_label.place(x=30, y=500, anchor='sw')
        
        # Initialize font
        self.font = self._get_default_font()
        
        # Bind events
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

    def _get_default_font(self):
        """Try to load a system font, fallback to default if none available"""
        try:
            # Try different common font paths
            font_paths = [
                # Windows fonts
                "C:/Windows/Fonts/arial.ttf",
                "C:/Windows/Fonts/segoeui.ttf",
                # macOS fonts
                "/Library/Fonts/Arial.ttf",
                "/System/Library/Fonts/Helvetica.ttc",
                # Linux fonts
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                "/usr/share/fonts/TTF/arial.ttf"
            ]
            
            for font_path in font_paths:
                if os.path.exists(font_path):
                    return font_path
            
            # If no system fonts found, return None to use default
            return None
        except:
            return None

    def update_display(self):
        composite = Image.alpha_composite(self.image.convert('RGBA'), self.watermark_layer) if self.watermark_layer else self.image
        self.img_tk = ImageTk.PhotoImage(composite)
        if not hasattr(self, 'img_id'):
            self.img_id = self.canvas.create_image(400, 240, image=self.img_tk, anchor='center')
        else:
            self.canvas.itemconfig(self.img_id, image=self.img_tk)

    def add_watermark_controls(self):
        if self.has_watermark: return
        self.control_panel = Frame(self, bg="white", relief="raised", borderwidth=1)
        self.control_panel.place(x=20, y=20, width=180, height=300)
        
        controls = [
            ("Watermark Opacity", Scale, {"from_": 0, "to": 100, "orient": "horizontal", "command": self._update_watermark, "length": 150}),
            ("Text Size", Scale, {"from_": 12, "to": 72, "orient": "horizontal", "command": lambda v: self._update_watermark(None), "length": 150}),
            ("Watermark Text", Entry, {"width": 20}),
            ("Watermark Color", Entry, {"width": 20})
        ]
        
        for i, (text, widget_class, props) in enumerate(controls):
            Label(self.control_panel, text=text, bg="white").pack(pady=(10 if i == 0 else 0, 0))
            widget = widget_class(self.control_panel, **props)
            if widget_class == Scale:
                widget.set(100 if i == 0 else self.watermark_size)
            else:
                widget.insert(0, "Watermark" if i == 2 else "#FFFFFF")
                widget.bind('<Return>', self._update_watermark)
            widget.pack(pady=(0, 10))
            setattr(self, f"{'alpha_slider' if i == 0 else 'size_slider' if i == 1 else 'watermark_entry' if i == 2 else 'color_entry'}", widget)
        
        Label(self.control_panel, text="Click and drag watermark\nto reposition", bg="white", justify="center").pack(pady=(10,0))
        self.has_watermark = True
        self.watermark_layer = Image.new('RGBA', self.image.size, (0, 0, 0, 0))
        self._update_watermark()

    def _update_watermark(self, event=None):
        if not self.has_watermark or not self.watermark_layer: return
        self.watermark_layer = Image.new('RGBA', self.image.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(self.watermark_layer)
        
        text = self.watermark_entry.get()
        color = self.color_entry.get()
        alpha = int(self.alpha_slider.get() * 2.55)
        size = int(self.size_slider.get() * self.zoom)
        
        if len(color) == 7:
            r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
            color = (r, g, b, alpha)
        
        # Use system font if available, otherwise fall back to default
        try:
            font = ImageFont.truetype(self.font, size) if self.font else ImageFont.load_default()
        except:
            font = ImageFont.load_default()
            
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
        
        x = max(0, min(int(self.watermark_x * self.zoom) - text_width // 2, self.image.width - text_width))
        y = max(0, min(int(self.watermark_y * self.zoom) - text_height // 2, self.image.height - text_height))
        
        draw.text((x, y), text, font=font, fill=color)
        self.update_display()

    def _handle_zoom(self, factor):
        new_zoom = self.zoom * factor
        if 0.5 <= new_zoom <= 2.0:
            self.zoom = new_zoom
            self.zoom_label.config(text=f"Zoom: {int(self.zoom * 100)}%")
            self.update_display()
            self.canvas.coords(self.img_id, self.canvas.winfo_width() // 2, self.canvas.winfo_height() // 2)

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