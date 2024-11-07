import os
from PIL import Image, ImageDraw, ImageFont

def text(input_image_path, output_path, text_color=(255, 0, 0), opacity=255):
    # Open the original image
    image = Image.open(input_image_path).convert("RGBA")
    
    # Create an empty "overlay" with the same size as the original image (transparent)
    text_layer = Image.new("RGBA", image.size, (0, 0, 0, 0))  # Transparent layer

    draw = ImageDraw.Draw(text_layer)
    y = 10

    # Path to a default font (replace with the correct path if necessary)
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    if not os.path.isfile(font_path):
        print(f"Font {font_path} not found. Using default font.")
        font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"  # Another fallback font

    for font_size in range(12, 75, 10):
        try:
            font = ImageFont.truetype(font_path, size=font_size)
        except OSError:
            print(f"Error: Unable to load font at size {font_size}.")
            continue

        # Adjust the color and opacity
        color_with_opacity = (*text_color, opacity)  # RGBA

        # Draw the text onto the text layer (which is transparent)
        draw.text((10, y), f"Chihuly Exhibit (font_size={font_size})", font=font, fill=color_with_opacity)
        y += 35

    # Composite the text_layer onto the original image
    final_image = Image.alpha_composite(image, text_layer)

    # Save the resulting image
    final_image.save(output_path, format="PNG")  # Use PNG to support transparency

if __name__ == "__main__":
    # Example usage with text color and opacity
    text("img/test.jpg", "output_with_opacity.png", text_color=(0, 255, 0), opacity=30)
