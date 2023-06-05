from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout


class SettingsScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.button = QPushButton('Go to screen 2')
        self.button.clicked.connect(self.go_to_screen2)
        layout = QVBoxLayout()
        layout.addWidget(self.button)
        self.setLayout(layout)

    def go_to_screen2(self):
        print(1)
        #stacked_widget.setCurrentIndex(1)
