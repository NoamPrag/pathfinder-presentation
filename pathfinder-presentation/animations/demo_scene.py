from manim import *
from manim_revealjs import PresentationScene

import utils.bezier

config.video_dir = "./videos"

class BezierScene(PresentationScene):
    def construct(self):
        beziers: list[utils.bezier.Bezier] = [
            utils.bezier.Bezier([0, 1j, 0, 0.5]),
            utils.bezier.Bezier([0.5, 1.5, 3+2j, 1+2j]),
            utils.bezier.Bezier([1+2j, -1+2j, -1+2j, -1+1j]),
        ]
        manim_beziers: list[CubicBezier] = [b.manim_bezier() for b in beziers]

        colors = [GREEN, RED, BLUE, ORANGE]

        for b, color in zip(manim_beziers, colors): b.set_color(color)
        bezier_group = VGroup()
        for bezier in manim_beziers: bezier_group.add(bezier)
        self.play(Create(bezier_group, run_time=4))
        # for b in manim_beziers: self.play(Create(b))
        self.end_fragment()

        bezier_points: list[list[complex]] = [b.distanced_points(0.1) for b in beziers]
        dots: list[list[Dot]] = [[Dot((point.real, point.imag, 0), radius=0.04) for point in points] for points in bezier_points]

        dots_groups = []
        for dots_list in dots:
            group = VGroup()
            for dot in dots_list: group.add(dot)
            dots_groups.append(group)
            
        dots_group = VGroup()
        for bezier_dots, color in zip(dots, colors):
            for dot in bezier_dots:
                dot.set_color(color)
                dots_group.add(dot)
        evaluation_animation_group = AnimationGroup()
        evaluation_animation_group.animations
        for bezier, bezier_dots in zip(manim_beziers, dots_groups):
            evaluation_animation_group.animations.append(Transform(bezier, bezier_dots))
            # self.play(TransformMatchingShapes(bezier, bezier_dots))
        self.play(evaluation_animation_group)
        self.end_fragment()
        return

        lengths: list[float] = []
        lines: list[Line] = []
        for bezier in beziers:
            length = bezier.length()
            start: float = sum(lengths)
            line = Line(
                (start - 2, 0, 0),
                (start + length - 2, 0, 0),
            )
            lines.append(line)
            lengths.append(length)
        
        for line, color in zip(lines, colors): line.set_color(color)
        
        for bezier, line in zip(manim_beziers, lines): self.play(Transform(bezier, line))
        self.end_fragment()

class DemoScene(PresentationScene):
    def construct(self):
        # TODO find out why end_fragment has the t parameter
        rect = Rectangle(fill_color=BLUE, fill_opacity=1)
        self.play(Create(rect))
        self.end_fragment()

        self.play(rect.animate.shift(UP).rotate(PI / 3))
        self.end_fragment()

        self.play(rect.animate.shift(3*LEFT))
        self.end_fragment()
