from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout


class SettingsScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)
