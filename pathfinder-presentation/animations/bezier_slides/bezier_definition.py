from manim import *
from manim_revealjs import PresentationScene
from utils.utils import complex_to_array

config.video_dir = "./videos"

class BezierDefinition(PresentationScene):
    def construct(self):
        title = Text("Bézier curve - Definition")
        title.shift(UP*3.5)
        self.play(Write(title))
        self.end_fragment()

        p0 = -2 - 2j
        p1 = 2 + 1j

        p0_dot = Dot(complex_to_array(p0))
        p1_dot = Dot(complex_to_array(p1))

        p0_text = MathTex("P_0")
        p1_text = MathTex("P_1")
        p0_text.next_to(p0_dot, UP)
        p1_text.next_to(p1_dot, UP)

        self.play(Create(p0_dot), Create(p1_dot), Write(p0_text), Write(p1_text))
        self.end_fragment()

        line = Line(start=complex_to_array(p0), end=complex_to_array(p1))
        self.play(Create(line))
        self.end_fragment()

        b_equation = MathTex("B(s) = (1-s)P_0 + sP_1", substrings_to_isolate=["B", "s"])
        b_equation.set_color_by_tex("B", BLUE)
        b_equation.set_color_by_tex("s", RED)
        b_equation.shift(UP*2.5)
        self.play(Write(b_equation))
        self.end_fragment()

        s_eq_tex = MathTex("s =", substrings_to_isolate=["s"])
        s_eq_tex.set_color_by_tex("s", RED)
        s_eq_tex.shift(RIGHT*4)
        s_eq_tex.shift(UP*1)
        s_value_text = DecimalNumber(0.5)
        s_value_text.next_to(s_eq_tex, RIGHT)
        s_tracker = ValueTracker(0.5)

        bezier_value = Dot(complex_to_array((p0+p1)/2))
        bezier_value.set_color(BLUE)
        bezier_value.add_updater(
            lambda b: b.move_to(complex_to_array(s_tracker.get_value()*p1 + (1-s_tracker.get_value())*p0)),
        )
        dot_title = Tex("B(s)", substrings_to_isolate=["B", "s"])
        dot_title.set_color_by_tex("B", BLUE)
        dot_title.set_color_by_tex("s", RED)
        dot_title.next_to(bezier_value, DOWN*0.5+RIGHT*0.5)
        dot_title.add_updater(lambda title: title.next_to(bezier_value, DOWN*0.5+RIGHT*0.5))

        s_value_text.add_updater(lambda v: v.set_value(s_tracker.get_value()))

        self.play(Write(s_eq_tex), Write(s_value_text), Create(bezier_value), Write(dot_title))
        self.end_fragment()

        self.play(s_tracker.animate.set_value(0.1))
        self.wait(0.25)
        self.play(s_tracker.animate.set_value(1))
        self.wait(0.25)
        self.play(s_tracker.animate.set_value(0))
        self.wait(0.25)
        self.play(s_tracker.animate.set_value(0.42))
        self.wait(0.25)

        self.end_fragment()

