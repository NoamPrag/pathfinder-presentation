from constants import *
from manim import *
from manim_revealjs import PresentationScene

config.video_dir = "./videos"

# trajectory: list[TrajectoryPoint] = create_trajectory_list(example_path)
# calculate_kinematics(trajectory, acc_forward=True)
# trajectory = reverse_trajectory(trajectory)
# calculate_kinematics(trajectory, acc_forward=False)
# trajectory = reverse_trajectory(trajectory)

class AccForward(PresentationScene):
    def max_acc_forward_eq(self) -> MathTex:
        eq = MathTex(r"a = a_{max} (1 - \frac{v}{v_{max}})")
        eq[0][0].set_color(colors["a"])
        eq[0][2:6].set_color(colors["a"])
        eq[0][-7].set_color(colors["v"])
        eq[0][-5:-1].set_color(colors["v"])
        return eq

    def construct(self):
        acc_forward_eq = self.max_acc_forward_eq()
        acc_forward_eq.shift(UP*3.25)
        self.play(Write(acc_forward_eq))
        self.end_fragment()

        ax = Axes(
            x_range = [0, 5, 1],
            y_range = [0, 9, 1],
            x_length=9,
            axis_config={"include_numbers": True},
        )
        x_label = ax.get_x_axis_label(r"v [\frac{m}{s}]", direction=1.25*RIGHT+0.05*DOWN)
        y_label = ax.get_y_axis_label(r"a [\frac{m}{s^2}]", direction=1.5*UP+3*LEFT)
        ax_labels = VGroup()
        ax_labels.add(x_label)
        ax_labels.add(y_label)
        self.play(DrawBorderThenFill(ax), Create(ax_labels))
        self.end_fragment()

        acc_graph = ax.plot(lambda v: MAX_ACC * (1 - v/MAX_VEL), x_range=[0, MAX_VEL]).set_color(BLUE)
        self.play(Create(acc_graph))

        v_max_tex: MathTex = MathTex(r"v_{max}").set_color(RED)
        v_max_tex.next_to(ax.coords_to_point(MAX_VEL, 0), DOWN*0.75+LEFT*0.3)

        a_max_tex: MathTex = MathTex(r"a_{max}").set_color(BLUE)
        a_max_tex.next_to(ax.coords_to_point(0, MAX_ACC), LEFT)
        self.play(Write(v_max_tex), Write(a_max_tex))
        self.end_fragment()
