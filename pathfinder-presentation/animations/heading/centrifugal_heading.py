from constants import *
from algorithm.animations import get_vel_time_graph, generate_graph_points
from manim import *
from manim_revealjs import PresentationScene

config.video_dir = "./videos"

trajectory: list[TrajectoryPoint] = create_trajectory_list(example_path)
trajectory = do_kinematics(trajectory)
centrifugal_force(trajectory)


def get_curvature_integral(
    ax: Axes, start_time: float, end_time: float, color: str
) -> Polygon:
    start_index = search_for_time(trajectory, start_time)
    end_index = search_for_time(trajectory, end_time, start_index)
    poly_points = [
        ax.coords_to_point(point.time, point.vel)
        for point in trajectory[start_index:end_index]
    ]
    poly = Polygon(*poly_points)
    poly.set_stroke(color=WHITE, width=0, opacity=0)
    poly.set_fill(color=color, opacity=1)
    return poly


class CentrifugalHeading(PresentationScene):
    def v_omega_r_eq(self):
        eq = MathTex(r"v = \omega r")
        eq[0][0].set_color(colors["v"])
        eq[0][2].set_color(colors["w"])
        eq[0][-1].set_color(colors["r"])
        return eq

    def integral_eq(self):
        eq = MathTex(r"\int v")
        eq[0][-1].set_color(colors["v"])
        return eq

    def intergral_with_omega(self):
        eq = MathTex(r"\int v = \int \omega r")
        eq[0][1].set_color(colors["v"])
        eq[0][-2].set_color(colors["w"])
        eq[0][-1].set_color(colors["r"])
        return eq

    def integral_without_r(self):
        eq = MathTex(r"\int v = r \int \omega")
        eq[0][1].set_color(colors["v"])
        eq[0][3].set_color(colors["r"])
        eq[0][-1].set_color(colors["w"])
        return eq

    def integral_with_h(self):
        eq = MathTex(r"\int v = r \int \omega = r \Delta H")
        eq[0][1].set_color(colors["v"])
        eq[0][3].set_color(colors["r"])
        eq[0][-5].set_color(colors["w"])
        eq[0][-3].set_color(colors["r"])
        eq[0][-2:].set_color(colors["h"])
        return eq

    def final_h_eq(self):
        eq = MathTex(r"\Delta H = \frac{\int v}{r}")
        eq[0][:2].set_color(colors["h"])
        eq[0][-3].set_color(colors["v"])
        eq[0][-1].set_color(colors["r"])
        return eq

    def construct(self):
        ax = Axes(
            x_range=[0, 7, 1],
            y_range=[0, 4.5, 0.5],
            x_length=10,
            axis_config={"include_numbers": True},
        )
        x_label = ax.get_x_axis_label(r"t [s]", direction=3 * DOWN)
        y_label = ax.get_y_axis_label(r"v [\frac{m}{s}]", direction=1.5 * UP + 3 * LEFT)
        ax_labels = VGroup()
        ax_labels.add(x_label)
        ax_labels.add(y_label)
        self.play(DrawBorderThenFill(ax), Create(ax_labels))

        limited_vel_points = generate_graph_points(
            trajectory, ax, lambda p: (p.time, p.vel), dt=0.005
        )
        limited_vel_graph = VGroup()
        for point in limited_vel_points:
            limited_vel_graph.add(point)
        self.play(ShowIncreasingSubsets(limited_vel_graph, run_time=3))
        self.end_fragment()  # showing limited vel graph

        first_poly = get_curvature_integral(ax, 2.8, 3.2, colors["h"])
        second_poly = get_curvature_integral(ax, 5.4, 5.65, colors["h"])
        self.play(Create(first_poly), Create(second_poly))
        self.end_fragment()

        v_omega_r_eq = self.v_omega_r_eq()
        v_omega_r_eq.shift(UP * 3)
        self.play(Write(v_omega_r_eq))
        v_omega_r_eq.generate_target()
        v_omega_r_eq.target.shift(RIGHT * 4.5)
        self.play(MoveToTarget(v_omega_r_eq))
        self.end_fragment()

        integral_eq = self.integral_eq()
        integral_eq.shift(UP * 3)
        self.play(Write(integral_eq))
        self.end_fragment()

        integral_with_omega = self.intergral_with_omega()
        integral_with_omega.shift(UP * 3)
        self.play(TransformMatchingShapes(integral_eq, integral_with_omega))
        self.end_fragment()

        integral_without_r = self.integral_without_r()
        integral_without_r.shift(UP * 3)
        self.play(TransformMatchingShapes(integral_with_omega, integral_without_r))
        self.end_fragment()

        integral_with_h = self.integral_with_h()
        integral_with_h.shift(UP * 3)
        self.play(TransformMatchingShapes(integral_without_r, integral_with_h))
        self.end_fragment()

        final_h_eq = self.final_h_eq()
        final_h_eq.shift(UP * 3)
        self.play(
            TransformMatchingShapes(integral_with_h, final_h_eq), FadeOut(v_omega_r_eq)
        )
        self.end_fragment()
