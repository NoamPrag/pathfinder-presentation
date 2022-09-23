from manim import *

from algorithm.pathfinder import *


def get_vel_graph_points(trajectory: list[TrajectoryPoint], ax: Axes, dt: float = 0.005) -> list[Dot]:
    t = 0
    last_search_index = 0
    dots: list[Dot] = []
    while t <= trajectory[-1].time:
        point_index = search_for_time(trajectory, t, last_search_index)
        last_search_index = point_index
        dot = Dot(
            ax.coords_to_point(trajectory[point_index].time,
            trajectory[point_index].vel),
            radius=0.03,
        )
        dots.append(dot)
        t += dt
    return dots
