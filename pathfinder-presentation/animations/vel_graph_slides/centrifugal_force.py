from algorithm.animations import get_vel_time_graph
from algorithm.path import Path
from constants import *
from manim import *
from manim_revealjs import PresentationScene
from utils.utils import dot_from_complex

config.video_dir = "./videos"

trajectory: list[TrajectoryPoint] = create_trajectory_list(example_path)
trajectory = do_kinematics(trajectory)
calculate_curvature(trajectory)
# centrifugal_force(trajectory)
# trajectory = do_kinematics(trajectory)

def get_max_vel(point: TrajectoryPoint) -> tuple[float, float]:
    max_vel: float = sqrt(MAX_ACC * point.drive_radius)
    return (point.time, max_vel)
    
class CentrifugalForce(PresentationScene):
    def angular_acc_eq(self) -> MathTex:
        eq = MathTex(r"a_r = \frac{v^2}{r}")
        eq[0][:2].set_color(colors["a"])
        eq[0][-4].set_color(colors["v"])
        eq[0][-1].set_color(colors["x"])
        return eq

    def v_squared_eq(self) -> MathTex:
        eq = MathTex(r"v^2 = a_r r")
        eq[0][0].set_color(colors["v"])
        eq[0][-3:-1].set_color(colors["a"])
        eq[0][-1].set_color(colors["x"])
        return eq

    def v_eq(self) -> MathTex:
        eq = MathTex(r"v = \sqrt{a_r r}")
        eq[0][0].set_color(colors["v"])
        eq[0][-3:-1].set_color(colors["a"])
        eq[0][-1].set_color(colors["x"])
        return eq

    def max_vel_eq(self) -> MathTex:
        eq = MathTex(r"v = \sqrt{a_{max} r}")
        eq[0][0].set_color(colors["v"])
        eq[0][-5:-1].set_color(colors["a"])
        eq[0][-1].set_color(colors["x"])
        return eq

    def derive_vel_equation(self) -> MathTex:
        angular_acc_eq = self.angular_acc_eq()
        angular_acc_eq.shift(UP*3)
        self.play(Write(angular_acc_eq))
        self.end_fragment()

        v_squared_eq = self.v_squared_eq()
        v_squared_eq.shift(UP*3)
        self.play(TransformMatchingShapes(angular_acc_eq, v_squared_eq))
        self.wait(0.5)

        v_eq = self.v_eq()
        v_eq.shift(UP*3)
        self.play(TransformMatchingShapes(v_squared_eq, v_eq))
        self.end_fragment()

        max_vel_eq = self.max_vel_eq()
        max_vel_eq.shift(UP*3)
        self.play(TransformMatchingShapes(v_eq, max_vel_eq))
        self.end_fragment()
        return max_vel_eq

    def get_tangent_circle(self, dist_tracker: ValueTracker, path: Path, path_derivative: Path) -> Circle:
       def get_circle() -> Circle:
           dist: float = dist_tracker.get_value()
           s = path.t_for_distance(dist)
           start: complex = path.evaluate(s)
           derivative: complex = path_derivative.evaluate(s)
           curvature: float = path.curvature(s)
           radius: float = 1 / curvature if curvature != 0 else inf
           end: complex = start + (derivative / abs(derivative) * -1j * radius)
           return Circle(arc_center=complex_to_R3(end), radius=radius).set_color(RED)

       return always_redraw(get_circle)
 
    def get_max_vel_graph(self, ax: Axes, dist_tracker: ValueTracker, path: Path) -> VGroup:
       trajectory_length = trajectory[-1].distance
       scaled_path_length = path.length()
       time_interval = 0.01
       def get_graph_dots() -> VGroup:
           dist: float = trajectory_length * dist_tracker.get_value() / scaled_path_length
           graph = VGroup()
           prev_point_time = 0
           for i in range(0, len(trajectory)):
               point = trajectory[i]
               if point.distance >= dist: break # plotting until dist_tracker's distance

               # limiting points byb time interval (graph's x-axis)
               if point.time - prev_point_time < time_interval: continue
               prev_point_time = point.time

               (time, max_vel) = get_max_vel(point)
               if max_vel > 20: continue
               graph_dot = Dot(ax.coords_to_point(time, max_vel), radius=0.03)
               graph.add(graph_dot)
           return graph

       return always_redraw(get_graph_dots)
        
 
    def construct(self):
       global trajectory
       max_vel_eq = self.derive_vel_equation()
       max_vel_eq.generate_target()
       max_vel_eq.target.shift(LEFT*4)

       path: Path = Path([seg.bezier for seg in example_path])
       path = path.scale(0.7)
       path = path.translate(-4.3-1.5j)
       path_derivative: Path = path.derivative()
       bezier_fs: list[ParametricFunction] = [b.parametric_function() for b in path.beziers]
       bezier_group = VGroup()
       for bezier in bezier_fs: bezier_group.add(bezier)
       self.play(MoveToTarget(max_vel_eq))
       self.play(Create(bezier_group), run_time=2)

       dist_tracker = ValueTracker(0.5)
       dot = always_redraw(lambda: dot_from_complex(path.evaluate_by_distance(dist_tracker.get_value())).set_color(BLUE))
       self.play(Create(dot))

       circle = self.get_tangent_circle(dist_tracker, path, path_derivative)
       self.play(Create(circle))
       self.end_fragment() # moving the equation to the left and creating path with tangent circle

       ax = Axes(
           x_range = [0, 7.5, 1],
           y_range = [0, 4.5, 0.5],
           x_length=9,
           axis_config={"include_numbers": True},
       )
       ax.shift(RIGHT*3+0.75*DOWN)
       ax.scale(0.65)
       x_label = ax.get_x_axis_label(r"t [s]", direction=3*DOWN)
       y_label = ax.get_y_axis_label(r"v [\frac{m}{s}]", direction=1.5*UP+3*LEFT)
       ax_labels = VGroup()
       ax_labels.add(x_label)
       ax_labels.add(y_label)
       self.play(DrawBorderThenFill(ax), Create(ax_labels))

       vel_graph_no_centrifugal = get_vel_time_graph(trajectory, ax, dt=0.01)
       self.play(ShowIncreasingSubsets(vel_graph_no_centrifugal, run_time=2), run_time=2)
       self.end_fragment() # drawing path and non-limited vel graph

       self.play(dist_tracker.animate.set_value(0), run_time=2)
       self.wait(0.25)

       max_vel_graph = self.get_max_vel_graph(ax, dist_tracker, path)
       self.add(max_vel_graph)
       self.play(dist_tracker.animate.set_value(path.length()), run_time=8)

       centrifugal_force(trajectory) # applying vel limit
    
       limited_vel_graph = get_vel_time_graph(trajectory, ax, dt=0.01)
       self.add(limited_vel_graph) # adding limited vel graph on top of current
       self.end_fragment() # creating max vel graph

       self.remove(max_vel_graph)
       self.play(FadeOut(vel_graph_no_centrifugal))
       self.end_fragment() # removing old velocity graphs

       trajectory = do_kinematics(trajectory)
       final_vel_graph = get_vel_time_graph(trajectory, ax, dt=0.01)
       self.play(TransformMatchingShapes(limited_vel_graph, final_vel_graph))
       self.end_fragment() # drawing final graph after applying kinematics
