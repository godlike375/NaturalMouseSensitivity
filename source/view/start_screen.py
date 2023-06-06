from functools import partial

from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout

from source.controller.event_bus import event_bus
from source.view.qt_utils import call_slot_interface_wrapper

class StartScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.start_button = QPushButton('Start calibration')
        self.settings_button = QPushButton('Settings')

        open_settings = partial(call_slot_interface_wrapper, event_bus.emit, 'settings_opened')
        start_calibration = partial(call_slot_interface_wrapper, event_bus.emit, 'calibration_started')

        self.start_button.clicked.connect(start_calibration)
        self.settings_button.clicked.connect(open_settings)

        layout = QVBoxLayout()
        layout.addWidget(self.start_button)
        self.setLayout(layout)


