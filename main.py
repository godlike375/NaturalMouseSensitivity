from PyQt6.QtWidgets import QApplication
from source.view.main_window import MainWindow
from source.controller.mouse import MouseParamsController
from source.controller.orchestrator import Orchestrator

import sys


def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    mouse_position = window.get_related_cursor_position
    ochestrator = Orchestrator()

    app.exec()


if __name__ == '__main__':
    main()
