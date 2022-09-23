from constants import *
from manim import *
from manim_revealjs import PresentationScene

config.video_dir = "./videos"

class KinematicsAlgorithm(PresentationScene):
    def write_title(self):
        title = Text("Kinematics algorithm")
        title.shift(UP*3.5)
        self.play(Write(title))

    def zero_eq(self) -> MathTex:
        eq = MathTex(r"t_0 = 0, \quad v_0 = 0, \quad a_0 = 0")
        eq[0][:2].set_color(colors["t"])
        eq[0][5:7].set_color(colors["v"])
        eq[0][10:12].set_color(colors["a"])
        return eq

    def vel_eq(self) -> MathTex:
        eq = MathTex(r"v_n = v_{n-1} + a_{n-1} \Delta t")
        eq[0][0:2].set_color(colors["v"])
        eq[0][3:7].set_color(colors["v"])
        eq[0][-6:-2].set_color(colors["a"])
        eq[0][-2:].set_color(colors["t"])
        return eq

    def acc_eq(self) -> MathTex:
        eq = MathTex(r"a_n = a_{n-1} + j \Delta t")
        eq[0][0:2].set_color(colors["a"])
        eq[0][3:7].set_color(colors["a"])
        eq[0][-3].set_color(colors["j"])
        eq[0][-2:].set_color(colors["t"])
        return eq

    def average_v_eq(self) -> MathTex:
        average_v_eq = MathTex(r"v = \frac{\Delta x}{\Delta t}")
        average_v_eq[0][0].set_color(colors["v"])
        average_v_eq[0][2:4].set_color(colors["x"])
        average_v_eq[0][5:7].set_color(colors["t"])
        return average_v_eq

    def delta_t_eq(self) -> MathTex:
        eq = MathTex(r"\Delta t = \frac{\Delta x}{v_{n-1}}")
        eq[0][:2].set_color(colors["t"])
        eq[0][3:5].set_color(colors["x"])
        eq[0][6:].set_color(colors["v"])
        return eq

    def xt_eq(self) -> MathTex:
        eq = MathTex(r"x(t) = \frac{1}{6} j \Delta t^3")
        eq[0][0].set_color(colors["x"])
        eq[0][2].set_color(colors["t"])
        eq[0][-4].set_color(colors["j"])
        eq[0][-3:-1].set_color(colors["t"])
        return eq

    def x1_eq(self) -> MathTex:
        eq = MathTex(r"x_1= \frac{1}{6} j t_{1}^3")
        eq[0][:2].set_color(colors["x"])
        eq[0][-4].set_color(colors["j"])
        eq[0][-3].set_color(colors["t"])
        eq[0][-1].set_color(colors["t"])
        return eq

    def t1_eq(self) -> MathTex:
        eq = MathTex(r"t_1 = (6x_1j)^{\frac{1}{3}}")
        eq[0][:2].set_color(colors["t"])
        eq[0][5:7].set_color(colors["x"])
        eq[0][7].set_color(colors["j"])
        return eq

    def a1v1_eq(self) -> MathTex:
        eq = MathTex(r"a_1 = jt_1, \quad v_1 = \frac{1}{2}jt_1^2")
        eq[0][:2].set_color(colors["a"])
        eq[0][3].set_color(colors["j"])
        eq[0][4:6].set_color(colors["t"])

        eq[0][7:9].set_color(colors["v"])
        eq[0][-4].set_color(colors["j"])
        eq[0][-3].set_color(colors["t"])
        eq[0][-1].set_color(colors["t"])
        return eq

    def construct(self):
        self.write_title()
        self.end_fragment()

        zero_eq = self.zero_eq()
        zero_eq.shift(UP*2.5)
        self.play(Write(zero_eq)) # write zero equations

        acc_eq = self.acc_eq()
        acc_eq.next_to(zero_eq, DOWN*1.5)

        vel_eq = self.vel_eq()
        vel_eq.next_to(acc_eq, DOWN)

        acc_eq.generate_target()
        vel_eq.generate_target()
 
        self.play(Write(vel_eq), Write(acc_eq))
        self.end_fragment() # write general vel and acc equations

        acc_eq.target.shift(DOWN*1.25)
        vel_eq.target.shift(DOWN*1.25)
        self.play(MoveToTarget(acc_eq), MoveToTarget(vel_eq))

        average_v_eq = self.average_v_eq()
        average_v_eq.next_to(acc_eq, UP)
        average_v_eq.generate_target()
        self.play(Write(average_v_eq))
        self.end_fragment() # moving general equations down and writing average v

        delta_t_eq = self.delta_t_eq()
        delta_t_eq.next_to(acc_eq, UP)
        delta_t_eq.generate_target()
        self.play(TransformMatchingShapes(average_v_eq, delta_t_eq))
        self.end_fragment() # transform average eq to ∆t


        delta_t_eq.target.shift(DOWN*2.5)
        average_v_eq.target.shift(DOWN*2.5)
        acc_eq.target.shift(DOWN*2.5)
        vel_eq.target.shift(DOWN*2.5)
        self.play(MoveToTarget(acc_eq), MoveToTarget(vel_eq), MoveToTarget(delta_t_eq))
        self.end_fragment() # move all down

        xt_eq = self.xt_eq()
        xt_eq.next_to(zero_eq, DOWN)
        self.play(Write(xt_eq))
        self.end_fragment() # writing x(t) equation

        x1_eq = self.x1_eq()
        x1_eq.next_to(zero_eq, DOWN)
        self.play(Transform(xt_eq, x1_eq))
        self.end_fragment() # transforming x(t) to x1

        t1_eq = self.t1_eq()
        t1_eq.next_to(zero_eq, DOWN)
        self.play(TransformMatchingShapes(x1_eq, t1_eq))
        self.end_fragment() # transforming x1 to t1

        a1v1_eq = self.a1v1_eq()
        a1v1_eq.next_to(t1_eq, DOWN)
        self.play(Write(a1v1_eq))
        self.end_fragment() # writing equations for v1 and a1
