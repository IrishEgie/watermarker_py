import tkinter as tk
from tkinter import Image, Label, Scale, Entry, Frame
from config.watermark_handler import WatermarkHandler
import customtkinter as ctk
class WatermarkControls:
    def __init__(self, watermark_handler: WatermarkHandler):
        self.watermark_handler = watermark_handler

    def add_watermark_controls(self):
        """Add watermark controls to the UI"""
        if self.watermark_handler.has_watermark:
            return
        
        # Reset zoom when adding watermark controls
        self.watermark_handler.zoom = 1.0
        self.watermark_handler.zoom_label.config(text="Zoom: 100%")
        self.watermark_handler.image = self.watermark_handler.base_image.copy()
        self.watermark_handler.update_display()
        
        self.watermark_handler.control_panel = Frame(self.watermark_handler, bg="white", relief="raised", borderwidth=1)
        self.watermark_handler.control_panel.place(x=20, y=20, width=180, height=340)
        
        # Modify the handle frame to have 'whitesmoke' background color
        handle = Frame(self.watermark_handler.control_panel, bg="lightgray", height=20)
        handle.pack(fill='x', side='top')

        # Add the Close Button to the top-right corner of the handle frame
        close_button = ctk.CTkButton(handle,
                                     text="X",
                                     command=self.close_control_panel,
                                     fg_color="lightgray", 
                                     hover_color="gray",
                                     width=20, height=20, 
                                     corner_radius=10,
                                     text_color="black", 
                                     border_width=0)
        close_button.pack(side='right')
        
        handle.bind("<Enter>", lambda e: handle.config(cursor="hand2"))
        handle.bind("<Leave>", lambda e: handle.config(cursor="arrow"))
        handle.bind('<Button-1>', self.watermark_handler._start_control_panel_drag)
        handle.bind('<B1-Motion>', self.watermark_handler._handle_control_panel_drag)
        handle.bind('<ButtonRelease-1>', self.watermark_handler._stop_control_panel_drag)

        controls = [
            ("Watermark Opacity", ctk.CTkSlider, {
                "from_": 0,
                "to": 100,
                "command": self.watermark_handler._update_watermark,
                "fg_color": "#f0f0f0",  # Light color for the track (inverted effect)
                "button_color": "#4CAF50",  # Darker color for the button (inverted effect)
                "width": 150, "height": 20
            }),
            ("Font Size", Entry, {"width": 20, "bg": "white", "fg": "black"}),
            ("Watermark Text", Entry, {"width": 20, "bg": "white", "fg": "black"}),
            ("Watermark Color", Entry, {"width": 20, "bg": "white", "fg": "black"})
        ]

        for i, (text, widget_class, props) in enumerate(controls):
            label = Label(self.watermark_handler.control_panel, text=text, bg="white", anchor='w', width=20)
            label.pack(pady=(10 if i == 0 else 0, 0), anchor='w')
            
            widget = widget_class(self.watermark_handler.control_panel, **props)
            
            if widget_class == ctk.CTkSlider:  # Check if it's the CTkSlider
                widget.set(100)  # Set the default value to 100 (full opacity)
                self.watermark_handler.alpha_slider = widget
                self.watermark_handler._update_watermark()  # Ensure opacity is set correctly on startup
            else:
                initial_value = {
                    "Font Size": str(self.watermark_handler.watermark_size),
                    "Watermark Text": "Watermark",
                    "Watermark Color": "#FFFFFF"
                }.get(text, "")
                widget.insert(0, initial_value)
                
                # Bind the update function for "Font Size", "Watermark Text", and "Watermark Color"
                widget.bind('<Return>', self.watermark_handler._update_watermark)
                widget.bind('<FocusOut>', self.watermark_handler._update_watermark)

            widget.pack(pady=(0, 10))
            
            # Assign the widgets to handler
            if text == "Watermark Opacity":
                self.watermark_handler.alpha_slider = widget
            elif text == "Font Size":
                self.watermark_handler.size_entry = widget
            elif text == "Watermark Text":
                self.watermark_handler.watermark_entry = widget
            elif text == "Watermark Color":
                self.watermark_handler.color_entry = widget

        # Save Button with CustomTkinter style
        save_button = ctk.CTkButton(self.watermark_handler.control_panel,
                                    text="Save Image",
                                    command=self.watermark_handler.save_watermarked_image,
                                    fg_color="#4CAF50",
                                    hover_color="#45a049",
                                    width=150,
                                    height=40,
                                    corner_radius=10,
                                    text_color="white")
        save_button.pack(pady=(0, 10), padx=10, fill='x')

        self.watermark_handler.has_watermark = True
        self.watermark_handler.watermark_layer = Image.new('RGBA', self.watermark_handler.image.size, (0, 0, 0, 0))
        self.watermark_handler._update_watermark()

    def close_control_panel(self):
        """Method to close/hide the control panel"""
        if self.watermark_handler.control_panel:
            self.watermark_handler.control_panel.place_forget()
            self.watermark_handler.has_watermark = False
