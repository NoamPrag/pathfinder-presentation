from manim import *
from manim_revealjs import PresentationScene
from utils.bezier import Bezier
from utils.utils import (complex_to_array, dot_from_complex, lerp,
                         quadratic_lerp)

config.video_dir = "./videos"

class QuadraticBezier(PresentationScene):
    def construct(self):
        title = Text("Quadratic Bèzier")
        title.shift(UP*3.5)
        self.play(Write(title))
        self.end_fragment() # write title

        p0 = -4-3j
        p1 = 0+1j
        p2 = 3-1.5j
        p0_dot = dot_from_complex(p0)
        p1_dot = dot_from_complex(p1)
        p2_dot = dot_from_complex(p2)
        p0_title = MathTex("P_0")
        p1_title = MathTex("P_1")
        p2_title = MathTex("P_2")
        p0_title.next_to(p0_dot, UP)
        p1_title.next_to(p1_dot, UP)
        p2_title.next_to(p2_dot, UP)
        self.play(Create(p0_dot), Create(p1_dot), Create(p2_dot), Write(p0_title), Write(p1_title), Write(p2_title))
        self.end_fragment() # creating dot and dots' titles

        b_eq = MathTex(r"B_{P_0, P_1, P_2}(s)=(1-s)B_{P_0, P_1}(s)+sB_{P_1, P_2}(s)", substrings_to_isolate=["B", "s"])
        b_eq.set_color_by_tex("B", BLUE)
        b_eq.set_color_by_tex("s", RED)
        b_eq.shift(UP*2.5)
        self.play(Write(b_eq))
        self.end_fragment() # writing equation for quadratic bezier

        
        b_01_line = Line(start=complex_to_array(p0), end=complex_to_array(p1))
        b_12_line = Line(start=complex_to_array(p1), end=complex_to_array(p2))
        self.play(Create(b_01_line), Create(b_12_line))
        self.end_fragment() # creating linear beziers

        s_eq_tex = MathTex("s =", substrings_to_isolate=["s"])
        s_eq_tex.set_color_by_tex("s", RED)
        s_eq_tex.shift(RIGHT*4)
        s_eq_tex.shift(UP*1)
        s_value_text = DecimalNumber(0.5)
        s_value_text.next_to(s_eq_tex, RIGHT)
        s_tracker = ValueTracker(0.5)

        s_value_text.add_updater(lambda v: v.set_value(s_tracker.get_value()))

        b_01_value = Dot(complex_to_array(lerp(p0, p1, s_tracker.get_value())))
        b_12_value = Dot(complex_to_array(lerp(p1, p2, s_tracker.get_value())))
        b_01_value.add_updater(lambda v: v.move_to(complex_to_array(lerp(p0, p1, s_tracker.get_value()))))
        b_12_value.add_updater(lambda v: v.move_to(complex_to_array(lerp(p1, p2, s_tracker.get_value()))))
        b_01_value.set_color(BLUE)
        b_12_value.set_color(BLUE)

        b_01_title = MathTex("B_{P_0, P_1}(s)", substrings_to_isolate=["B", "s"])
        b_01_title.set_color_by_tex("B", BLUE)
        b_01_title.set_color_by_tex("s", RED)
        b_01_title.next_to(b_01_value, UP+LEFT)
        b_01_title.add_updater(lambda t: t.next_to(b_01_value, UP+LEFT))

        b_12_title = MathTex("B_{P_1, P_2}(s)", substrings_to_isolate=["B", "s"])
        b_12_title.set_color_by_tex("B", BLUE)
        b_12_title.set_color_by_tex("s", RED)       
        b_12_title.next_to(b_12_value, DOWN+LEFT)
        b_12_title.add_updater(lambda t: t.next_to(b_12_value, DOWN+LEFT))
        
        self.play(Create(b_01_value), Create(b_12_value), Write(s_eq_tex), Write(s_value_text), Write(b_01_title), Write(b_12_title))

        self.play(s_tracker.animate.set_value(0.1))
        self.wait(0.25)
        self.play(s_tracker.animate.set_value(1))
        self.wait(0.25)
        self.play(s_tracker.animate.set_value(0))
        self.wait(0.25)
        self.play(s_tracker.animate.set_value(0.42))
        self.wait(0.25)
        self.end_fragment() # visualize linear beziers

        
        self.play(Unwrite(b_01_title), Unwrite(b_12_title))
        connecting_line = Line(start=complex_to_array(lerp(p0, p1, s_tracker.get_value())), end=complex_to_array(lerp(p1, p2, s_tracker.get_value())))
        connecting_line.add_updater(lambda l: l.set_points_by_ends(start=complex_to_array(lerp(p0, p1, s_tracker.get_value())), end=complex_to_array(lerp(p1, p2, s_tracker.get_value()))))
        self.play(Create(connecting_line))

        self.play(s_tracker.animate.set_value(0.1))
        self.wait(0.25)
        self.play(s_tracker.animate.set_value(1))
        self.wait(0.25)
        self.play(s_tracker.animate.set_value(0))
        self.wait(0.25)
        self.play(s_tracker.animate.set_value(0.42))
        self.wait(0.25)
        self.end_fragment() # visualize connecting line 

        quad_point = Dot(complex_to_array(quadratic_lerp(p0, p1, p2, s_tracker.get_value())))
        quad_point.set_color(BLUE)
        quad_point_title = MathTex("B_{P_0, P_1, P_2}(s)", substrings_to_isolate=["B", "s"])
        quad_point_title.set_color_by_tex("B", BLUE)
        quad_point_title.set_color_by_tex("s", RED)
        quad_point_title.next_to(quad_point, DOWN*1.5+RIGHT)

        quad_point.add_updater(lambda p: p.move_to(complex_to_array(quadratic_lerp(p0, p1, p2, s_tracker.get_value()))))
        quad_point_title.add_updater(lambda t: t.next_to(quad_point, DOWN*1.5+RIGHT))

        self.play(Create(quad_point), Write(quad_point_title))
        self.end_fragment() # creating the quadratic bezier point on the connecting line


        self.play(s_tracker.animate.set_value(0.1))
        self.wait(0.25)
        self.play(s_tracker.animate.set_value(1))
        self.wait(0.25)
        self.play(s_tracker.animate.set_value(0))
        self.wait(0.25)
        self.play(s_tracker.animate.set_value(0.42))
        self.wait(0.25)
        self.end_fragment() # visualize point movement

        self.play(s_tracker.animate.set_value(0))
        self.wait(1)

        quad_bezier = Bezier(points=[p0, p1, p2])
        bezier_func = quad_bezier.parametric_function().set_color(BLUE)
        self.play(Create(bezier_func), s_tracker.animate.set_value(1), run_time=1)
        self.end_fragment() # draw quadratic bezier
