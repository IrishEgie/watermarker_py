from tkinter import Tk, filedialog

def test_file_dialog():
    root = Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(
        filetypes=[
            ("Image Files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp;*.tiff"),
            ("All Files", "*.*")
        ]
    )
    if file_path:
        print(f"File selected: {file_path}")
    else:
        print("No file selected.")

test_file_dialog()
