from constants import *
from manim import *
from manim_revealjs import PresentationScene

config.video_dir = "./videos"

percentage_tracker = ValueTracker(10)

distance = 5
d_heading = PI / 2


def dist_to_acc() -> float:
    return percentage_tracker.get_value() / 100 * distance


def angular_acc(percentage: float, distance: float) -> float:
    return d_heading / (2 * percentage * (1 - percentage) * (distance**2))


def heading_at_end_of_acc(angular_acc: float, dist_to_acc: float) -> float:
    return angular_acc * dist_to_acc**2


def const_omega(percentage: float, distance: float) -> float:
    return d_heading / (distance * (1 - percentage))


def heading_function(d: float) -> float:
    percentage: float = percentage_tracker.get_value() / 100

    angular_acceleration = angular_acc(percentage, distance)
    constant_omega = const_omega(percentage, distance)

    dist_to_acc = percentage * distance
    end_of_acc_heading = heading_at_end_of_acc(angular_acceleration, dist_to_acc)

    if d < dist_to_acc:
        return angular_acceleration * d**2

    if d < distance - dist_to_acc:
        return end_of_acc_heading + constant_omega * (d - dist_to_acc)

    return d_heading - angular_acceleration * (distance - d) ** 2


def dashed_lines_and_dots(ax: Axes) -> tuple[DashedLine, DashedLine]:
    percentage = lambda: percentage_tracker.get_value() / 100

    start_line = always_redraw(
        lambda: DashedLine(
            start=ax.coords_to_point(dist_to_acc(), 0),
            end=ax.coords_to_point(
                dist_to_acc(),
                heading_at_end_of_acc(
                    angular_acc(percentage(), distance),
                    dist_to_acc(),
                ),
            ),
        )
    )

    start_dot = always_redraw(
        lambda: Dot(
            ax.coords_to_point(
                dist_to_acc(),
                heading_at_end_of_acc(
                    angular_acc(percentage(), distance),
                    dist_to_acc(),
                ),
            )
        )
    )

    end_line = always_redraw(
        lambda: DashedLine(
            start=ax.coords_to_point(distance - dist_to_acc(), 0),
            end=ax.coords_to_point(
                distance - dist_to_acc(),
                d_heading
                - heading_at_end_of_acc(
                    angular_acc(percentage(), distance),
                    dist_to_acc(),
                ),
            ),
        )
    )

    end_dot = always_redraw(
        lambda: Dot(
            ax.coords_to_point(
                distance - dist_to_acc(),
                d_heading
                - heading_at_end_of_acc(
                    angular_acc(percentage(), distance),
                    dist_to_acc(),
                ),
            )
        )
    )

    return (start_line, end_line, start_dot, end_dot)


def percentage_texts(ax: Axes) -> tuple[Text, Text]:
    text = lambda: f"{round(percentage_tracker.get_value())}%"
    text_scale_factor: float = 0.6
    start_text = always_redraw(
        lambda: Text(text())
        .next_to(ax.coords_to_point(dist_to_acc() / 2), DOWN * 0.8)
        .scale(text_scale_factor)
    )

    end_text = always_redraw(
        lambda: Text(text())
        .next_to(ax.coords_to_point(distance - dist_to_acc() / 2), DOWN * 0.8)
        .scale(text_scale_factor)
    )
    return (start_text, end_text)


class HeadingSpread(PresentationScene):
    def construct(self):
        ax = Axes(
            x_range=[0, distance, 1],
            y_range=[0, PI * 2 / 3, 1],
            x_length=9,
            axis_config={
                "include_numbers": False,
                "include_ticks": False,
            },
        )
        x_label = ax.get_x_axis_label(
            r"t [s]", direction=1.25 * RIGHT + 0.05 * DOWN * 0.8
        )
        y_label = ax.get_y_axis_label(r"H [rad]", direction=1.5 * UP + 3 * LEFT)
        ax_labels = VGroup()
        ax_labels.add(x_label)
        ax_labels.add(y_label)
        self.play(DrawBorderThenFill(ax), Create(ax_labels))
        self.end_fragment()

        heading_graph = always_redraw(
            lambda: ax.plot(heading_function).set_color(colors["h"])
        )
        self.play(Create(heading_graph))
        self.end_fragment()

        start_line, end_line, start_dot, end_dot = dashed_lines_and_dots(ax)
        self.play(
            Create(start_line), Create(end_line), Create(start_dot), Create(end_dot)
        )

        start_text, end_text = percentage_texts(ax)
        self.play(Create(start_text), Create(end_text))
        self.end_fragment()

        self.play(percentage_tracker.animate.set_value(40))
        self.wait(0.5)
        self.play(percentage_tracker.animate.set_value(5))
        self.wait(0.5)
        self.play(percentage_tracker.animate.set_value(20))
        self.end_fragment()

        d_label = ax.get_x_axis_label(
            r"d [m]", direction=1.25 * RIGHT + 0.05 * DOWN * 0.8
        )
        self.play(Transform(x_label, d_label))
        self.end_fragment()
