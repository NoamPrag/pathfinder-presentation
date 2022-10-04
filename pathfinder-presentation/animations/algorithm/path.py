from __future__ import annotations

from utils.bezier import Bezier


class Path:
    def __init__(self, beziers: list[Bezier]) -> None:
        self.beziers = beziers
        self.number_of_beziers = len(beziers)
        self.t_for_each_bezier = 1 / self.number_of_beziers

    def length(self) -> float:
        return sum([bezier.length() for bezier in self.beziers])

    def get_bezier_index_and_t(self, t: float) -> tuple(int, float):
        if t >= 1: return (self.number_of_beziers - 1, 1)

        unscaled_t_for_bezier = t % self.t_for_each_bezier
        t_for_evaluated_bezier = unscaled_t_for_bezier / self.t_for_each_bezier
        evaluated_bezier_index = int((t - unscaled_t_for_bezier) / self.t_for_each_bezier)
        return evaluated_bezier_index, t_for_evaluated_bezier

    def evaluate(self, t: float) -> complex:
        index, t_for_bezier = self.get_bezier_index_and_t(t)
        return self.beziers[index].evaluate(t_for_bezier)

    def curvature(self, t: float) -> float:
        index, t_for_bezier = self.get_bezier_index_and_t(t)
        return self.beziers[index].curvature(t_for_bezier)

    def derivative(self) -> Path:
        return Path([bezier.derivative() for bezier in self.beziers])

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
