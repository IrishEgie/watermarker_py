import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton
from PyQt6.QtCore import Qt

class RoundedButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            QPushButton {
                border: 2px solid #4CAF50;  /* Green border */
                border-radius: 15px;         /* Rounded corners */
                background-color: #f0f0f0;   /* Button background color */
                padding: 10px;                /* Padding inside the button */
            }
            QPushButton:hover {
                background-color: #e7e7e7;    /* Change background on hover */
            }
            QPushButton:pressed {
                background-color: #d0d0d0;    /* Change background when pressed */
                border: 2px solid #3e8e41;    /* Darker border when pressed */
            }
        """)

class TestApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window title
        self.setWindowTitle("Test App")

        # Set window size (width, height)
        self.setFixedSize(300, 400)

        # Create a central widget and layout
        central_widget = QWidget()
        layout = QVBoxLayout()

        # Add a label
        label = QLabel("This is a test app.")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add a rounded button
        rounded_button = RoundedButton("Click Me", central_widget)

        layout.addWidget(label)
        layout.addWidget(rounded_button)
        central_widget.setLayout(layout)

        # Set central widget
        self.setCentralWidget(central_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TestApp()
    window.show()
    sys.exit(app.exec())
