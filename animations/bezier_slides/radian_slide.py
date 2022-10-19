from math import e

from constants import *
from manim import *
from manim_revealjs import PresentationScene

config.video_dir = "./videos"

CIRCLE_CENTER = ORIGIN + DOWN
CIRCLE_RADIUS = 2.5

class RadianSlide(PresentationScene):
    def construct(self):
        circle = Circle(radius=CIRCLE_RADIUS, color=WHITE, arc_center=CIRCLE_CENTER)
        self.play(Create(circle))
        self.end_fragment() # create circle

        angle_tracker = ValueTracker(PI/6)

        zero_line = Line(start=CIRCLE_CENTER, end=CIRCLE_CENTER+RIGHT*CIRCLE_RADIUS)
        angle_line = always_redraw(lambda: Line(start=CIRCLE_CENTER, end=CIRCLE_CENTER+complex_to_R3(CIRCLE_RADIUS * e**(angle_tracker.get_value()*1j))))

        angle_arc = always_redraw(lambda: Arc(radius=0.5, angle=angle_tracker.get_value(), arc_center=CIRCLE_CENTER))
        theta = always_redraw(lambda: MathTex(r"\theta").shift(CIRCLE_CENTER+complex_to_R3(0.8 * e**(angle_tracker.get_value()*0.5j))))
        r = always_redraw(lambda: MathTex(r"R").shift(CIRCLE_CENTER + CIRCLE_RADIUS * 0.5 * RIGHT + 0.5*DOWN))
        self.play(Create(angle_arc), Create(zero_line), Create(angle_line), Write(theta), Write(r))
        self.end_fragment() # create angle on circle

        arc_length_eq = MathTex(r"R \theta = L").shift(UP*3)
        outside_arc = always_redraw(lambda: Arc(radius=CIRCLE_RADIUS, angle=angle_tracker.get_value(), arc_center=CIRCLE_CENTER).set_color(RED))
        l = always_redraw(lambda: MathTex(r"L").shift(CIRCLE_CENTER+complex_to_R3((CIRCLE_RADIUS*1.2) * e**(angle_tracker.get_value()*0.5j))))
        self.play(Create(outside_arc), Write(l), Write(arc_length_eq))
        self.end_fragment() # create angle's arc on circle

        self.play(angle_tracker.animate.set_value(TAU*7/8))
        self.wait(0.25)
        self.play(angle_tracker.animate.set_value(PI/4))
        self.end_fragment() # tweaking angle values

        radius_eq = MathTex(r"R = \frac{L}{\theta}").shift(UP*3)
        self.play(TransformMatchingShapes(arc_length_eq, radius_eq))
        self.wait(1)

        curvature_eq = MathTex(r"\frac{1}{R} = \frac{\theta}{L}").shift(UP*3)
        self.play(TransformMatchingShapes(radius_eq, curvature_eq))
        self.end_fragment()
