# Image Watermark Tool

A simple, user-friendly GUI application for adding text watermarks to images. Built with Python and CustomTkinter, this tool allows users to easily add and customize watermarks on their images with features like opacity control, font size adjustment, and color selection.

## Features

- **Drag & Drop Support**: Easily drag and drop images into the application
- **Image Manipulation**:
  - Zoom in/out functionality
  - Pan/drag image viewing
  - Center-aligned image display
- **Watermark Customization**:
  - Adjustable opacity (0-100%)
  - Custom font size (12-200px)
  - Custom text input
  - Color selection (hex color codes)
  - Draggable watermark positioning
- **Modern UI**:
  - Dark/Light mode support
  - Draggable control panel
  - Clean and intuitive interface
- **File Operations**:
  - Support for common image formats (PNG, JPG, JPEG, GIF, BMP, TIFF)
  - Save watermarked images in PNG or JPEG format

## Installation

1. Clone the repository:
```bash
git clone https://github.com/IrishEgie/watermarker_py.git
cd watermark-tool
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

Required packages:
- customtkinter
- tkinterdnd2
- Pillow (PIL)

## Usage

1. Run the application:
```bash
python gui.py
```

2. Add an image:
   - Click "Select File" to choose an image
   - Or drag and drop an image file into the application window

3. Add a watermark:
   - Click "Add Watermark" in the top menu
   - Use the control panel to customize your watermark:
     - Type your watermark text
     - Adjust the opacity slider
     - Enter a font size (12-200)
     - Enter a hex color code (e.g., #FFFFFF for white)
   - Drag the watermark to position it on the image

4. Save your image:
   - Click "Save" in the top menu
   - Choose your save location and format (PNG or JPEG)

## File Structure

```
watermark-tool/
├── gui.py              # Main application window
├── gui1.py            # Second screen with watermark controls
├── config/
│   ├── config.py      # Application configuration
│   ├── watermark_handler.py    # Watermark processing logic
│   ├── watermark_controls.py   # Watermark UI controls
│   └── image_handler_ui.py     # Image display and manipulation
└── build/
    └── assets/        # Application assets
```

## System Requirements

- Python 3.6 or higher
- Operating System: Windows, macOS, or Linux
- System font availability for watermark text (falls back to default if none available)

## Known Limitations

- Zoom functionality is disabled while the watermark control panel is open
- Font selection is limited to system defaults
- Maximum font size is capped at 200px

## Contributing

Feel free to fork the repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT License](LICENSE)