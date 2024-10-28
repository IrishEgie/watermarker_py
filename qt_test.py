import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Set the window title and size
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 400, 300)

        # Create a central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Add UI Elements
        label = QLabel("Login", self)
        layout.addWidget(label)

        self.username_edit = QLineEdit(self)
        self.username_edit.setPlaceholderText("Username")
        layout.addWidget(self.username_edit)

        self.password_edit = QLineEdit(self)
        self.password_edit.setPlaceholderText("Password")
        self.password_edit.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_edit)

        login_button = QPushButton("Login", self)
        layout.addWidget(login_button)

        # Connect button to a method (for later functionality)
        login_button.clicked.connect(self.on_login)

        # Set the layout to central widget
        central_widget.setLayout(layout)

    def on_login(self):
        # Placeholder for login logic
        username = self.username_edit.text()
        password = self.password_edit.text()
        print(f"Username: {username}, Password: {password}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showFullScreen()  # Full screen for testing
    sys.exit(app.exec_())
