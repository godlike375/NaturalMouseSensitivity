
from source.controller.event_bus import event_bus
from source.controller.thread_helpers import ThreadLoopable, MutableValue, run_after
from source.controller.mouse import MouseParamsController, INTERVAL, MousePosition
from source.model.target_spawner import generate_random_target
from source.view.main_window import MainWindow, CALIBRATION_SCREEN_ID

class Orchestrator(ThreadLoopable):
    def __init__(self, mouse_position: MousePosition, view: MainWindow):
        self._mouse = MouseParamsController(mouse_position)
        self._view = view
        self._interval = MutableValue(INTERVAL)
        #self._mouse.start_thread()

        self.start_calibration = event_bus.on('calibration_started', self.start_calibration)
        self.open_settings = event_bus.on('settings_opened', self.open_settings)

        super().__init__(self._in_game_loop, self._interval, run_immediately=False)

    def _in_game_loop(self):
        run_after(generate_random_target, 10, args=[])

    def start_calibration(self):
        self._view.go_to_screen(CALIBRATION_SCREEN_ID)

    def open_settings(self):
        ...