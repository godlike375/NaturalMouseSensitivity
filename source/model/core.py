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


def vertical_vector(vec: Vector) -> Vector:
    return Vector(0, vec.y, vec.z)

def horizontal_vector(vec: Vector) -> Vector:
    return Vector(vec.x, 0, vec.z)

def append_flicks(overflicks, underflicks, result):
    if result >= 1:
        underflicks.append(result)
    else:
        overflicks.append(result)

def remove_percentiles(overflicks, underflicks, percentile):
    overflicks = overflicks[int(len(overflicks) * percentile): int(len(overflicks) * 1 - percentile)]
    underflicks = underflicks[int(len(underflicks) * percentile): int(len(underflicks) * 1 - percentile)]
    return overflicks, underflicks

def calculate_average_delta_diff(flicks_targets: List[FlickAndTarget]) -> float:
    average_result = 0
    horizontal_overflicks = []
    horizontal_underflicks = []
    horizontal_packed = (horizontal_overflicks, horizontal_underflicks,)

    vertical_overflicks = []
    vertical_underflicks = []
    vertical_packed = (vertical_overflicks, vertical_underflicks,)
    # сбалансированное среднее (ср1*(к2 / к1) + ср2 (к1 / к2) )/ 2
    for i in flicks_targets:
        horizontal_angle_actual = horizontal_vector(i.flick.start).angle_deg(horizontal_vector(i.flick.end))
        vertical_angle_actual = vertical_vector(i.flick.start).angle_deg(vertical_vector(i.flick.end))

        horizontal_angle_expected = horizontal_vector(i.flick.start).angle_deg(horizontal_vector(i.target.center))
        vertical_angle_expected = vertical_vector(i.flick.start).angle_deg(vertical_vector(i.target.center))

        #actual = i.flick.angle_between_start_end()
        #expected = i.flick.start.angle_deg(i.target.center)
        #result = expected / actual

        horizontal_result = horizontal_angle_expected / horizontal_angle_actual
        vertical_result = vertical_angle_expected / vertical_angle_actual

        append_flicks(*horizontal_packed, horizontal_result)
        append_flicks(*vertical_packed, vertical_result)


    # TODO: отфильтровать выбросы нахер

    horizontal_overflicks.sort()
    horizontal_underflicks.sort()

    vertical_overflicks.sort()
    vertical_underflicks.sort()

    percentile = 0.115

    horizontal_packed = \
        remove_percentiles(*horizontal_packed, percentile)

    vertical_packed = \
        remove_percentiles(*vertical_packed, percentile)

    horizontal_flicks = [*horizontal_packed[0], *horizontal_packed[1]]
    vertical_flicks = [*vertical_packed[0], *vertical_packed[1]]
    return mean(horizontal_flicks), mean(vertical_flicks)
    #return (mean(overflicks) + mean(underflicks)) / 2


def vector_length_distance(v1: Vector):
    return sqrt(v1.x ** 2 + v1.y ** 2 + v1.z ** 2)
