from manim import *

from algorithm.path import Path
from algorithm.pathfinder import *


def generate_graph_points(
    trajectory: list[TrajectoryPoint],
    ax: Axes,
    f: Callable[[TrajectoryPoint], tuple[float, float]],
    dt: float = 0.005,
) -> list[Dot]:
    t: float = 0
    last_search_index: int = 0
    dots: list[Dot] = []
    while t <= trajectory[-1].time:
        point_index: int = search_for_time(trajectory, t, last_search_index)
        last_search_index = point_index
        point: tuple[float, float] = f(trajectory[point_index])
        dot = Dot(
            ax.coords_to_point(point[0], point[1]),
            radius=0.03,
        )
        dots.append(dot)
        t += dt
    return dots


def get_vel_time_graph(
    trajectory: list[TrajectoryPoint], ax: Axes, dt: float = 0.005
) -> VGroup:
    graph = VGroup()
    dots: list[Dot] = generate_graph_points(
        trajectory, ax, lambda p: (p.time, p.vel), dt=dt
    )
    for dot in dots:
        graph.add(dot)
    return graph


def get_vel_graph_points(
    trajectory: list[TrajectoryPoint], ax: Axes, dt: float = 0.005
) -> list[Dot]:
    t: float = 0
    last_search_index: int = 0
    dots: list[Dot] = []
    while t <= trajectory[-1].time:
        point_index: int = search_for_time(trajectory, t, last_search_index)
        last_search_index = point_index
        dot = Dot(
            ax.coords_to_point(
                trajectory[point_index].time, trajectory[point_index].vel
            ),
            radius=0.03,
        )
        dots.append(dot)
        t += dt
    return dots
