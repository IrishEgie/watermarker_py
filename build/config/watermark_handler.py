# Section 2: Watermark Management, Control Panel UI & Event Handling
from config.image_handler_ui import CustomImageGallery
from pathlib import Path
import sys
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageFont
import os
from config.config import Config

class WatermarkHandler(CustomImageGallery):
    def __init__(self, parent, img_path):
        # Initialize the parent class (CustomImageGallery) first
        super().__init__(parent, img_path)
        
        # Initialize watermark-specific attributes
        self.watermark_entry = None
        self.alpha_slider = None
        self.size_entry = None
        self.color_entry = None
        self.control_panel = None
        self.has_watermark = False
        self.watermark_layer = None
        self.base_watermark_size = 36  # Store the base size separately
        self.watermark_size = 36  # This will be the scaled size

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
        alpha = int(self.alpha_slider.get() * 2.55)
        
        # Use the base watermark size for initial drawing
        try:
            size_input = int(self.size_entry.get())
            self.base_watermark_size = max(12, min(72, size_input))
        except (ValueError, AttributeError):
            pass
        
        # Process color
        if len(color) == 7:
            r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
            color = (r, g, b, alpha)
        
        # Load font at base size
        try:
            if self.font:
                font = ImageFont.truetype(self.font, self.base_watermark_size)
            else:
                font = ImageFont.load_default()
        except Exception as e:
            print(f"Font error: {e}")
            font = ImageFont.load_default()
        
        # Calculate text position in base image coordinates
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        # Convert watermark position to base image coordinates
        base_x = self.watermark_x
        base_y = self.watermark_y
        
        x = max(0, min(base_x - text_width // 2, self.base_image.width - text_width))
        y = max(0, min(base_y - text_height // 2, self.base_image.height - text_height))
        
        # Draw watermark on base layer
        draw.text((x, y), text, font=font, fill=color)
        
        # Resize watermark layer to match current zoom level
        if self.zoom != 1.0:
            new_width = int(self.base_image.width * self.zoom)
            new_height = int(self.base_image.height * self.zoom)
            self.watermark_layer = base_layer.resize((new_width, new_height), Image.Resampling.LANCZOS)
        else:
            self.watermark_layer = base_layer
        
        # Update display to show the new watermark size
        self.update_display()

    # In watermark_handler.py
    def _validate_font_size(self, event=None):
        """Validate font size input and update watermark"""
        try:
            current = self.size_entry.get().strip()
            if current == "":
                return

            size = int(current)
            
            # Update base size within bounds
            if 12 <= size <= 72:
                self.base_watermark_size = size
            elif size < 12:
                self.base_watermark_size = 12
                self.size_entry.delete(0, tk.END)
                self.size_entry.insert(0, "12")
            elif size > 72:
                self.base_watermark_size = 72
                self.size_entry.delete(0, tk.END)
                self.size_entry.insert(0, "72")
            
            # Force watermark redraw
            self._recreate_watermark()
                
        except ValueError as e:
            print(f"Value error in font size validation: {e}")
            self.size_entry.delete(0, tk.END)
            self.size_entry.insert(0, str(self.base_watermark_size))


    def _update_watermark(self, event=None):
        """Update watermark in response to changes"""
        self._recreate_watermark()

    def save_watermarked_image(self):
        """Save the watermarked image to a user-selected location"""
        if not self.has_watermark:
            messagebox.showwarning("No Watermark", "Please add a watermark before saving.")
            return

        # Set initial directory to the Pictures library
        initial_dir = (
            os.path.join(os.environ['USERPROFILE'], 'Pictures') if sys.platform.startswith('win') 
            else os.path.expanduser('~/Pictures')
        )

        # Open file dialog
        file_path = filedialog.asksaveasfilename(
            initialdir=initial_dir,
            title="Save Watermarked Image",
            filetypes=[
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg;*.jpeg"),
                ("All files", "*.*")
            ],
            defaultextension=".png"
        )

        if file_path:
            try:
                # Update the last save path in config
                Config.last_save_path = str(Path(file_path).parent)

                # Create the final composite image
                if self.watermark_layer:
                    # Create a new composite at original size
                    base_img = self.base_image.copy()
                    watermark = self.watermark_layer.resize(
                        base_img.size, 
                        Image.Resampling.LANCZOS
                    )
                    final_image = Image.alpha_composite(
                        base_img.convert('RGBA'), 
                        watermark
                    )
                else:
                    final_image = self.base_image

                # Save the image
                final_image.save(file_path)
                messagebox.showinfo(
                    "Success", 
                    f"Image saved successfully to:\n{file_path}"
                )
            except Exception as e:
                messagebox.showerror(
                    "Error",
                    f"Failed to save image:\n{str(e)}"
                )

