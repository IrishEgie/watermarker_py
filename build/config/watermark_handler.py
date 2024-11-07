# Section 2: Watermark Management, Control Panel UI & Event Handling
from config.image_handler_ui import CustomImageGallery
from pathlib import Path
import sys
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageFont, ImageTk
import os
from config.config import Config

class WatermarkHandler(CustomImageGallery):
    def __init__(self, parent, img_path):
        super().__init__(parent, img_path)
        
        # Initialize watermark-specific attributes
        self.watermark_entry = None
        self.alpha_slider = None
        self.size_entry = None
        self.color_entry = None
        self.control_panel = None
        self.has_watermark = False
        self.watermark_layer = None
        self.base_watermark_size = 36
        self.watermark_size = 36
        self.font = self._get_default_font()

    def _recreate_watermark(self):
        """Recreate watermark with current settings"""
        if not self.has_watermark:
            return
            
        # Create fresh watermark layer at the base image size
        base_layer = Image.new('RGBA', self.base_image.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(base_layer)
        
        # Get current parameters
        text = self.watermark_entry.get()
        color = self.color_entry.get()
        alpha = int(self.alpha_slider.get() * 2.55)  # Convert from 0-100 to 0-255
        
        try:
            # Get and validate font size
            size_text = self.size_entry.get().strip()
            if size_text:  # Only update if there's a value
                font_size = int(size_text)
                self.watermark_size = max(12, min(font_size, 200))  # Clamp between 12 and 200
        except (ValueError, TypeError):
            # Keep current size if invalid input
            pass
        
        # Process color with fallback
        try:
            if len(color) == 7 and color.startswith('#'):
                r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
                color = (r, g, b, alpha)
            else:
                color = (255, 255, 255, alpha)
        except ValueError:
            color = (255, 255, 255, alpha)
        
        # Load font with current size
        try:
            if self.font:
                font = ImageFont.truetype(self.font, self.watermark_size)
            else:
                font = ImageFont.load_default()
                # Scale default font if possible
                if hasattr(font, 'size'):
                    font = font.font_variant(size=self.watermark_size)
        except Exception as e:
            print(f"Font error: {e}")
            font = ImageFont.load_default()
        
        # Calculate text position with new font size
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        # Center the text at watermark position
        x = max(0, min(self.watermark_x - text_width // 2, self.base_image.width - text_width))
        y = max(0, min(self.watermark_y - text_height // 2, self.base_image.height - text_height))
        
        # Draw watermark
        draw.text((x, y), text, font=font, fill=color)
        
        # Store the base watermark layer
        self.watermark_layer = base_layer
        
        # Update display
        self.update_display()

    def _update_watermark(self, event=None):
        """Update watermark in response to changes"""
        # If size entry exists and has focus, wait for Enter key
        if event and event.widget == self.size_entry:
            if event.type == '2':  # KeyPress event
                if event.keysym != 'Return':
                    return
        self._recreate_watermark()

    def _handle_size_change(self, event=None):
        """Specific handler for font size changes"""
        try:
            new_size = int(self.size_entry.get())
            if 12 <= new_size <= 200:
                self.watermark_size = new_size
                self._recreate_watermark()
        except ValueError:
            # Restore previous valid size
            self.size_entry.delete(0, tk.END)
            self.size_entry.insert(0, str(self.watermark_size))

            
    def save_watermarked_image(self):
        """Save the watermarked image to a user-selected location"""
        if not self.has_watermark:
            messagebox.showwarning("No Watermark", "Please add a watermark before saving.")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg;*.jpeg")]
        )
        
        if file_path:
            try:
                # Create final composite at original size
                base_img = self.base_image.copy()
                if self.watermark_layer:
                    watermark = self.watermark_layer.resize(
                        base_img.size, 
                        Image.Resampling.LANCZOS
                    )
                    final_image = Image.alpha_composite(
                        base_img.convert('RGBA'), 
                        watermark
                    )
                else:
                    final_image = base_img
                    
                final_image.save(file_path)
                messagebox.showinfo("Success", "Image saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {str(e)}")    
    
    def update_display(self):
        """Update the display with current image and watermark"""
        if self.watermark_layer:
            # Ensure watermark layer matches current image size
            if self.watermark_layer.size != self.image.size:
                self.watermark_layer = self.watermark_layer.resize(
                    self.image.size, 
                    Image.Resampling.LANCZOS
                )
            # Composite the watermark onto the image
            composite = Image.alpha_composite(self.image.convert('RGBA'), self.watermark_layer)
        else:
            composite = self.image
            
        self.img_tk = ImageTk.PhotoImage(composite)
        
        if not hasattr(self, 'img_id'):
            # Initialize image at the center of the canvas
            self.img_id = self.canvas.create_image(
                self.canvas_center_x,
                self.canvas_center_y,
                image=self.img_tk,
                anchor='center'
            )
        else:
            self.canvas.itemconfig(self.img_id, image=self.img_tk)