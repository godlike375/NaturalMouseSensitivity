
from source.model.core import Flick, calculate_average_delta
from source.model.coordinates import Point

def test_flick_calculation():
    targets, flicks = [Point(2, 2), Point(10, 10), Point(4, 4), Point(100, 100)],\
                        [Flick(Point(0, 0), Point(3, 3)), Flick(Point(4, 4), Point(12, 12)),
                         Flick(Point(100, 100), Point(6, 6)), Flick(Point(50, 50), Point(105, 105))]

    delta = calculate_average_delta(targets, flicks)

    assert delta