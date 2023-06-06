from PyQt6.QtWidgets import QMainWindow, QStackedWidget

from source.view.calibration_screen import CalibrationScreen
from source.view.settings_screen import SettingsScreen
from source.view.result_screen import ResultScreen
from source.view.start_screen import StartScreen

CALIBRATION_SCREEN_ID = 1

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self._screens = QStackedWidget()
        for screen in [StartScreen(), CalibrationScreen(), ResultScreen(), SettingsScreen()]:
            self._screens.addWidget(screen)

        self.setWindowTitle("Natural Mouse Sensitivity")

        self.setCentralWidget(self._screens)
        self.show()

    def go_to_screen(self, index: int):
        self._screens.setCurrentIndex(index)

