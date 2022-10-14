from constants import *
from manim import *
from manim_revealjs import PresentationScene

config.video_dir = "./videos"

OMEGA_SCALE = 0.2
VEL_SCALE = 0.7

MAX_OMEGA = MAX_VEL / ROBOT_RADIUS

ALLOWED_RIGREON_COLOR = YELLOW


class VelOmegaDiamond(PresentationScene):
    def vel_omega_eq(self) -> MathTex:
        eq = MathTex(r"v + \omega r \leq v_{max}")
        eq[0][0].set_color(colors["v"])
        eq[0][2].set_color(colors["w"])
        eq[0][3].set_color(colors["r"])
        eq[0][-4:].set_color(colors["v"])
        return eq

    def construct(self):
        plane = NumberPlane()
        ax = Axes(axis_config={"include_ticks": False})
        x_label = ax.get_x_axis_label(r"v [m/s]", direction=4 * DOWN + 2.5 * LEFT)
        y_label = ax.get_y_axis_label(
            r"\omega [\frac{rad}{s}]",
            direction=1.5 * UP + 3 * LEFT,
        )
        ax_labels = VGroup()
        ax_labels.add(x_label)
        ax_labels.add(y_label)

        self.play(DrawBorderThenFill(plane), DrawBorderThenFill(ax))

        vel_omega_eq: MathTex = self.vel_omega_eq()
        vel_omega_eq.shift(UP * 3.5 + RIGHT * 4)

        vel_omega_eq.add_background_rectangle(color=BLACK)
        self.play(Write(vel_omega_eq))
        self.end_fragment()  # drawing number plane, axes, and equation

        self.play(Create(ax_labels))  # creating axis labels

        max_vel_tex = MathTex(r"v_{max}").set_color(colors["v"])
        max_vel_tex.next_to(
            plane.coords_to_point(MAX_VEL * VEL_SCALE, 0),
            DOWN * 0.75 + RIGHT * 0.8,
        )
        max_vel_tex.add_background_rectangle(color=BLACK)
        max_vel_dot = Dot(plane.coords_to_point(MAX_VEL * VEL_SCALE, 0)).set_color(
            colors["v"]
        )

        max_omega_tex = MathTex(r"\frac{v_{max}}{r}").set_color(colors["w"])
        max_omega_tex.next_to(
            plane.coords_to_point(0, MAX_OMEGA * OMEGA_SCALE),
            LEFT * 1.5,
        )
        max_omega_tex.add_background_rectangle(color=BLACK)
        max_omega_dot = Dot(
            plane.coords_to_point(0, MAX_OMEGA * OMEGA_SCALE)
        ).set_color(colors["w"])

        self.play(
            Write(max_vel_tex),
            Write(max_omega_tex),
            Create(max_vel_dot),
            Create(max_omega_dot),
        )
        self.end_fragment()  # plot max vel and omega on plane

        allowed_rigeon = Polygon(
            [MAX_VEL * VEL_SCALE, 0, 0],
            [0, MAX_OMEGA * OMEGA_SCALE, 0],
            [-MAX_VEL * VEL_SCALE, 0, 0],
            [0, -MAX_OMEGA * OMEGA_SCALE, 0],
        )
        allowed_rigeon.set_color(ALLOWED_RIGREON_COLOR)
        self.play(Create(allowed_rigeon))

        self.end_fragment()
