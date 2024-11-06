import tkinter as tk
from tkinter import Image
from config.watermark_handler import WatermarkHandler
import customtkinter as ctk
from config.config import Config


class WatermarkControls:
    def __init__(self, watermark_handler: WatermarkHandler):
        # Initialize the WatermarkControls object with a reference to the watermark handler
        self.watermark_handler = watermark_handler

    def add_watermark_controls(self):
        # If a watermark is already added, no need to add controls again
        if self.watermark_handler.has_watermark:
            return

        # Reset zoom and prepare the base image for watermarking
        self.watermark_handler.zoom = 1.0
        self.watermark_handler.image = self.watermark_handler.base_image.copy()
        self.watermark_handler.zoom_label.config(text="Zoom: 100%")
        self.watermark_handler.update_display()

        # Create the control panel frame and place it on the screen
        self.watermark_handler.control_panel = ctk.CTkFrame(
            self.watermark_handler,
            fg_color=Config.get_dynamic_bg_color(),
            width=180,
            height=360,
            corner_radius=0
        )
        self.watermark_handler.control_panel.place(x=20, y=20)

        # Create a handle bar for the control panel with drag functionality
        handle = ctk.CTkFrame(self.watermark_handler.control_panel, fg_color="lightgray", height=20, corner_radius=0)
        handle.pack(fill='x', side='top')

        # Add a close button to the handle to close the control panel
        ctk.CTkButton(handle, text="x", command=self.close_control_panel, fg_color="lightgray", hover_color="gray",width=15, height=15, corner_radius=20, text_color=Config._update_label_colors()[1], border_width=0
        ).pack(side='right', padx=5, pady=5)

        # Bind drag events to the handle for moving the control panel around
        [handle.bind(e, f) for e, f in {
            "<Enter>": lambda e: handle.config(cursor="hand2"),
            "<Leave>": lambda e: handle.config(cursor="arrow"),
            "<Button-1>": self.watermark_handler._start_control_panel_drag,
            "<B1-Motion>": self.watermark_handler._handle_control_panel_drag,
            "<ButtonRelease-1>": self.watermark_handler._stop_control_panel_drag
        }.items()]

        # Define the list of controls and their properties
        controls = [
            ("Watermark Opacity", ctk.CTkSlider, {
                "from_": 0, "to": 100, "command": self.watermark_handler._update_watermark,
                "fg_color": "#f0f0f0", "button_color": "#4CAF50", "width": 150, "height": 20
            }),
            ("Font Size", ctk.CTkEntry, {
                "width": 150, "fg_color": Config.get_dynamic_bg_color(),
                "text_color": Config._update_label_colors()[1], "corner_radius": 8
            }),
            ("Watermark Text", ctk.CTkEntry, {
                "width": 150, "fg_color": Config.get_dynamic_bg_color(),
                "text_color": Config._update_label_colors()[1], "corner_radius": 8
            }),
            ("Watermark Color", ctk.CTkEntry, {
                "width": 150, "fg_color": Config.get_dynamic_bg_color(),
                "text_color": Config._update_label_colors()[1], "corner_radius": 8
            })
        ]

        # Set initial values for the controls
        initial_values = {
            "Font Size": str(self.watermark_handler.watermark_size),
            "Watermark Text": "Watermark",
            "Watermark Color": "#FFFFFF"
        }

        # Create the controls dynamically (sliders and text entries)
        for i, (text, widget_class, props) in enumerate(controls):
            # Create label for each control and pack it
            setattr(self, f'_{text.lower().replace(" ", "_")}_label', ctk.CTkLabel(
                self.watermark_handler.control_panel,
                text=text,
                fg_color=Config.get_dynamic_bg_color(),
                bg_color=Config.get_dynamic_bg_color(),
                anchor='w',
                width=20
            ).pack(padx=15, pady=(10 if i == 0 else 0, 0), anchor='w'))

            # Create the widget (Slider or Entry) and set its properties
            widget = widget_class(self.watermark_handler.control_panel, **props)
            # Update widget value or bind events based on the widget type
            if isinstance(widget, ctk.CTkSlider):
                widget.set(100)
            else:
                widget.insert(0, initial_values.get(text, ""))
                # Bind events like <Return> and <FocusOut> to update watermark
                for e in ('<Return>', '<FocusOut>'):
                    widget.bind(e, self.watermark_handler._update_watermark)
            # Pack the widget and apply padding
            widget.pack(pady=(0, 10))

            # Assign the widget to a property on the watermark_handler object
            widget_name = {
                'Watermark Opacity': 'alpha_slider',
                'Font Size': 'size_entry',
                'Watermark Text': 'watermark_entry',
                'Watermark Color': 'color_entry'
            }[text]
            setattr(self.watermark_handler, widget_name, widget)

        # Add a button to save the watermarked image
        ctk.CTkButton(
            self.watermark_handler.control_panel, text="Save Image", command=self.watermark_handler.save_watermarked_image,
            fg_color="#4CAF50", hover_color="#45a049", width=150, height=25, corner_radius=10, text_color="white"
        ).pack(pady=(0, 10), padx=15, fill='x')

        # Set watermark as added and initialize the watermark layer
        self.watermark_handler.has_watermark = True
        self.watermark_handler.watermark_layer = Image.new('RGBA', self.watermark_handler.image.size, (0, 0, 0, 0))
        self.watermark_handler._update_watermark()

    def close_control_panel(self):
        # Close the control panel and reset watermark-related properties
        if self.watermark_handler.control_panel:
            self.watermark_handler.control_panel.place_forget()
        setattr(self.watermark_handler, 'has_watermark', False)
