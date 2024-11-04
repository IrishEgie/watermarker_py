import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageFont
from tkinter import Canvas, Label, Scale, Entry, Frame
import os

class CustomImageGallery(tk.Frame):
    def __init__(self, parent, img_path):
        super().__init__(parent)
        self.image = Image.open(img_path).convert('RGBA')
        self.zoom, self.dragging, self.dragging_watermark = 1.0, False, False
        self.watermark_alpha, self.watermark_color = 255, "#FFFFFF"
        self.watermark_size = 24  # Initialize watermark_size here
        self.has_watermark = False
        self.watermark_layer = None
        
        # Set up canvas and initial image
        self.canvas = Canvas(self, bg="black", height=480, width=800)
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

    def _validate_font_size(self, event=None):
        """Validate font size input and update watermark"""
        try:
            current = self.size_entry.get().strip()
            if current == "":
                return
                
            size = int(current)
            print(f"Validating font size: {size}")
            old_size = self.watermark_size
            
            # Update size within bounds
            if 12 <= size <= 72:
                self.watermark_size = size
            elif size < 12:
                self.watermark_size = 12
                self.size_entry.delete(0, tk.END)
                self.size_entry.insert(0, "12")
            elif size > 72:
                self.watermark_size = 72
                self.size_entry.delete(0, tk.END)
                self.size_entry.insert(0, "72")
            
            print(f"Size changed from {old_size} to {self.watermark_size}")
            
            # Force watermark redraw
            self._recreate_watermark()
                
        except ValueError as e:
            print(f"Value error in font size validation: {e}")
            self.size_entry.delete(0, tk.END)
            self.size_entry.insert(0, str(self.watermark_size))
            
    def _recreate_watermark(self):
        """Completely recreate the watermark layer with current settings"""
        if not self.has_watermark:
            return
            
        print(f"Recreating watermark with size: {self.watermark_size}")
            
        # Create fresh watermark layer
        self.watermark_layer = Image.new('RGBA', self.image.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(self.watermark_layer)
        
        # Get current parameters
        text = self.watermark_entry.get()
        color = self.color_entry.get()
        alpha = int(self.alpha_slider.get() * 2.55)
        scaled_size = int(self.watermark_size * self.zoom)
        
        print(f"Drawing text with scaled size: {scaled_size}")
        
        # Process color
        if len(color) == 7:
            r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
            color = (r, g, b, alpha)
        
        # Load font
        try:
            if self.font:
                font = ImageFont.truetype(self.font, scaled_size)
                print(f"Loaded font: {self.font} at size {scaled_size}")
            else:
                font = ImageFont.load_default()
                print("Using default font")
        except Exception as e:
            print(f"Font error: {e}")
            font = ImageFont.load_default()
        
        # Calculate text position
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        screen_x = int(self.watermark_x * self.zoom)
        screen_y = int(self.watermark_y * self.zoom)
        
        x = max(0, min(screen_x - text_width // 2, self.image.width - text_width))
        y = max(0, min(screen_y - text_height // 2, self.image.height - text_height))
        
        # Draw watermark
        draw.text((x, y), text, font=font, fill=color)
        print(f"Drew text at position ({x}, {y})")
        
        # Update display
        self.update_display()

    def _update_watermark(self, event=None):
        """Update watermark in response to changes"""
        self._recreate_watermark()

    def add_watermark_controls(self):
        if self.has_watermark:
            return
            
        self.control_panel = Frame(self, bg="white", relief="raised", borderwidth=1)
        self.control_panel.place(x=20, y=20, width=180, height=300)
        
        controls = [
            ("Watermark Opacity", Scale, {"from_": 0, "to": 100, "orient": "horizontal", "command": self._update_watermark, "length": 150}),
            ("Font Size", Entry, {"width": 20}),
            ("Watermark Text", Entry, {"width": 20}),
            ("Watermark Color", Entry, {"width": 20})
        ]
        
        for i, (text, widget_class, props) in enumerate(controls):
            label = Label(self.control_panel, text=text, bg="white", anchor='w', width=20)
            label.pack(pady=(10 if i == 0 else 0, 0), anchor='w')
            widget = widget_class(self.control_panel, **props)
            
            # Set initial values
            if widget_class == Scale:
                widget.set(100)
            else:
                initial_value = {
                    "Font Size": str(self.watermark_size),
                    "Watermark Text": "Watermark",
                    "Watermark Color": "#FFFFFF"
                }.get(text, "")
                widget.insert(0, initial_value)
                
                if text == "Font Size":
                    widget.bind('<Return>', self._validate_font_size)
                    widget.bind('<FocusOut>', self._validate_font_size)
                else:
                    widget.bind('<Return>', self._update_watermark)
                    widget.bind('<FocusOut>', self._update_watermark)
            
            widget.pack(pady=(0, 10))
            
            # Store references
            if text == "Watermark Opacity":
                self.alpha_slider = widget
            elif text == "Font Size":
                self.size_entry = widget
            elif text == "Watermark Text":
                self.watermark_entry = widget
            elif text == "Watermark Color":
                self.color_entry = widget
        
        self.has_watermark = True
        self.watermark_layer = Image.new('RGBA', self.image.size, (0, 0, 0, 0))
        self._update_watermark()

    def _update_watermark(self, event=None):
        if not self.has_watermark or not self.watermark_layer:
            return
            
        self.watermark_layer = Image.new('RGBA', self.image.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(self.watermark_layer)
        
        # Get current watermark parameters
        text = self.watermark_entry.get()
        color = self.color_entry.get()
        alpha = int(self.alpha_slider.get() * 2.55)
        
        # Use the stored watermark_size directly
        scaled_size = int(self.watermark_size * self.zoom)
        
        # Process color with alpha
        if len(color) == 7:
            r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
            color = (r, g, b, alpha)
        
        # Load font with scaled size
        try:
            font = ImageFont.truetype(self.font, scaled_size) if self.font else ImageFont.load_default()
        except:
            font = ImageFont.load_default()
        
        # Calculate text boundaries with the scaled font
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        # Calculate position ensuring text stays within image bounds
        screen_x = int(self.watermark_x * self.zoom)
        screen_y = int(self.watermark_y * self.zoom)
        
        x = max(0, min(screen_x - text_width // 2, self.image.width - text_width))
        y = max(0, min(screen_y - text_height // 2, self.image.height - text_height))
        
        # Draw text at calculated position
        draw.text((x, y), text, font=font, fill=color)
        self.update_display()

    def update_display(self):
        """Update the display with current image and watermark"""
        if self.watermark_layer:
            composite = Image.alpha_composite(self.image.convert('RGBA'), self.watermark_layer)
        else:
            composite = self.image
            
        self.img_tk = ImageTk.PhotoImage(composite)
        
        if not hasattr(self, 'img_id'):
            self.img_id = self.canvas.create_image(400, 240, image=self.img_tk, anchor='center')
        else:
            self.canvas.itemconfig(self.img_id, image=self.img_tk)


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