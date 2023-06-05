from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QCursor

from source.controller.thread_helpers import ThreadLoopable, MutableValue
from source.model.coordinates import Point
from source.controller.event_bus import event_bus

INTERVAL = 1 / 100  # of second


class MousePosition:
    def __init__(self):
        self.screens = QApplication.screens()

    @property
    def position_on_screen(self) -> Point:
        position = QCursor.pos(self.screens[0])
        QCursor.p
        return Point(position.x(), position.y())


class FlickDetector:
    def __init__(self):
        self._in_flick = False
        self._direction = Point(0, 0)

    def detect_flick(self, direction):
        flick_started = direction != Point(0, 0) and not self._in_flick
        if flick_started:
            self._in_flick = True
            self._direction = direction
            return

        flick_stoped = self._in_flick
        new_flick_started = direction != Point(0, 0) and direction == self._direction * -1

        if flick_stoped:
            self._in_flick = False
            self._direction = direction
            event_bus.emit('flick_detected', self)

        if new_flick_started:
            self._in_flick = True
            self._direction = direction


class MouseParamsController(ThreadLoopable):

    def __init__(self, mouse_position: MousePosition=None, flick_detector: FlickDetector=None):
        self._interval = MutableValue(INTERVAL)
        self._mouse = mouse_position or MousePosition()
        self._detector = flick_detector or FlickDetector()
        self._previous_position = self._mouse.position_on_screen
        self._previous_speed = Point(0, 0)
        self._direction = Point(0, 0)

        self.mouse_position = Point(0, 0)
        self.mouse_speed = Point(0, 0)
        self.mouse_acceleration = Point(0, 0)

        super().__init__(self._update_params, self._interval, run_immediately=False)


    @event_bus.on('flick_detected')
    def flick_detected(self):
        # TODO: перебиндить на модель, которая во время игрового процесса это делает
        print('detected')

    def _update_params(self):
        self.mouse_position = self._mouse.position_on_screen
        delta_position = self.mouse_position - self._previous_position
        self._direction = Point(0 if delta_position.x == 0 else delta_position.x / abs(delta_position.x),
                                0 if delta_position.y == 0 else delta_position.y / abs(delta_position.y))
        self.mouse_speed = abs(delta_position) / INTERVAL
        self.mouse_acceleration = abs(self.mouse_speed - self._previous_speed) / INTERVAL

        self._detector.detect_flick(self._direction)

        self._previous_position = self.mouse_position
        self._previous_speed = self.mouse_speed
