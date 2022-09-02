from manim import *
from manim_revealjs import PresentationScene

from utils.bezier import Bezier
from utils.utils import complex_to_array

config.video_dir = "./videos"

class CurveDefinition(PresentationScene):
    def construct(self):
        title = Text("Curves")
        title.shift(UP*3.5)
        self.play(Write(title))
        self.end_fragment()

        beziers: list[Bezier] = [
            Bezier(points=[0, 3j, 6, 4+2j]).translate(-5-3j),
            Bezier(points=[5+3j, 3j, 6, 4+2j]),
            Bezier(points=[0, 3j, 4+3j, 4]).translate(-3j),
            Bezier(points=[0, 2-1j, 2+4j, 4+3j]).translate(-5.5-0.5j)
        ]
        manim_beziers = [b.manim_bezier() for b in beziers]
        for b in manim_beziers: self.play(Create(b))
        self.end_fragment()

        for b in manim_beziers: self.play(FadeOut(b))

        example_bezier = beziers[0].translate(3+2j)
        example_bezier_object = example_bezier.manim_bezier()
        self.play(Create(example_bezier_object))
        self.end_fragment()

        curve_equation = Tex(r"c(t)=(x,\:y)")
        t_range_tex = Tex(r"\[ 0\leq t\leq 1 \]")
        t_range_tex.shift(UP*2.5)
        t_range_tex.shift(RIGHT*1.5)
        curve_equation.shift(UP*2.5)
        curve_equation.shift(LEFT*1.5)
        self.play(Write(curve_equation))
        self.play(Write(t_range_tex))
        self.end_fragment()
        
        t_tracker = ValueTracker(0.5)
        t_text = Tex(r"t =")
        t_text.shift(RIGHT * 4.5)
        t_text.shift(UP * 1)
        t_value = DecimalNumber(0.5)
        t_value.next_to(t_text, RIGHT, aligned_edge=DOWN)
        dot = Dot(complex_to_array(example_bezier.evaluate(0.5)))
        self.play(Create(dot), Write(t_text), Write(t_value))
        dot.add_updater(
            lambda d: d.move_to([(example_bezier.evaluate(t_tracker.get_value())).real, (example_bezier.evaluate(t_tracker.get_value())).imag, 0])
        )
        t_value.add_updater(
            lambda v: v.set_value(t_tracker.get_value())
        )
        self.end_fragment()

        self.play(t_tracker.animate.set_value(0))
        self.wait(0.25)
        self.play(t_tracker.animate.set_value(1))
        self.wait(0.25)
        self.play(t_tracker.animate.set_value(0.7))
        self.end_fragment()
