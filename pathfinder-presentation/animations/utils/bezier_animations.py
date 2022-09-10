from __future__ import annotations

from manim import *

from bezier import Bezier
from utils.utils import lerp, line_from_complex


def line_from_tuple(start_end: tuple[complex, complex]) -> Line:
    return line_from_complex(start_end[0], start_end[1])


class BezierAnimations:
    def __init__(self, bezier: Bezier) -> BezierAnimations:
        self.bezier = bezier
        self.dots([Dot(p) for p in bezier.points])
        # self.lines_between_dots = [line_from_complex(start, end) for start, end in zip(bezier.points, bezier.points[1:])]
        self.lines_between_dots = list(map(line_from_tuple, zip(bezier.points, bezier.points[1:])))

    # points from linear beziers connecting all of the bezier's points
    def sub_points(self, t: float) -> list[complex]:
        return [lerp(start, end, t) for start, end in zip(self.beziers.points, self.beziers.points[1:])]
