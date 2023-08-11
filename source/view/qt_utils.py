from PyQt6.QtCore import QPoint

from source.model.coordinates import Vector


def call_slot_interface_wrapper(emit_func, event, _):
    emit_func(event)

def qpoint_to_point(point: QPoint):
    return Vector(point.x(), point.y())