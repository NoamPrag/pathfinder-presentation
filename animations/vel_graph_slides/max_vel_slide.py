from constants import *
from manim import *
from manim_revealjs import PresentationScene

config.video_dir = "./videos"


class MaxVelSlide(PresentationScene):
    def construct(self):
        ax = Axes(
            x_range = [0, path_length+1, 1],
            y_range = [0, 4.5, 0.5],
            axis_config={"include_numbers": True},
            x_length=9
        )
        # Labels for the x-axis and y-axis.
        y_label = ax.get_y_axis_label(r"v [\frac{m}{s}]", direction=1.5*UP+3*LEFT)
        x_label = ax.get_x_axis_label(r"d [m]", direction=1.25*RIGHT+0.05*DOWN)
        ax_labels = VGroup(x_label, y_label)

        self.play(DrawBorderThenFill(ax), Create(ax_labels))
        self.end_fragment() # draw axes

        constant_max_vel_graph = ax.plot(lambda _: MAX_VEL)
        self.play(Create(constant_max_vel_graph))
        self.end_fragment()

        self.play(Uncreate(constant_max_vel_graph))

        max_velocities = [seg.max_vel for seg in example_path]

        segment_limited_vel_graphs = []
        start_x = 0
        end_x = 0
        for max_vel, length, color in zip(max_velocities, segments_lengths, segments_colors):
            end_x += length
            graph = ax.plot(lambda _: max_vel, x_range=[start_x, end_x]).set_color(color)
            segment_limited_vel_graphs.append(graph)
            start_x = end_x

        for graph in segment_limited_vel_graphs: self.play(Create(graph))
        self.end_fragment()
