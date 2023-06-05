from PyQt6.QtWidgets import QMainWindow, QStackedWidget

from source.view.play_screen import PlayScreen
from source.view.settings_screen import SettingsScreen


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self._screens = QStackedWidget()
        for screen in [PlayScreen(), SettingsScreen()]:
            self._screens.addWidget(screen)

        self.setWindowTitle("Natural Mouse Sensitivity")

        self.setCentralWidget(self._screens)
        self.show()

    def get_related_cursor_position(self):
        ...

    def go_to_screen(self, index: int):
        self._screens.setCurrentIndex(index)

