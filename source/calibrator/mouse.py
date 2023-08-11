from time import time
from typing import Optional
from itertools import cycle

from source.calibrator.game import CalibrationGame
from source.controller.event_bus import event_bus
from source.aliases import Vector
from source.model.core import Flick


class FlickDetector:
    def __init__(self, min_flick_angle: float=0.5):
        self.timestamp = time()
        self._current_flick: Optional[Flick] = None
        self._flick_direction = Vector()
        self.min_flick_angle = min_flick_angle



    def detect_flick(self, speed: float, camera_direction: Vector):
        if speed == 0:
            if self._current_flick:
                self._current_flick.end = camera_direction
                passed_sec = time() - self.timestamp
                self._current_flick.duration = passed_sec
                if passed_sec > 0.05:
                    if self._current_flick.angle_between_start_end() > self.min_flick_angle:
                        event_bus.emit('flick_detected', self._current_flick)
                        self._current_flick = None
        else:
            if self._current_flick is None:
                self._current_flick = Flick(start=camera_direction, end=camera_direction)
                self.timestamp = time()


class MouseParamsController:

    def __init__(self, game: CalibrationGame, flick_detector: FlickDetector = None):
        self._game = game
        self._detector = flick_detector or FlickDetector()
        self._previous_direction = self._game.get_camera_position_and_direction()[1]
        self._previous_speed: float = 0.0  # degree / sec
        self._flick_direction = Vector()

        self.camera_direction = Vector()
        self.mouse_speed: float = 0.0  # degree / sec
        self.mouse_acceleration: float = 0.0  # degree / sec
        self.last_flick = None

        self.flick_detected = event_bus.on('flick_detected', self.flick_detected)
        self.slower_times = 4
        self.update_params_multiplier = cycle(range(self.slower_times))

    def ready(self):
        return next(self.update_params_multiplier) == 0


    def flick_detected(self, flick: Flick):
        self.last_flick = flick
        #print(f'flick {flick}')

    def update_params(self):
        self.camera_direction = self._game.get_camera_position_and_direction()[1]
        delta_angle = self.camera_direction.angle_deg(self._previous_direction)
        frame_time = self._game.frametime.current_frame_time / self.slower_times
        self.mouse_speed = abs(delta_angle) / frame_time
        self.mouse_acceleration = abs(self.mouse_speed - self._previous_speed) / frame_time

        #print(delta_angle)
        self._detector.detect_flick(self.mouse_speed, self.camera_direction)

        self._previous_direction = self.camera_direction
        self._previous_speed = self.mouse_speed


class MouseParamsControllerV2:

    def __init__(self, game: CalibrationGame, flick_detector: FlickDetector = None):
        cam_direction = game.get_camera_position_and_direction()[1]
        self.last_flick = Flick(start=cam_direction)

    def ready(self):
        return True


    def flick_detected(self, flick: Flick):
        self.last_flick = flick
        #print(f'flick {flick}')

    def update_params(self):
        ...

    def set_start_point(self, point: Vector):
        self.last_flick = Flick(start=point)

    def set_end_point(self, point: Vector):
        self.last_flick.end = point
