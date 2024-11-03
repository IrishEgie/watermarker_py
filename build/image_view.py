import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageFont
from tkinter import Canvas, Label, filedialog
import os

class CustomImageGallery(tk.Frame):
    def __init__(self, parent, img_path):
        super().__init__(parent)
        self.original_image = Image.open(img_path)  # Store original image
        self.image = self.original_image.copy()     # Working copy
        self.zoom = 1.0
        self.dragging = False
        self.watermark = None
        self.text_overlays = []  # Store text overlay information

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

    def add_text_overlay(self, text, position=(10, 10), font_size=30, color=(255, 255, 255, 255), 
                        font_path=None):
        """
        Add text overlay to the image.
        
        Args:
            text (str): Text to add to the image
            position (tuple): (x, y) coordinates for text placement
            font_size (int): Size of the font
            color (tuple): RGBA color value for the text
            font_path (str): Optional path to a custom font file
        """
        # Store text overlay information
        self.text_overlays.append({
            'text': text,
            'position': position,
            'font_size': font_size,
            'color': color,
            'font_path': font_path
        })
        
        # Apply the text overlay
        self._apply_overlays()

    def set_watermark(self, watermark_path, opacity=0.5):
        """
        Load and set a watermark image.
        
        Args:
            watermark_path (str): Path to the watermark image
            opacity (float): Opacity level for the watermark (0.0 to 1.0)
        """
        if not os.path.exists(watermark_path):
            raise FileNotFoundError("Watermark image not found")
            
        # Load and convert watermark to RGBA
        watermark = Image.open(watermark_path).convert('RGBA')
        
        # Create alpha layer
        alpha = watermark.split()[3]
        alpha = alpha.point(lambda x: int(x * opacity))
        watermark.putalpha(alpha)
        
        self.watermark = {
            'image': watermark,
            'opacity': opacity
        }
        
        # Apply the watermark
        self._apply_overlays()

    def apply_watermark(self, position=(0, 0)):
        """
        Apply the currently set watermark to the image.
        
        Args:
            position (tuple): (x, y) coordinates for watermark placement
        """
        if not self.watermark:
            return
            
        # Create a new image for compositing
        composite = Image.new('RGBA', self.image.size, (0, 0, 0, 0))
        
        # Convert base image to RGBA
        base = self.image.convert('RGBA')
        
        # Resize watermark if needed
        watermark = self.watermark['image']
        if watermark.size != base.size:
            watermark = watermark.resize(
                (base.size[0] // 4, base.size[1] // 4),
                Image.Resampling.LANCZOS
            )
        
        # Paste base image and watermark
        composite.paste(base, (0, 0))
        composite.paste(watermark, position, watermark)
        
        self.image = composite
        self._update_display()

    def _apply_overlays(self):
        """Apply all text overlays and watermark to the image."""
        # Start with a fresh copy of the original image
        self.image = self.original_image.copy()
        
        # Resize to current size
        self.image = self.image.resize(
            (int(self.original_image.width * self.zoom), 
             int(self.original_image.height * self.zoom)),
            Image.Resampling.LANCZOS
        )
        
        # Convert to RGBA for overlays
        self.image = self.image.convert('RGBA')
        
        # Apply text overlays
        if self.text_overlays:
            draw = ImageDraw.Draw(self.image)
            for overlay in self.text_overlays:
                try:
                    if overlay['font_path']:
                        font = ImageFont.truetype(overlay['font_path'], overlay['font_size'])
                    else:
                        font = ImageFont.load_default()
                except:
                    font = ImageFont.load_default()
                
                draw.text(
                    overlay['position'],
                    overlay['text'],
                    font=font,
                    fill=overlay['color']
                )
        
        # Apply watermark if exists
        if self.watermark:
            self.apply_watermark()
        
        self._update_display()

    def _update_display(self):
        """Update the displayed image with current modifications."""
        self.img_tk = ImageTk.PhotoImage(self.image)
        self.canvas.itemconfig(self.img_id, image=self.img_tk)

    def save_image(self, output_path):
        """
        Save the current state of the image with all overlays and watermark.
        
        Args:
            output_path (str): Path where to save the image
        """
        # Ensure we're saving in RGB mode for JPG compatibility
        if output_path.lower().endswith(('.jpg', '.jpeg')):
            self.image = self.image.convert('RGB')
        
        self.image.save(output_path)

    def reset_image(self):
        """Reset the image to its original state without any overlays or watermark."""
        self.image = self.original_image.copy()
        self.text_overlays = []
        self.watermark = None
        self._update_display()

    # Existing methods remain unchanged
    def _handle_zoom(self, factor):
        new_zoom = self.zoom * factor
        if 0.5 <= new_zoom <= 2.0:
            self.zoom = new_zoom
            self._apply_overlays()  # Reapply overlays after zoom
            self.zoom_label.config(text=f"Zoom: {int(self.zoom * 100)}%")
            self._center_image()

    def _start_drag(self, event):
        self.prev_x, self.prev_y = event.x, event.y
        self.dragging = True
        self.canvas.config(cursor="hand2")

    def _handle_drag(self, event):
        if not self.dragging: return
        
        dx, dy = event.x - self.prev_x, event.y - self.prev_y
        x, y = self.canvas.coords(self.img_id)
        img_width, img_height = int(self.image.width * self.zoom), int(self.image.height * self.zoom)
        canvas_width, canvas_height = self.canvas.winfo_width(), self.canvas.winfo_height()
        new_x, new_y = x + dx, y + dy
        min_visible = 450
        
        new_x = min(canvas_width - min_visible + img_width/2, max(min_visible - img_width/2, new_x))
        new_y = min(canvas_height - min_visible + img_height/2, max(min_visible - img_height/2, new_y))
        
        self.canvas.coords(self.img_id, new_x, new_y)
        self.prev_x, self.prev_y = event.x, event.y

    def _stop_drag(self, event):
        self.dragging = False
        self.canvas.config(cursor="arrow")

    def _center_image(self):
        self.canvas.coords(self.img_id, self.canvas.winfo_width() // 2, self.canvas.winfo_height() // 2)