from collections import defaultdict

class EventBus:

    def __init__(self):
        self._event_receivers = defaultdict(list)

    def on(self, event, receiver):
        self._event_receivers[event].append(receiver)
        def wrapper(*args, **kwargs):
            receiver(*args, **kwargs)
        return wrapper

    def emit(self, event, *args, **kwargs):
        for receiver in self._event_receivers[event]:
            receiver(*args, **kwargs)

    def unsubscribe(self, event, receiver):
        if receiver in self._event_receivers[event]:
            self._event_receivers[event].remove(receiver)

event_bus = EventBus()