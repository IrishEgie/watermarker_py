import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt  # Import Qt here


class TestApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window title
        self.setWindowTitle("Test App")

        # Set window size (width, height)
        self.setFixedSize(300, 400)  # Adjust to desired size

        # Create a central widget and layout
        central_widget = QWidget()
        layout = QVBoxLayout()

        # Add a label for demonstration
        label = QLabel("This is a test app.")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(label)
        central_widget.setLayout(layout)
        
        # Set central widget
        self.setCentralWidget(central_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TestApp()
    window.show()
    sys.exit(app.exec())
