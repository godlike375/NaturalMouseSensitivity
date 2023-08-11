from time import time as clock

from ursina import Entity

class Frametime(Entity):
    def __init__(self):
        super().__init__()
        self.timestamp = clock()
        self.current_frame_time = 0.0

    def update(self):
        self.current_frame_time = clock() - self.timestamp
        self.timestamp = clock()