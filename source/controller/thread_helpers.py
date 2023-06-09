from sys import exit
from threading import (
    Thread, Event, current_thread, Timer
)
from time import sleep
from dataclasses import dataclass


def run_after(interval, func, args=None, kwargs=None):
    args = args or []
    kwargs = kwargs or {}
    Timer(interval, func, args=args, kwargs=kwargs).start()


# https://stackoverflow.com/questions/323972/is-there-any-way-to-kill-a-thread
class StoppableThread(Thread):
    # Thread class with a stop() method

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._stop_event = Event()

    def stop(self):
        self._stop_event.set()

    @property
    def is_stopped(self):
        return self._stop_event.is_set()


# https://gist.github.com/awesomebytes/0483e65e0884f05fb95e314c4f2b3db8
def threaded(fn):
    # To use as decorator to make a function call threaded
    def wrapper(*args, **kwargs):
        thread = StoppableThread(target=fn, args=args, kwargs=kwargs)
        return thread

    return wrapper


@dataclass
class MutableValue:
    __slots__ = ['value']
    value: object


@threaded
def thread_loop_runner(func, interval: MutableValue = None):
    if interval is None:
        interval = MutableValue(0.05)
    while True:
        sleep(interval.value)
        if current_thread().is_stopped:
            exit()
        func()


class ThreadLoopable:
    def __init__(self, loop_func, interval: MutableValue, run_immediately: bool = True):
        self._loop_func = loop_func
        self._interval = interval
        self._thread_loop = StoppableThread()
        if run_immediately:
            self.start_thread(loop_func, interval)

    def start_thread(self, loop_func=None, interval=None):
        loop_func = loop_func or self._loop_func
        interval = interval or self._interval
        self._thread_loop = thread_loop_runner(loop_func, interval)
        self._thread_loop.start()

    def stop_thread(self):
        self._thread_loop.stop()

    def __enter__(self):
        self.start_thread(self._loop_func, self._interval)
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.stop_thread()
        if exc_value:
            raise exc_value
