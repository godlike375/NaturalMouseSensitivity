
from source.controller.event_bus import event_bus
from source.controller.thread_helpers import ThreadLoopable, MutableValue, run_after
from source.controller.mouse import MouseParamsController, INTERVAL
from source.model.target_spawner import generate_random_target

class Orchestrator(ThreadLoopable):
    def __init__(self):
        self._mouse = MouseParamsController()
        self._interval = MutableValue(INTERVAL)
        #self._mouse.start_thread()
        super().__init__(self._in_game_loop, self._interval, run_immediately=False)

    def _in_game_loop(self):
        run_after(generate_random_target, 10, args=[])