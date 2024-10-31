import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, QLabel
from PyQt5.QtGui import QIcon


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle('Watermarker')
        self.setFixedSize(500, 500)  # Set a fixed size for the window
        self.center()  # Center the window on startup

    def center(self):
        # Get the screen's geometry
        screen = QDesktopWidget().screenGeometry()
        # Get the window's geometry
        size = self.geometry()
        # Calculate the x and y positions to center the window
        x = (screen.width() - size.width()) // 2
        y = (screen.height() - size.height()) // 2
        # Set the new position
        self.move(x, y)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
