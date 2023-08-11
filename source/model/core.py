from dataclasses import dataclass
from math import sqrt
from statistics import mean
from typing import List
from typing import Optional

from source.aliases import Vector


class Flick:
    def __init__(self, start: Optional[Vector] = None, end: Optional[Vector] = None, duration: float = 0.0):
        self.start: Vector = start or Vector(0, 0, 0)
        self.end: Vector = end or Vector(0, 0, 0)
        self.duration: float = duration

    def angle_between_start_end(self):
        return self.start.angle_deg(self.end)

    def get_flick_direction(self):
        direction = self.end - self.start
        dx = direction.x / abs(direction.x) if direction.x != 0 else 0
        dy = direction.y / abs(direction.y) if direction.y != 0 else 0
        dz = direction.z / abs(direction.z) if direction.z != 0 else 0
        return Vector(dx, dy, dz)

    def __str__(self):
        return f'[start=({self.start}), ' \
               f'end=({self.end}), ' \
               f'duration=({round(self.duration, 3)})]'


@dataclass
class Target:
    __slots__ = ['center']
    center: Vector

    def __str__(self):
        return f'[{self.center}]'


@dataclass
class FlickAndTarget:
    __slots__ = ['flick', 'target']
    flick: Flick
    target: Target

    def __str__(self):
        return f'flick={self.flick}  ' \
               f'target=({self.target})'


def calculate_average_delta_diff(flicks_targets: List[FlickAndTarget]) -> float:
    average_result = 0
    overflicks = []
    underflicks = []
    # сбалансированное среднее (ср1*(к2 / к1) + ср2 (к1 / к2) )/ 2
    for i in flicks_targets:
        actual = i.flick.angle_between_start_end()
        expected = i.flick.start.angle_deg(i.target.center)
        result = expected / actual
        if result >= 1:
            underflicks.append(result)
        else:
            overflicks.append(result)

    # TODO: отфильтровать выбросы нахер

    overflicks.sort()
    underflicks.sort()
    percentile = 0.115
    overflicks = overflicks[int(len(overflicks) * percentile): int(len(overflicks) * 1 - percentile)]
    underflicks = underflicks[int(len(underflicks) * percentile): int(len(underflicks) * 1 - percentile)]
    flicks = [*overflicks, *underflicks]
    return mean(flicks)
    #return (mean(overflicks) + mean(underflicks)) / 2


def vector_length_distance(v1: Vector):
    return sqrt(v1.x ** 2 + v1.y ** 2 + v1.z ** 2)
