from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout

from source.model.core import Target


class PlayScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.button = QPushButton('Play')
        self.button.clicked.connect(self.go_to_screen1)
        layout = QVBoxLayout()
        layout.addWidget(self.button)
        self.setLayout(layout)

    def spawn_target(self, target: Target):
        ...
