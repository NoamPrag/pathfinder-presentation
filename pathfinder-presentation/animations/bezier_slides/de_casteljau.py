from manim import *
from manim_revealjs import PresentationScene
from utils.bezier import Bezier
from utils.utils import (complex_to_array, connect_the_dots, create_all,
                         dot_from_complex)

config.video_dir = "./videos"

class DeCasteljau(PresentationScene):
    def write_title(self):
        title = Text("DeCasteljau's Algorithm")
        title.shift(UP*3.5)
        self.play(Write(title))

    def construct(self):
        self.write_title()
        self.end_fragment()

        base_case_tex = MathTex(r"B_{P_0}(s)=P_0", substrings_to_isolate=["B", "s"])
        base_case_tex.set_color_by_tex("B", BLUE)
        base_case_tex.set_color_by_tex("s", RED)
        base_case_tex.shift(UP*1.5)

        general_tex = MathTex(r"B_{P_0, P_1...P_n}(s)=(1-s)B_{P_0, P_1...P_{n-1}}(s) + sB_{P_1, P_2...P_n}(s)", substrings_to_isolate=["B", "s"])
        general_tex.set_color_by_tex("B", BLUE)
        general_tex.set_color_by_tex("s", RED)
        general_tex.next_to(base_case_tex, direction=DOWN*4)

        self.play(Write(base_case_tex))
        self.play(Write(general_tex))
        self.end_fragment()
