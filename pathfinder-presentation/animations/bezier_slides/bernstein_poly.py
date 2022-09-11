from manim import *
from manim_revealjs import PresentationScene

config.video_dir = "./videos"

class BernsteinPoly(PresentationScene):
    def write_title(self):
        title = Text("Bernstein Polynomials")
        title.shift(UP*3.5)
        self.play(Write(title))

    def color_tex(self, tex):
        tex.set_color_by_tex("B", BLUE)
        tex.set_color_by_tex("s", RED)
        colors = [GREEN, YELLOW, PURPLE, TEAL]
        for i, color in enumerate(colors):
            tex.set_color_by_tex(f"P_{i}", color)

    def construct(self):
        self.write_title()
        self.end_fragment()

        eq_tex = MathTex(
            "B_{P_0, P_1, P_2, P_3}(s)=(1-s)B_{P_0, P_1, P_2}(s) + sB_{P_1, P_2, P_3}(s)",
            substrings_to_isolate=["B", "s", "P_0", "P_1", "P_2", "P_3"],
        )
        self.color_tex(eq_tex)
        eq_tex.shift(UP*2)
        self.play(GrowFromCenter(eq_tex))
        eq_tex_clone = eq_tex.copy()
        self.add(eq_tex_clone)
        self.end_fragment()

        first_layer = MathTex(
            "B_{P_0, P_1, P_2, P_3}(s)=(1-s)[(1-s)B_{P_0, P_1}(s)+sB_{P_1, P_2}(s)] + s[(1-s)B_{P_1, P_2}(s)+sB_{P_2, P_3}(s)]",
            substrings_to_isolate=["B", "s", "P_0", "P_1", "P_2", "P_3"],
        )
        self.color_tex(first_layer)
        first_layer.scale(0.6)
        first_layer.shift(UP)
        self.play(Transform(eq_tex_clone, first_layer))
        first_layer_clone = first_layer.copy()
        self.add(first_layer_clone)
        self.end_fragment()

        
        second_layer = MathTex(
            "B_{P_0, P_1, P_2, P_3}(s)=(1-s)\{(1-s)[(1-s)P_0+sP_1]+s[(1-s)P_1+sP_2]\} + s\{(1-s)[(1-s)P_1+sP_2]+s[(1-s)P_2+sP_3]\}",
            substrings_to_isolate=["B", "s", "P_0", "P_1", "P_2", "P_3"],
        )
        self.color_tex(second_layer)
        second_layer.scale(0.45)
        self.play(TransformMatchingTex(first_layer_clone, second_layer))
        second_layer_clone = second_layer.copy()
        self.add(second_layer_clone)
        self.end_fragment()

        final_form = MathTex(
            "B_{P_0, P_1, P_2, P_3}(s)=(1-s)^3P_0+3(1-s)^2sP_1+3(1-s)s^2P_2+s^3P_3",
            substrings_to_isolate=["B", "s", "P_0", "P_1", "P_2", "P_3"],
        )
        self.color_tex(final_form)
        final_form.shift(DOWN)
        final_form.scale(0.75)
        self.play(TransformMatchingTex(second_layer_clone, final_form))
        self.end_fragment()

        bernstein_eq = MathTex(r"b_{i,n}(s)=\binom{n}{i}s^i(1-s)^{n-i}")
        bernstein_eq.shift(DOWN*2.5)
        self.play(Write(bernstein_eq))
        self.end_fragment()
