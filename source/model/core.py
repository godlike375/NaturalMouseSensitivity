from dataclasses import dataclass

from source.model.coordinates import Point


@dataclass
class Flick:
    __slots__ = ['start', 'end', 'duration']
    start: Point
    end: Point
    duration: float

    def calc_length(self):
        return self.start.calc_distance(self.end)

@dataclass
class Target:
    __slots__ = ['center']
    center: Point

@dataclass
class FlickAndTarget:
    __slots__ = ['flick', 'target']
    flick: Flick
    target: Target

    def __str__(self):
        return f'[start=({self.flick.start.x}, {self.flick.start.y}), ' \
               f'end=({self.flick.end.x}, {self.flick.end.y}), ' \
               f'duration=({self.flick.duration})],  ' \
               f'[target=({self.target.center.x}, {self.target.center.y})]'

class DataHolder:
    def __init__(self):
        self._flicks_targets


def calculate_average_delta(targets_flicks: list) -> float:
    return targets_flicks
