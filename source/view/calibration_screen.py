from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout

from source.model.core import Target


class CalibrationScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)

    def spawn_target(self, target: Target):
        ...
