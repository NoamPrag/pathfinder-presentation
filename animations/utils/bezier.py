from __future__ import annotations

from functools import reduce

import numpy as np
from manim import *

from utils.bernstein import get_bernstein
from utils.utils import determinant, dot_from_complex, lerp, line_from_complex


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
        if len(self.points) == 0: return Bezier([])

        new_points: list[complex] = [self.points[0]]
        for point in self.points[1:]:
            new_points.append(lerp(self.points[0], point, factor))
        return Bezier(new_points)
    
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

    def t_for_distance(self, distance: float, delta_distance: float = 1e-3) -> float:
        distance_accumulator: float = 0
        t: float = 0
        derivative = self.derivative()
        prev_point = self.evaluate(0)
        while t <= 1:
            t += delta_distance / abs(derivative.evaluate(t)) 

            curr_point = self.evaluate(t)
            distance_accumulator += abs(curr_point - prev_point)
            prev_point = curr_point

            if distance_accumulator >= distance: return t

    def evaluate_by_distance(self, distance: float, delta_distance: float = 1e-3) -> complex:
        return self.evaluate(self.t_for_distance(distance, delta_distance=delta_distance))
   
    def curvature(self, t: float) -> float:
        derivative = self.derivative()
        second_derivative = derivative.derivative()

        derivative_at_t = derivative.evaluate(t)
        second_derivative_at_t = second_derivative.evaluate(t)
        return determinant(derivative_at_t, second_derivative_at_t) / (abs(derivative_at_t) ** 3)

    def curvature_by_distance(self, distance: float, delta_distance: float = 1e-3) -> float:
        t: float = self.t_for_distance(distance, delta_distance=delta_distance)
        return self.curvature(t)
    
    def manim_bezier(self) -> CubicBezier:
        if (self.degree != 3): raise Exception("Bezier must be cubic in order to be converted to manim bezier.")

        manim_bezier_points = [[point.real, point.imag, 0] for point in self.points]
        return CubicBezier(
            start_anchor=manim_bezier_points[0],
            start_handle=manim_bezier_points[1],
            end_handle=manim_bezier_points[2],
            end_anchor=manim_bezier_points[3],
        )

    def parametric_function(self):
        def points(t):
            return np.array((self.evaluate(t).real, self.evaluate(t).imag, 0))

        return ParametricFunction(points)

    def dots(self) -> list[Dot]:
        return [dot_from_complex(z) for z in self.points]

    def lines(self) -> list[Line]:
        lines_between_dots: list[Line] = []
        for i, point in enumerate(self.points[1:]):
            lines_between_dots.append(line_from_complex(start=self.points[i], end=point))
        return lines_between_dots

    @staticmethod
    def sub_points(points: list[complex], t: float) -> list[list[complex]]:
        if len(points) <= 1: return [points] # base case

        sub_points = [lerp(start, end, t) for start, end in zip(points, points[1:])]

        return [sub_points, *Bezier.sub_points(sub_points, t)]
