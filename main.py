from PyQt6.QtWidgets import QApplication
from source.view.main_window import MainWindow
from source.controller.mouse import MouseParamsController, MousePosition
from source.controller.orchestrator import Orchestrator

import sys


def main():
    app = QApplication(sys.argv)

    view = MainWindow()
    mouse_position = MousePosition(view)
    ochestrator = Orchestrator(mouse_position, view)

    app.exec()


if __name__ == '__main__':
    main()
