from constants import *
from manim import *
from manim_revealjs import PresentationScene

config.video_dir = "./videos"


class HeadingPoints(PresentationScene):
    def write_title(self):
        title = Text("Heading points")
        title.shift(UP * 3.5)
        self.play(Write(title))

    def construct(self):
        self.write_title()
        self.end_fragment()

        segments = [seg.bezier for seg in example_path]
        segments = [b.translate(-0.5 - 1.5j) for b in segments]
        colors = [GREEN, RED, BLUE, ORANGE]
        bezier_fs: list[ParametricFunction] = [
            b.parametric_function() for b in segments
        ]

        for b, color in zip(bezier_fs, colors):
            b.set_color(color)
        bezier_group = VGroup()
        for bezier in bezier_fs:
            bezier_group.add(bezier)
        self.play(Create(bezier_group, run_time=4))

        max_velocities = [seg.max_vel for seg in example_path]
        max_vels = [MathTex(f"{v}") for v in max_velocities]
        directions = [UP, RIGHT, UP]
        for vel, segment, direction in zip(max_vels, bezier_fs, directions):
            vel.next_to(segment, direction)
        for vel in max_vels:
            self.play(Write(vel))
        self.end_fragment()  # writing vels

        text_scale = 0.6
        start_dot = Dot(complex_to_R3(segments[0].evaluate(0)))
        start_heading = Text("30°").scale(text_scale).next_to(start_dot, DOWN)

        second_dot = Dot(complex_to_R3(segments[1].evaluate(0)))
        second_heading = Text("0").scale(text_scale).next_to(second_dot, DOWN)

        third_dot = Dot(complex_to_R3(segments[-1].evaluate(1)))
        third_heading = Text("120°").scale(text_scale).next_to(third_dot, DOWN)

        self.play(
            Create(start_dot),
            Create(second_dot),
            Create(third_dot),
            Write(start_heading),
            Write(second_heading),
            Write(third_heading),
        )
        self.end_fragment()
