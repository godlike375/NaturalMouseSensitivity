
from source.model.core import Flick, calculate_average_delta_diff
from source.aliases import Vector

def test_flick_calculation():
    targets, flicks = [Vector(2, 2), Vector(10, 10), Vector(4, 4), Vector(100, 100)],\
                        [Flick(Vector(0, 0), Vector(3, 3)), Flick(Vector(4, 4), Vector(12, 12)),
                         Flick(Vector(100, 100), Vector(6, 6)), Flick(Vector(50, 50), Vector(105, 105))]

    delta = calculate_average_delta_diff(targets, flicks)

    assert delta