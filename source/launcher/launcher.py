from time import sleep
import subprocess

import sys
from pathlib import Path

from PyQt6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget

START_SCREEN_ID = 0
CALIBRATION_SCREEN_ID = 1
RESULT_SCREEN_ID = 2
SETTINGS_SCREEN_ID = 3

CREATE_NEW_PROCESS_GROUP = 0x00000200
DETACHED_PROCESS = 0x00000008


class Launcher(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Natural Mouse Sensitivity")
        self.start_button = QPushButton('Start calibration')
        self.settings_button = QPushButton('Settings')

        # start_calibration = partial(call_slot_interface_wrapper, event_bus.emit, 'calibration_started')

        self.start_button.clicked.connect(self.start_calibration)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.start_button)
        self.layout.addWidget(self.settings_button)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

        self.show()

    def start_calibration(self):
        program = str(Path.cwd() / sys.argv[0])

        interpreter = sys.executable
        subprocess.Popen([interpreter, str(Path(program).parent / 'source' / 'calibrator' / 'runner.py')],
                         creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP)
        sleep(1)
        sys.exit()
