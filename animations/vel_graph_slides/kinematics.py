from manim import *
from manim_revealjs import PresentationScene

config.video_dir = "./videos"

colors = {
    "v": RED,
    "a": BLUE,
    "j": PURPLE,
    "t": YELLOW,
}
def color_tex(tex: MathTex):
    for substring, color in colors.items():
        tex.set_color_by_tex(substring, color)

CONSTANT_ACCELERATION = 0.3

class Kinematics(PresentationScene):
    def linear_vel_eq(self) -> MathTex:
        eq = MathTex(r"v(t) = v_0 + at")
        eq[0][0].set_color(colors["v"])
        eq[0][2].set_color(colors["t"])
        eq[0][5:7].set_color(colors["v"])
        eq[0][-2].set_color(colors["a"])
        eq[0][-1].set_color(colors["t"])
        return eq

    def linear_vel_graph(self, ax: Axes) -> Graph:
        return ax.plot(lambda t: t*CONSTANT_ACCELERATION).set_color(colors["v"])
    
    def constant_acc_graph(self, ax: Axes) -> Graph:
        return ax.plot(lambda _: CONSTANT_ACCELERATION*6).set_color(colors["a"])

    def linear_acc_eq(self):
        eq = MathTex(r"a(t) = a_0 + jt")
        eq[0][0].set_color(colors["a"])
        eq[0][2].set_color(colors["t"])
        eq[0][5:7].set_color(colors["a"])
        eq[0][-2].set_color(colors["j"])
        eq[0][-1].set_color(colors["t"])
        return eq

    def parabolic_vel_eq(self) -> MathTex:
        eq = MathTex(r"v(t) = v_0 + a_0 t + \frac{1}{2} j t^2")
        eq[0][0].set_color(colors["v"])
        eq[0][2].set_color(colors["t"])
        eq[0][5:7].set_color(colors["v"])
        eq[0][8:10].set_color(colors["a"])
        eq[0][10].set_color(colors["t"])
        eq[0][-3].set_color(colors["j"])
        eq[0][-2].set_color(colors["t"])
        return eq

    def parabolic_vel_graph(self, ax: Axes) -> Graph:
        return ax.plot(lambda t: 0.025*t**2).set_color(colors["v"])

    def linear_acc_graph(self, ax: Axes) -> Graph:
        return ax.plot(lambda t: 0.4*CONSTANT_ACCELERATION*t).set_color(colors["a"])

    def discrete_vel_eq(self) -> MathTex:
        eq = MathTex(r"v_n = v_{n-1} + a_n \Delta t + \frac{1}{2} j \Delta t^2")
        eq[0][0:2].set_color(colors["v"])
        eq[0][3:7].set_color(colors["v"])
        eq[0][8:10].set_color(colors["a"])
        eq[0][10:12].set_color(colors["t"])
        eq[0][-4].set_color(colors["j"])
        eq[0][-3:-1].set_color(colors["t"])
        return eq

    def discrete_acc_eq(self) -> MathTex:
        eq = MathTex(r"a_n = a_{n-1} + j \Delta t")
        eq[0][0:2].set_color(colors["a"])
        eq[0][3:7].set_color(colors["a"])
        eq[0][-3].set_color(colors["j"])
        eq[0][-2:].set_color(colors["t"])
        return eq
    
    def construct(self):
        ax = Axes(
            x_range = [0, 12, 1],
            y_range = [0, 4.5, 0.5],
            x_length=9
        )
        # Labels for the x-axis and y-axis.
        x_label = ax.get_x_axis_label(r"t [s]", direction=1.25*RIGHT+0.05*DOWN)
        ax_labels = VGroup(x_label)

        self.play(DrawBorderThenFill(ax), Create(ax_labels))
        self.end_fragment() # draw axes

        linear_vel_eq = self.linear_vel_eq()
        linear_vel_eq.shift(UP*3.5)
        self.play(Write(linear_vel_eq))
        self.end_fragment() # draw linear vel equation

        linear_vel_graph = self.linear_vel_graph(ax)
        vel_graph_title = MathTex(r"v(t)", substrings_to_isolate=["v", "t"])
        color_tex(vel_graph_title)
        vel_graph_title.next_to(linear_vel_graph)
        vel_graph_title.shift(2.5*UP)
        self.play(Create(linear_vel_graph))
        self.play(Write(vel_graph_title))
        self.end_fragment() # draw vel graph

        constant_acc_graph = self.constant_acc_graph(ax)
        acc_graph_title = MathTex("a(t)", substrings_to_isolate=["a", "t"])
        color_tex(acc_graph_title)
        acc_graph_title.next_to(constant_acc_graph, RIGHT)
        self.play(Create(constant_acc_graph))
        self.play(Write(acc_graph_title))
        self.end_fragment() # draw acc graph

        self.play(
            Uncreate(linear_vel_graph),
            Unwrite(vel_graph_title),
            Uncreate(constant_acc_graph),
            Unwrite(acc_graph_title),
        )
        self.end_fragment() # remove graphs from screen

        parabolic_vel_eq = self.parabolic_vel_eq()
        parabolic_vel_eq.shift(UP*2.5)
        linear_acc_eq = self.linear_acc_eq()
        linear_acc_eq.shift(UP*3.5)
        self.play(Transform(linear_vel_eq, parabolic_vel_eq))
        self.play(Write(linear_acc_eq))
        self.end_fragment() # displaying equations for parabolic vel

        parabolic_vel_graph = self.parabolic_vel_graph(ax)
        vel_graph_title = MathTex(r"v(t)", substrings_to_isolate=["v", "t"])
        color_tex(vel_graph_title)
        vel_graph_title.next_to(linear_vel_graph)
        vel_graph_title.shift(5.25*UP+9*RIGHT)

        self.play(Create(parabolic_vel_graph))
        self.play(Write(vel_graph_title))
        self.end_fragment() # drawing parabolic velocity graph

        linear_acc_graph = self.linear_acc_graph(ax)
        acc_graph_title = MathTex("a(t)", substrings_to_isolate=["a", "t"])
        color_tex(acc_graph_title)
        acc_graph_title.next_to(constant_acc_graph, RIGHT)
        acc_graph_title.shift(9*RIGHT)

        self.play(Create(linear_acc_graph))
        self.play(Write(acc_graph_title))
        self.end_fragment() # draw linear acceleration graph

        discrete_vel_eq = self.discrete_vel_eq()
        discrete_vel_eq.shift(2.5*UP)

        discrete_acc_eq = self.discrete_acc_eq()
        discrete_acc_eq.shift(UP*3.5)
        self.play(Transform(linear_vel_eq, discrete_vel_eq), Transform(linear_acc_eq, discrete_acc_eq))
        self.end_fragment() # transform equations to discrete form
