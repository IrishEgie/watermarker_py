import tkinter as tk
from PIL import Image, ImageTk

class ImageGallery(tk.Tk):
    def __init__(self, image_path):
        super().__init__()
        self.image_path = image_path
        self.image = Image.open(self.image_path)
        self.zoom_factor = 1.0

        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.img_tk = ImageTk.PhotoImage(self.image)
        self.image_id = self.canvas.create_image(0, 0, image=self.img_tk, anchor='nw')

        # Label to display zoom level
        self.zoom_label = tk.Label(self, text=f"Zoom: {int(self.zoom_factor * 100)}%", bg="white")
        self.zoom_label.place(x=30, y=self.winfo_height() - 30, anchor='sw')

        # Bind mouse wheel events for zooming
        self.bind("<MouseWheel>", self.zoom)  # Windows
        self.bind("<Button-4>", self.zoom_in)  # Linux zoom in
        self.bind("<Button-5>", self.zoom_out)  # Linux zoom out

        self.canvas.bind("<ButtonPress-1>", self.start_drag)
        self.canvas.bind("<B1-Motion>", self.do_drag)

        self.prev_x = 0
        self.prev_y = 0
        
        # Constraints
        self.left_limit = 150
        self.right_limit = 150
        self.top_limit = 150
        self.bottom_limit = 150

        # Update zoom label position on resize
        self.bind("<Configure>", self.update_label_position)

    def zoom(self, event):
        if event.delta > 0 or event.num == 4:  # Zoom in
            new_zoom_factor = self.zoom_factor * 1.1
            if new_zoom_factor <= 2.0:  # Allow zoom only up to 200%
                self.zoom_factor = new_zoom_factor
        elif event.delta < 0 or event.num == 5:  # Zoom out
            new_zoom_factor = self.zoom_factor / 1.1
            if new_zoom_factor >= 0.5:  # Allow zoom only down to 10%
                self.zoom_factor = new_zoom_factor

        # Update the image size and label
        self.update_image()

    def zoom_in(self, event):
        self.zoom(event)

    def zoom_out(self, event):
        self.zoom(event)

    def update_image(self):
        new_size = (int(self.image.width * self.zoom_factor), int(self.image.height * self.zoom_factor))
        resized_image = self.image.resize(new_size, Image.LANCZOS)
        self.img_tk = ImageTk.PhotoImage(resized_image)
        self.canvas.itemconfig(self.image_id, image=self.img_tk)

        # Update the zoom label
        self.zoom_label.config(text=f"Zoom: {int(self.zoom_factor * 100)}%")

        # Reposition to keep it centered after zooming
        self.center_image()

    def start_drag(self, event):
        self.prev_x = event.x
        self.prev_y = event.y

    def do_drag(self, event):
        dx = event.x - self.prev_x
        dy = event.y - self.prev_y
        self.canvas.move(self.image_id, dx, dy)

        # Get the current image position
        x, y = self.canvas.coords(self.image_id)
        
        # Get image dimensions
        img_width, img_height = int(self.image.width * self.zoom_factor), int(self.image.height * self.zoom_factor)

        # Constrain the image position
        if x > self.left_limit:
            self.canvas.move(self.image_id, self.left_limit - x, 0)
        elif x + img_width < self.canvas.winfo_width() - self.right_limit:
            self.canvas.move(self.image_id, (self.canvas.winfo_width() - self.right_limit - (x + img_width)), 0)

        if y > self.top_limit:
            self.canvas.move(self.image_id, 0, self.top_limit - y)
        elif y + img_height < self.canvas.winfo_height() - self.bottom_limit:
            self.canvas.move(self.image_id, 0, (self.canvas.winfo_height() - self.bottom_limit - (y + img_height)))

        self.prev_x = event.x
        self.prev_y = event.y

    def center_image(self):
        x, y = self.canvas.coords(self.image_id)
        img_width, img_height = int(self.image.width * self.zoom_factor), int(self.image.height * self.zoom_factor)

        # Center the image on the canvas
        new_x = (self.canvas.winfo_width() - img_width) // 2
        new_y = (self.canvas.winfo_height() - img_height) // 2
        self.canvas.coords(self.image_id, new_x, new_y)

    def update_label_position(self, event):
        # Update the position of the zoom label when the window is resized
        self.zoom_label.place(x=30, y=self.winfo_height() - 30, anchor='sw')

if __name__ == "__main__":
    app = ImageGallery("build/assets/frame0/image_1.png")
    app.geometry("800x600")
    app.mainloop()
