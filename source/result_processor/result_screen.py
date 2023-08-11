from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout

from source.model.core import Target
from source.controller.event_bus import event_bus

class ResultScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.show_result = event_bus.on('result_calculated', self.show_result)

    def show_result(self, result):
        print(result)
