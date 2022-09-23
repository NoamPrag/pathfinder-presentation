from algorithm.animations import get_vel_graph_points
from algorithm.pathfinder import *
from constants import *
from manim import *
from manim_revealjs import PresentationScene

config.video_dir = "./videos"

trajectory: list[TrajectoryPoint] = create_trajectory_list(example_path)
limit_vel_kinematics(trajectory)

class LimitVelKinematics(PresentationScene):
    def construct(self):
        global trajectory

        ax = Axes(
            x_range = [0, 6, 1],
            y_range = [0, 4.5, 0.5],
            x_length=9,
            axis_config={"include_numbers": True},
        )
        x_label = ax.get_x_axis_label(r"t [s]", direction=1.25*RIGHT+0.05*DOWN)
        y_label = ax.get_y_axis_label(r"v [\frac{m}{s}]", direction=1.5*UP+3*LEFT)
        ax_labels = VGroup()
        ax_labels.add(x_label)
        ax_labels.add(y_label)

        self.play(DrawBorderThenFill(ax), Create(ax_labels))
        self.end_fragment() # drawing axes and labels

        dot_group = VGroup()
        dots = get_vel_graph_points(trajectory, ax, dt=0.005)
        for dot in dots: dot_group.add(dot)
        self.play(ShowIncreasingSubsets(dot_group), run_time=2)
        self.end_fragment() # drawing vel graph

        reverse_dot_group = VGroup()

        first_dot_x = dots[0].get_x()
        last_dot_x = dots[-1].get_x()
        for dot in dots:
            dot_x = dot.get_x()
            reversed_x = last_dot_x - (dot_x-first_dot_x)
            reversed_dot = Dot([reversed_x, dot.get_y(), 0], radius=0.03)
            reverse_dot_group.add(reversed_dot)

        self.play(TransformMatchingShapes(dot_group, reverse_dot_group))
        self.end_fragment()

        trajectory = reverse_trajectory(trajectory)
        limit_vel_kinematics(trajectory)

        dots = get_vel_graph_points(trajectory, ax, dt=0.005)
        dot_group = VGroup()
        for dot in dots: dot_group.add(dot)
        self.play(FadeOut(reverse_dot_group))
        self.play(ShowIncreasingSubsets(dot_group))
        self.end_fragment() # draw vel graph with deceleration

        trajectory = reverse_trajectory(trajectory)
        dots = get_vel_graph_points(trajectory, ax, dt=0.005)
        final_dot_group = VGroup()
        for dot in dots: final_dot_group.add(dot)
        self.play(TransformMatchingShapes(dot_group, final_dot_group))
        self.end_fragment() # showing final graph
