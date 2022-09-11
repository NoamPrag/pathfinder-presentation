from manim import *
from manim_revealjs import PresentationScene
from utils.bezier import Bezier

config.video_dir = "./videos"

class Path(PresentationScene):
    def write_title(self):
        title = Text("Path - a series of Bèziers")
        title.shift(UP*3.5)
        self.play(Write(title))

    def construct(self):
        self.write_title()
        self.end_fragment()

        segments: list[Bezier] = [
            Bezier([0, 1.5j, 0, 0.75]),
            Bezier([0.75, 2.25, 4.5+3j, 1.5+3j]),
            Bezier([1.5+3j, -1.5+3j, -1.5+3j, -1.5+1.5j]),
        ]
        segments = [b.translate(-0.5-1.5j) for b in segments]
        colors = [GREEN, RED, BLUE, ORANGE]
        bezier_fs: list[ParametricFunction] = [b.parametric_function() for b in segments]

        for b, color in zip(bezier_fs, colors): b.set_color(color)
        bezier_group = VGroup()
        for bezier in bezier_fs: bezier_group.add(bezier)
        self.play(Create(bezier_group, run_time=4))
        self.end_fragment() # drawing path

        max_velocities = [1.5, 3.83, 2]
        max_vels = [MathTex(f"{v}") for v in max_velocities]
        directions = [UP, RIGHT, UP]
        for vel, segment, direction in zip(max_vels, bezier_fs, directions): vel.next_to(segment, direction)
        for vel in max_vels: self.play(Write(vel))
        self.end_fragment() # writing vels

        lengths: list[float] = []
        lines: list[Line] = []
        for bezier in segments:
            length = bezier.length()
            start: float = sum(lengths)
            line = Line(
                (start - 5, -1.5, 0),
                (start + length - 5, -1.5, 0),
            )
            lines.append(line)
            lengths.append(length)
        
        for line, color in zip(lines, colors): line.set_color(color)
        vels_after_flatten: list[MathTex] = []
        for line, vel in zip(lines, max_velocities): vels_after_flatten.append(MathTex(f"{vel}").next_to(line, UP))
        
        flat_animations: list[Animation] = []
        for bezier, line, vel, vel_after_flat in zip(bezier_fs, lines, max_vels, vels_after_flatten):
            flat_animations.append(Transform(bezier, line))
            flat_animations.append(Transform(vel, vel_after_flat))

        self.play(*flat_animations)
        self.end_fragment() # flattening path to 1D
