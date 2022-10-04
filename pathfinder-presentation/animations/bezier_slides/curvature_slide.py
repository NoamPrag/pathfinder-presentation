from algorithm.path import Path
from constants import *
from manim import *
from manim_revealjs import PresentationScene
from utils.utils import complex_to_array, dot_from_complex

config.video_dir = "./videos"

class CurvatureSlide(PresentationScene):
    def write_title(self):
        title = Text("Curvature")
        title.shift(UP*3.5)
        self.play(Write(title))

    def curvature_eq(self) -> MathTex:
        return MathTex(r"\kappa = \frac{\Delta \alpha}{\Delta d}")

    def curvature_eq_with_radius(self) -> MathTex:
        return MathTex(r"\kappa = \frac{\Delta \alpha}{\Delta d} = \frac{1}{R}")

    def construct(self):
        self.write_title()
        self.end_fragment()

        path: Path = Path([seg.bezier.translate(-0.5-1.5j) for seg in example_path])
        bezier_fs: list[ParametricFunction] = [b.parametric_function() for b in path.beziers]
        bezier_group = VGroup()
        for bezier in bezier_fs: bezier_group.add(bezier)
        self.play(Create(bezier_group, run_time=4))
        self.end_fragment() # creating path

        curvature_eq = self.curvature_eq()
        curvature_eq.shift(UP*2.5)
        self.play(Write(curvature_eq))
        self.end_fragment() # writing equation for curvature

        dist_tracker = ValueTracker(0)

        dot = always_redraw(lambda: dot_from_complex(path.evaluate_by_distance(dist_tracker.get_value())).set_color(BLUE))
        self.play(Create(dot))

        path_derivative: Path = path.derivative()

        def get_tangent_arrow() -> Arrow:
            dist: float = dist_tracker.get_value()
            s = path.t_for_distance(dist)
            start: complex = path.evaluate(s)
            derivative: complex = path_derivative.evaluate(s)
            end: complex = start + derivative / abs(derivative)
            return Arrow(start=complex_to_array(start), end=complex_to_array(end)).set_color(RED)

        tangent_arrow = always_redraw(get_tangent_arrow)
        self.play(Create(tangent_arrow))        
        self.end_fragment() # creating dot and tangent arrow

        self.play(dist_tracker.animate.set_value(path_length), run_time=8)
        self.end_fragment() # moving to end of path

        curvature_eq_with_radius = self.curvature_eq_with_radius()
        curvature_eq_with_radius.shift(UP*2.5)
        self.play(TransformMatchingShapes(curvature_eq, curvature_eq_with_radius))
        self.end_fragment()

        self.play(FadeOut(tangent_arrow))
        self.play(dist_tracker.animate.set_value(0.5), run_time=2)

        def get_tangent_circle() -> Circle:
            dist: float = dist_tracker.get_value()
            s = path.t_for_distance(dist)
            start: complex = path.evaluate(s)
            derivative: complex = path_derivative.evaluate(s)
            curvature: float = path.curvature(s)
            radius: float = 1 / curvature
            end: complex = start + (derivative / abs(derivative) * -1j * radius)
            return Circle(arc_center=complex_to_array(end), radius=radius).set_color(RED)
        circle = always_redraw(get_tangent_circle)
        self.play(Create(circle))
        self.end_fragment() # creating tangent circle
        
        self.play(dist_tracker.animate.set_value(path_length), run_time=8)
        self.end_fragment() # moving to end of path
