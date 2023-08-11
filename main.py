from PyQt6.QtWidgets import QApplication
from source.launcher.launcher import Launcher

import sys


def main():
    app = QApplication(sys.argv)

    view = Launcher()

    app.exec()


if __name__ == '__main__':
    main()
