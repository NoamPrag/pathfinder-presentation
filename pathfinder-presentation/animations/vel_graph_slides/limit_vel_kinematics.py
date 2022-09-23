from algorithm.pathfinder import *
from constants import *
from manim import *
from manim_revealjs import PresentationScene

config.video_dir = "./videos"

trajectory: list[TrajectoryPoint] = create_trajectory_list(example_path)
limit_vel_kinematics(trajectory)

class LimitVelKinematics(PresentationScene):
    def construct(self):
        ax = Axes(
            x_range = [0, trajectory[-1].time, 0.5],
            y_range = [0, 4.5, 0.5],
            x_length=9
        )
        x_label = ax.get_x_axis_label(r"t [s]", direction=1.25*RIGHT+0.05*DOWN)
        y_label = ax.get_y_axis_label(r"v [\frac{m}{s}]", direction=1.5*UP+3*LEFT)
        ax_labels = VGroup()
        ax_labels.add(x_label)
        ax_labels.add(y_label)

        self.play(DrawBorderThenFill(ax), Create(ax_labels))
        self.end_fragment() # drawing axes and labels

        dot_group = VGroup()
        dt = 0.0005
        t = 0
        last_search_index = 0
        while t <= trajectory[-1].time:
            point_index = search_for_time(trajectory, t, last_search_index)
            last_search_index = point_index
            dot = Dot(
                ax.coords_to_point(trajectory[point_index].time,
                trajectory[point_index].vel),
                radius=0.02,
            )
            dot_group.add(dot)
            t += dt
        self.play(ShowIncreasingSubsets(dot_group), run_time=2)
        self.end_fragment()
