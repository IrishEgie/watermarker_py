# watermark_controls.py
import tkinter as tk
from tkinter import Image, Label, Scale, Entry, Frame
from config.watermark_handler import WatermarkHandler

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
        
        handle = Frame(self.watermark_handler.control_panel, bg="lightgray", height=20)
        handle.pack(fill='x', side='top')
        handle.bind('<Button-1>', self.watermark_handler._start_control_panel_drag)
        handle.bind('<B1-Motion>', self.watermark_handler._handle_control_panel_drag)
        handle.bind('<ButtonRelease-1>', self.watermark_handler._stop_control_panel_drag)

        controls = [
            ("Watermark Opacity", Scale, {"from_": 0, "to": 100, "orient": "horizontal", "command": self.watermark_handler._update_watermark, "length": 150}),
            ("Font Size", Entry, {"width": 20}),
            ("Watermark Text", Entry, {"width": 20}),
            ("Watermark Color", Entry, {"width": 20})
        ]
        
        for i, (text, widget_class, props) in enumerate(controls):
            label = Label(self.watermark_handler.control_panel, text=text, bg="white", anchor='w', width=20)
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
                
                if text == "Font Size":
                    widget.bind('<Return>', self.watermark_handler._validate_font_size)
                    widget.bind('<FocusOut>', self.watermark_handler._validate_font_size)
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

        save_button = tk.Button(
            self.watermark_handler.control_panel,
            text="Save Image",
            command=self.watermark_handler.save_watermarked_image,
            bg="#4CAF50",
            fg="white",
            relief="raised",
            pady=5
        )
        save_button.pack(pady=(0, 10), padx=10, fill='x')
        
        self.watermark_handler.has_watermark = True
        self.watermark_handler.watermark_layer = Image.new('RGBA', self.watermark_handler.image.size, (0, 0, 0, 0))
        self.watermark_handler._update_watermark()
