from manim import *
from manim_revealjs import PresentationScene
from utils.bezier import Bezier
from utils.utils import (complex_to_array, connect_the_dots, create_all,
                         dot_from_complex, dot_with_title)

config.video_dir = "./videos"

class CubicBezier(PresentationScene):
    def write_title(self):
        title = Text("Cubic Bèzier")
        title.shift(UP*3.5)
        self.play(Write(title))

    def construct(self):
        self.write_title()
        self.end_fragment()

        bezier_points: list[complex] = [0, 2j, 2+2j, 4]
        bezier = Bezier(bezier_points).translate(-3-2.5j).scale(2)

        bezier_f = bezier.parametric_function().set_color(BLUE)

        bezier_dots: list[Dot] = bezier.dots()
        for dot in bezier_dots: dot.set_color(GREEN)

        bezier_lines: list[Line] = bezier.lines()

        self.play(*create_all(bezier_lines), *create_all(bezier_dots))
        self.end_fragment()


        sub_points: list[list[complex]] = Bezier.sub_points(bezier.points, 0.5)
        sub_dots: list[list[Dot]] = []
        sub_lines: list[list[Line]] = []
        for i, sub_points_list in enumerate(sub_points):
            dots = [dot_from_complex(z) for z in sub_points_list]
            for dot in dots: dot.set_color(RED if i != len(sub_points)-1 else BLUE)
            sub_dots.append(dots)
            self.play(*create_all(dots))
            self.add(*dots)
            if len(sub_points_list) > 1:
                lines = connect_the_dots(sub_points_list)
                sub_lines.append(lines)
                self.play(*create_all(lines))
                self.add(*lines)

        s_eq_tex = MathTex("s =")
        s_eq_tex.shift(RIGHT*4)
        s_eq_tex.shift(UP*1)
        s_value_text = DecimalNumber(0.5)
        s_value_text.next_to(s_eq_tex, RIGHT)
        s_tracker = ValueTracker(0.5)
        s_value_text.add_updater(lambda v: v.set_value(s_tracker.get_value()))
        self.play(Write(s_eq_tex), Write(s_value_text))
        self.end_fragment()


        # Adding updater functions for sub points
        def calculate_sub_point(i: int, j: int):
            return Bezier.sub_points(bezier.points, s_tracker.get_value())[i][j]
        def get_point_updater(i: int, j: int):
            return lambda d: d.move_to(complex_to_array(calculate_sub_point(i, j)))
        for i, sub_dots_list in enumerate(sub_dots):
            for j, dot in enumerate(sub_dots_list):
                dot.add_updater(get_point_updater(i, j))
        # Adding updater functions for sub lines
        def get_line_updater(i: int, j: int):
            return lambda l: l.set_points_by_ends(
                    start=complex_to_array(Bezier.sub_points(bezier.points, s_tracker.get_value())[i][j]),
                    end=complex_to_array(Bezier.sub_points(bezier.points, s_tracker.get_value())[i][j+1]),
                )
        for i, sub_lines_list in enumerate(sub_lines):
            for j, line in enumerate(sub_lines_list):
                line.add_updater(get_line_updater(i, j))

        # Showing recursive algorithm
        self.play(s_tracker.animate.set_value(0.9), run_time=1.5)
        self.wait(0.25)
        self.play(s_tracker.animate.set_value(0.1), run_time=1.5)
        self.wait(0.25)
        self.play(s_tracker.animate.set_value(1), run_time=1.5)
        self.wait(0.25)
        self.play(s_tracker.animate.set_value(0), run_time=1.5)
        self.end_fragment()

        # drawing curve
        self.play(s_tracker.animate.set_value(1), Create(bezier_f), run_time=3)
        self.end_fragment()

