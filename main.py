import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QFrame
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPainter, QRegion
class DraggableFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("border: 2px dashed #4CAF50; padding: 10px;")
        self.setAcceptDrops(True)
        self.setMinimumSize(250, 200)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            print(f'Dropped file: {url.toLocalFile()}')  # Handle the dropped file

class RoundedButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            QPushButton {
                border: 2px solid #4CAF50;
                border-radius: 15px;
                background-color: #f0f0f0;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #e7e7e7;
            }
            QPushButton:pressed {
                background-color: #d0d0d0;
                border: 2px solid #3e8e41;
            }
        """)

class TestApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window title and size
        self.setWindowTitle("Watermark App")
        self.setFixedSize(600, 600)  # Adjusted size

        # Create a central widget and layout
        central_widget = QWidget()
        layout = QVBoxLayout()

        # Add logo image
        self.logo_label = QLabel()
        self.logo_pixmap = QPixmap("watermark.svg").scaled(128, 128, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        rounded_pixmap = create_rounded_pixmap(self.logo_pixmap, 128)  # Create rounded pixmap with radius 128
        self.logo_label.setPixmap(rounded_pixmap)
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add a rounded button
        rounded_button = RoundedButton("Select Files", self)

        # Add a label for drag-and-drop instruction
        drag_label = QLabel("Or drag your files here.")
        drag_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create a draggable frame for dropping files
        self.draggable_frame = DraggableFrame()

        # Add widgets to the layout
        layout.addWidget(self.logo_label)
        layout.addWidget(rounded_button)
        layout.addWidget(drag_label)
        layout.addWidget(self.draggable_frame)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

def create_rounded_pixmap(pixmap, radius):
    rounded_pixmap = QPixmap(pixmap.size())
    rounded_pixmap.fill(Qt.GlobalColor.transparent)  # Fill with transparent color

    painter = QPainter(rounded_pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setBrush(Qt.GlobalColor.white)  # Fill with white or any background color
    painter.setPen(Qt.GlobalColor.transparent)  # No border
    painter.drawRoundedRect(0, 0, pixmap.width(), pixmap.height(), radius, radius)
    painter.setClipRegion(QRegion(rounded_pixmap.rect(), QRegion.RegionType.Ellipse))
    painter.drawPixmap(0, 0, pixmap)  # Draw original pixmap
    painter.end()

    return rounded_pixmap


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TestApp()
    window.show()
    sys.exit(app.exec())
