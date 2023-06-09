from random import randint

class TargetPositioning:
    def __init__(self, settings=None):
        self._settings = settings

    def generate_random_position(self, min_width, max_width, min_height, max_height):
        return (randint(min_width, max_width), randint(min_height, max_height))