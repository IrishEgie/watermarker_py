import tkinter as tk
from tkinter import Image, Scale, Frame
from config.watermark_handler import WatermarkHandler
import customtkinter as ctk
from config.config import Config
class WatermarkControls:
    def __init__(self, watermark_handler: WatermarkHandler):
        self.watermark_handler = watermark_handler
    
    def add_watermark_controls(self):
        """Add watermark controls to the UI"""
        title_color, subtitle_color, footer_color = Config._update_label_colors()
        if self.watermark_handler.has_watermark:
            return
        
        # Reset zoom when adding watermark controls
        self.watermark_handler.zoom = 1.0
        self.watermark_handler.zoom_label.config(text="Zoom: 100%")
        self.watermark_handler.image = self.watermark_handler.base_image.copy()
        self.watermark_handler.update_display()
        
        self.watermark_handler.control_panel = Frame(self.watermark_handler, bg=Config.get_dynamic_bg_color(), relief="raised", borderwidth=1)
        self.watermark_handler.control_panel.place(x=20, y=20, width=180, height=360)
        
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
                                     text_color=subtitle_color, 
                                     border_width=0)
        close_button.pack(side='right')
        
        handle.bind("<Enter>", lambda e: handle.config(cursor="hand2"))
        handle.bind("<Leave>", lambda e: handle.config(cursor="arrow"))
        handle.bind('<Button-1>', self.watermark_handler._start_control_panel_drag)
        handle.bind('<B1-Motion>', self.watermark_handler._handle_control_panel_drag)
        handle.bind('<ButtonRelease-1>', self.watermark_handler._stop_control_panel_drag)

        controls = [
            ("Watermark Opacity", Scale, {"from_": 0, "to": 100, "orient": "horizontal", 
                                        "command": self.watermark_handler._update_watermark, 
                                        "length": 150, "bg": Config.get_dynamic_bg_color(), 
                                        "troughcolor": "#f0f0f0", 
                                        "highlightbackground": "white", "highlightcolor": "white"}),
            
            ("Font Size", ctk.CTkEntry, {"width": 150, 
                                        "fg_color": Config.get_dynamic_bg_color(), 
                                        "text_color": subtitle_color, 
                                        "corner_radius": 8}),
            
            ("Watermark Text", ctk.CTkEntry, {"width": 150, 
                                            "fg_color": Config.get_dynamic_bg_color(), 
                                            "text_color": subtitle_color, 
                                            "corner_radius": 8}),
            
            ("Watermark Color", ctk.CTkEntry, {"width": 150, 
                                            "fg_color": Config.get_dynamic_bg_color(), 
                                            "text_color": subtitle_color, 
                                            "corner_radius": 8})
        ]

        for i, (text, widget_class, props) in enumerate(controls):
            # Replace tkinter Label with customtkinter CTkLabel
            label = ctk.CTkLabel(self.watermark_handler.control_panel, text=text, fg_color=Config.get_dynamic_bg_color(), bg_color=Config.get_dynamic_bg_color(), anchor='w', width=20)
            label.pack(pady=(10 if i == 0 else 0, 0), anchor='w')
            
            widget = widget_class(self.watermark_handler.control_panel, **props)
            
            if widget_class == Scale:
                widget.set(100)
            else:
                initial_value = {
                    "Font Size": str(self.watermark_handler.watermark_size),
                    "Watermark Text": "Watermark",
                    "Watermark Color": "#FFFFFF"
                }.get(text, "")
                widget.insert(0, initial_value)
                
                # In watermark_controls.py
                if text == "Font Size":
                    widget.bind('<Return>', self.watermark_handler._update_watermark)
                    widget.bind('<FocusOut>', self.watermark_handler._update_watermark)
                else:
                    widget.bind('<Return>', self.watermark_handler._update_watermark)
                    widget.bind('<FocusOut>', self.watermark_handler._update_watermark)
            
            widget.pack(pady=(0, 10))
            
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
