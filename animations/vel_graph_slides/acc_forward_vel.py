from algorithm.animations import get_vel_graph_points
from constants import *
from manim import *
from manim_revealjs import PresentationScene

config.video_dir = "./videos"

trajectory: list[TrajectoryPoint] = create_trajectory_list(example_path)
calculate_kinematics(trajectory, acc_forward=True)
trajectory = reverse_trajectory(trajectory)
calculate_kinematics(trajectory, acc_forward=False)
trajectory = reverse_trajectory(trajectory)

class AccForwardVel(PresentationScene):
    def construct(self):
        ax = Axes(
            x_range = [0, 7, 1],
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
        self.play(ShowIncreasingSubsets(dot_group, run_time=2), run_time=2)
        self.end_fragment() # drawing vel graph

        self.play(FadeOut(ax), FadeOut(ax_labels), FadeOut(dot_group))

        breathing_test_image = ImageMobject("./images/breathing-test.jpg").scale(0.7)
        self.play(GrowFromCenter(breathing_test_image))
        self.end_fragment() # fade out all and show image from breathing test
