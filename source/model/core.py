from dataclasses import dataclass

from source.model.coordinates import Point


@dataclass
class Flick:
    __slots__ = ['start', 'end']
    start: Point
    end: Point


class Target:
    @property
    def center(self) -> Point:
        return ...

    def draw(self):
        ...


def calculate_average_delta(targets, flicks) -> float:
    ...
