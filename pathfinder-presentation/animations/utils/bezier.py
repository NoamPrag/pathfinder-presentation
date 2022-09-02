from __future__ import annotations

from functools import reduce

from manim import CubicBezier

from utils.bernstein import get_bernstein


class Bezier:
    def __init__(self, points: list[complex]) -> Bezier:
        self.points = points
        self.degree = len(points) - 1

    def evaluate(self, t: float) -> complex:
        return reduce(
            lambda a, b: a + b,
            [p * get_bernstein(self.degree, i)(t) for i, p in enumerate(self.points)],
            0,
        )

    def derivative(self) -> Bezier:
        return Bezier(
            # points of the derivative are the differences of the curve's points scaled by the curve's degree
            [
                (self.points[i + 1] - p) * self.degree
                for i, p in enumerate(self.points[:-1])
            ]
        )

    def integral(self, c: complex) -> Bezier:
        # c is the "translation" of the curve, so it's the first point
        integral_points = [c]
        for i, p in enumerate(self.points):
            # computing the anti-derivative
            integral_points.append(p / (self.degree + 1) + integral_points[i])

        return Bezier(integral_points)

    def translate(self, translation: complex) -> Bezier:
        return Bezier([point + translation for point in self.points])

    def scale(self, factor: float) -> Bezier:
        return Bezier([point * factor for point in self.points])
    
    def distanced_points(self, distance: float) -> list[complex]:
        derivative: Bezier = self.derivative()

        points: list[complex] = []

        s: float = 0.0
        while s <= 1:
            ds: float = distance / abs(derivative.evaluate(s))
            points.append(self.evaluate(s))
            s += ds
        return points
    
    # empirical integration with dt
    def length(self, dt = 0.01) -> float:
        points = self.distanced_points(dt)
        bezier_length: float = 0.0
        for i, point in enumerate(points[1:]):
            prev_point = points[i] # i is +1 for points[1:]
            bezier_length += abs(point - prev_point)
        return bezier_length
    
    def __len__(self) -> float:
        return self.length()
    
    def manim_bezier(self) -> CubicBezier:
        if (self.degree != 3): raise Exception("Bezier must be cubic in order to be converted to manim bezier.")

        manim_bezier_points = [[point.real, point.imag, 0] for point in self.points]
        return CubicBezier(
            start_anchor=manim_bezier_points[0],
            start_handle=manim_bezier_points[1],
            end_handle=manim_bezier_points[2],
            end_anchor=manim_bezier_points[3],
        )
