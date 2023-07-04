from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtGui import QPixmap, QPainter, QColor, QBrush, QMouseEvent

from source.controller.event_bus import event_bus
from source.view.qt_utils import qpoint_to_point


class TargetWidget(QLabel):
    def __init__(self, parent=None, color=QColor(100, 200, 0), size: int=40):
        super().__init__(parent)
        self.color = color
        self.radius = size
        self.margin = (20, 20)
        self.pixmap = QPixmap(3 * self.radius + 1, 3 * self.radius + 1)
        self.pixmap.fill(QColor("transparent"))

        painter = QPainter(self.pixmap)
        painter.setRenderHint(QPainter.renderHints(painter).Antialiasing)
        painter.setBrush(QBrush(self.color))

        center = self.radius, self.radius
        painter.drawEllipse(center[0] - self.radius + self.margin[0], center[1] - self.radius + self.margin[1], self.radius * 2, self.radius * 2)
        painter.setBrush(QBrush(QColor(0, 0, 0)))
        painter.drawEllipse(center[0] - 2  + self.margin[0], center[1] - 2  + self.margin[1], 5, 5)

        painter.end()
        self.setPixmap(self.pixmap)
        self.setGeometry(0, 0, self.pixmap.width(), self.pixmap.height())
        self.show()

    def mousePressEvent(self, event: QMouseEvent):
        event_bus.emit('clicked_target', qpoint_to_point(event.scenePosition()).to_int(),
                       qpoint_to_point(self.pos()).to_int())

class CalibrationScreen(QWidget):
    def __init__(self, master):
        super().__init__(master)
        layout = QVBoxLayout()
        self.setLayout(layout)
        self._target = TargetWidget(self)

    def move_target(self, x, y):
        self._target.move(x, y)
