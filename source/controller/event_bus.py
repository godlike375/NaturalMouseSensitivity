class EventBus:

    def __init__(self):
        self._event_receiver = {}

    def on(self, event):
        def parameterized(receiver):
            self._event_receiver[event] = receiver
            def wrapper(*args, **kwargs):
                receiver(*args, **kwargs)
            return wrapper
        return parameterized

    def emit(self, event, *args, **kwargs):
        self._event_receiver[event](*args, **kwargs)

event_bus = EventBus()