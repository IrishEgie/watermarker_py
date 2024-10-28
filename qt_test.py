import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Steam Login Splash Screen Test")
        self.setGeometry(100, 100, 800, 600)  # Set window size (x, y, width, height)

        # Set the window to use native decorations
        self.setAttribute(Qt.WidgetAttribute.WA_NativeWindow, True)

        layout = QVBoxLayout()
        label = QLabel("Welcome to the Steam Login Screen!")
        label.setStyleSheet("font-size: 24px; font-weight: bold;")  # Optional styling
        layout.addWidget(label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
