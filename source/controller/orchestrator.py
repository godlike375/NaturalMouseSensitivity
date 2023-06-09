
from source.controller.event_bus import event_bus
from source.controller.thread_helpers import ThreadLoopable, MutableValue, run_after
from source.controller.mouse import MouseParamsController, INTERVAL, MousePosition
from source.model.target_positioning import TargetPositioning
from source.model.core import FlickAndTarget, Target, calculate_average_delta
from source.model.coordinates import Point
from source.view.main_window import MainWindow, CALIBRATION_SCREEN_ID, SETTINGS_SCREEN_ID, RESULT_SCREEN_ID

class Orchestrator(ThreadLoopable):
    def __init__(self, mouse_position: MousePosition, view: MainWindow):
        self._mouse = MouseParamsController(mouse_position)
        self._positioning = TargetPositioning()
        self._view = view
        self._interval = MutableValue(INTERVAL)
        self._calibration_screen = view.screen_objects[CALIBRATION_SCREEN_ID]

        self.start_calibration = event_bus.on('calibration_started', self.start_calibration)
        self.open_settings = event_bus.on('settings_opened', self.open_settings)
        self.clicked_target = event_bus.on('clicked_target', self.clicked_target)

        self._calibration_targets_count = 10
        self._calibration_results = []

        super().__init__(self._in_game_loop, self._interval, run_immediately=False)

    def _in_game_loop(self):
        ...
        #run_after(, 10, args=[])

    def start_calibration(self):
        self._calibration_results = []
        self._mouse.start_thread()
        height = self._view.height()
        width = self._view.width()
        self._calibration_screen.move_target(width // 2, height // 2)
        self._view.go_to_screen(CALIBRATION_SCREEN_ID)

    def open_settings(self):
        self._view.go_to_screen(SETTINGS_SCREEN_ID)

    def clicked_target(self, coordinates: Point, target_coordinates: Point):
        if self._mouse.last_flick is not None:
            self._mouse.last_flick.end = coordinates
            flick_target = FlickAndTarget(self._mouse.last_flick, Target(target_coordinates))
            self._mouse.last_flick = None
            self._calibration_targets_count -= 1
            self._calibration_results.append(flick_target)
            if self._calibration_targets_count == 0:
                self._view.go_to_screen(RESULT_SCREEN_ID)
                event_bus.emit('result_calculated', calculate_average_delta(self._calibration_results))
                return
        height = self._view.height()
        width = self._view.width()
        x, y = self._positioning.generate_random_position\
        (
            int(width*0.2), int(width*0.8),
            int(height*0.2), int(height*0.8)
        )
        self._calibration_screen.move_target(x, y)

    def stop(self):
        self.stop_thread()
        self._mouse.stop_thread()
