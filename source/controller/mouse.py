from time import time

from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import QApplication

from source.controller.event_bus import event_bus
from source.controller.thread_helpers import ThreadLoopable, MutableValue
from source.model.coordinates import Point
from source.model.core import Flick

INTERVAL = 1 / 135  # of second


class MousePosition:
    def __init__(self, position_provider):
        self.screens = QApplication.screens()
        self._position_provider = position_provider

    @property
    def position_on_screen(self) -> Point:
        position = QCursor.pos(self.screens[0])
        mapped = self._position_provider.mapFromGlobal(position)
        return Point(mapped.x(), mapped.y())

    def move_cursor_to_center(self):
        center_window_pos = self._position_provider.mapToGlobal(self._position_provider.rect().center())
        QCursor.setPos(center_window_pos)


class FlickDetector:
    def __init__(self, min_flick_distance: float=5.0):
        self.duration = time()
        self._in_flick = False
        self._direction = Point(0, 0)
        self.starting_point = None
        self.ending_point = None
        self.min_flick_distance = min_flick_distance

    def detect_flick(self, direction: Point, mouse_position: Point):
        undirected = direction == Point(0, 0)
        directed = not undirected
        opposite_direction = direction == self._direction * -1
        new_flick_started = directed and opposite_direction

        if self._in_flick:
            if undirected or new_flick_started:
                self.ending_point = mouse_position
                passed_sec = time() - self.duration
                if passed_sec< 1.25:
                    self.duration = passed_sec
                    flick = Flick(self.starting_point, self.ending_point, self.duration)
                    if flick.calc_length() > self.min_flick_distance:
                        event_bus.emit('flick_detected', flick)
                        self._in_flick = False
                        self._direction = direction
                if new_flick_started:
                    self._start_flick(direction, mouse_position)
        elif directed:
            self._start_flick(direction, mouse_position)

    def _start_flick(self, direction, mouse_position):
        self._in_flick = True
        self._direction = direction
        self.starting_point = mouse_position
        self.ending_point = mouse_position
        self.duration = time()


class MouseParamsController(ThreadLoopable):

    def __init__(self, mouse_position: MousePosition, flick_detector: FlickDetector = None):
        self._interval = MutableValue(INTERVAL)
        self._mouse = mouse_position
        self._detector = flick_detector or FlickDetector()
        self._previous_position = self._mouse.position_on_screen
        self._previous_speed = Point(0, 0)
        self._direction = Point(0, 0)

        self.mouse_position = Point(0, 0)
        self.mouse_speed = Point(0, 0)
        self.mouse_acceleration = Point(0, 0)
        self.last_flick = None

        self.flick_detected = event_bus.on('flick_detected', self.flick_detected)

        super().__init__(self._update_params, self._interval, run_immediately=False)

    def flick_detected(self, flick: Flick):
        self.last_flick = flick

    def _update_params(self):
        self.mouse_position = self._mouse.position_on_screen
        delta_position = self.mouse_position - self._previous_position
        self._direction = Point(0 if delta_position.x == 0 else delta_position.x / abs(delta_position.x),
                                0 if delta_position.y == 0 else delta_position.y / abs(delta_position.y))
        self.mouse_speed = abs(delta_position) / INTERVAL
        self.mouse_acceleration = abs(self.mouse_speed - self._previous_speed) / INTERVAL

        self._detector.detect_flick(self._direction, self.mouse_position)

        self._previous_position = self.mouse_position
        self._previous_speed = self.mouse_speed
        print(self.mouse_acceleration)
        #self._mouse.move_cursor_to_center()
