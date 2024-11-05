# Section 2: Watermark Management, Control Panel UI & Event Handling
from config.image_handler_ui import CustomImageGallery
from pathlib import Path
import sys
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageFont
from tkinter import Label, Scale, Entry, Frame
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

    def _recreate_watermark(self):
        """Recreate watermark with current settings"""
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

    def add_watermark_controls(self):
        """Modified version of add_watermark_controls to include save button"""
        if self.has_watermark:
            return
                    
        # Reset zoom when adding watermark controls
        self.zoom = 1.0
        self.zoom_label.config(text="Zoom: 100%")
        self.image = self.base_image.copy()
        self.update_display()
                    
        self.control_panel = Frame(self, bg="white", relief="raised", borderwidth=1)
        self.control_panel.place(x=20, y=20, width=180, height=340)  # Increased height for save button
        
        # Add controls for watermark options
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
                    # Bind the validation method here
                    widget.bind('<Return>', self._validate_font_size)
                    widget.bind('<FocusOut>', self._validate_font_size)
                else:
                    widget.bind('<Return>', self._update_watermark)
                    widget.bind('<FocusOut>', self._update_watermark)
            
            widget.pack(pady=(0, 10))
            
            # Save references to widgets for later use
            if text == "Watermark Opacity":
                self.alpha_slider = widget
            elif text == "Font Size":
                self.size_entry = widget
            elif text == "Watermark Text":
                self.watermark_entry = widget
            elif text == "Watermark Color":
                self.color_entry = widget
        
        # Add Save button at the bottom of control panel
        save_button = tk.Button(
            self.control_panel,
            text="Save Image",
            command=self.save_watermarked_image,
            bg="#4CAF50",
            fg="white",
            relief="raised",
            pady=5
        )
        save_button.pack(pady=(0, 10), padx=10, fill='x')
        
        self.has_watermark = True
        self.watermark_layer = Image.new('RGBA', self.image.size, (0, 0, 0, 0))
        self._update_watermark()
