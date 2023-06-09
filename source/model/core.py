from dataclasses import dataclass
from typing import List

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

#class DataHolder:
#    def __init__(self):
#        self._flicks_targets


def calculate_average_delta_diff(flicks_targets: List[FlickAndTarget]) -> float:
    average_result = 0
    for i in flicks_targets:
        actual = i.flick.start.calc_distance(i.flick.end)
        expected = i.flick.start.calc_distance(i.target.center)
        result = min(actual, expected) / max(actual, expected)
        average_result += result if expected < actual else -result

    return 1 + average_result / len(flicks_targets)
