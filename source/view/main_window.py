from PyQt6.QtWidgets import QMainWindow, QStackedWidget
from PyQt6.QtGui import QCursor, QMouseEvent
from PyQt6 import QtCore

from source.view.calibration_screen import CalibrationScreen
from source.view.settings_screen import SettingsScreen
from source.view.result_screen import ResultScreen
from source.view.start_screen import StartScreen

START_SCREEN_ID = 0
CALIBRATION_SCREEN_ID = 1
RESULT_SCREEN_ID = 2
SETTINGS_SCREEN_ID = 3

class MainWindow(QMainWindow):


    def __init__(self, width=1200, height=200):
        super().__init__()

        #self.showFullScreen()
        self.setCursor(QtCore.Qt.CursorShape.SizeAllCursor)
        #If mouse tracking is disabled (the default), the widget only receives mouse move events when at
        # least one mouse button is pressed while the mouse is being moved.
        #If mouse tracking is enabled, the widget receives mouse move events even if no buttons are pressed.
        self.setMouseTracking(True)

        self._screens = QStackedWidget()
        self.screen_objects = [StartScreen(), CalibrationScreen(self), ResultScreen(), SettingsScreen()]
        for screen in self.screen_objects:
            self._screens.addWidget(screen)

        self.setWindowTitle("Natural Mouse Sensitivity")

        self.setCentralWidget(self._screens)
        self.setMinimumSize(width, height+50)
        self.show()

    def go_to_screen(self, index: int):
        self._screens.setCurrentIndex(index)
