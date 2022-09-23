from __future__ import annotations

from dataclasses import dataclass
from math import inf, sqrt

from utils.bezier import Bezier
from utils.utils import phase, wrap_angle


@dataclass
class Segment:
    max_vel: float
    bezier: Bezier

@dataclass
class TrajectoryPoint:
    time: float = 0
    pos: complex = 0
    distance: float = 0
    vel: float = 0
    acc: float = 0
    heading: float = 0
    omega: float = 0

    def clone(self) -> TrajectoryPoint:
        return TrajectoryPoint(
            time=self.time,
            pos=self.pos,
            distance=self.distance,
            vel=self.vel,
            acc=self.acc,
            heading=self.heading,
            omega=self.omega,
        )

DELTA_DISTANCE_FOR_EVALUATION = 1e-4

MAX_VEL = 3.83
MAX_ACC = 7.5
MAX_JERK = 50

def create_trajectory_list(segments: list[Segment]) -> list[TrajectoryPoint]:
    trajectory: list[TrajectoryPoint] = []
    first_point = TrajectoryPoint(pos=segments[0].bezier.evaluate(0), distance=0, vel=0, acc=0, time=0)
    trajectory.append(first_point)

    for segment in segments:
        segment_points: list[complex] = segment.bezier.distanced_points(DELTA_DISTANCE_FOR_EVALUATION)
        for pos in segment_points[1:]:
            prev_point = trajectory[-1]
            current_point = TrajectoryPoint()
            current_point.pos = pos
            current_point.distance = prev_point.distance + abs(pos - prev_point.pos)
            current_point.vel = segment.max_vel

            trajectory.append(current_point)
    return trajectory

def get_first_point(distance: float) -> TrajectoryPoint:
    # x(t) = (1/6)*j*t^3 -> t(x) = (6*x/j)^(1/3)
	firstPointTime = (6*distance/MAX_JERK) ** (1.0/3.0)

	return TrajectoryPoint(
		time=firstPointTime,
		vel=0.5 * MAX_JERK * (firstPointTime ** 2),
		acc=MAX_JERK * firstPointTime,
    )


def calculate_kinematics(trajectory: list[TrajectoryPoint], acc_forward: bool):
    trajectory[0].vel = 0
    trajectory[0].acc = 0

    first_point = get_first_point(trajectory[1].distance)
    trajectory[1].time = first_point.time
    trajectory[1].vel = first_point.vel
    trajectory[1].acc = first_point.acc

    for i in range(2, len(trajectory)):
        curr_point = trajectory[i]
        prev_point = trajectory[i-1]

        delta_dist = curr_point.distance - prev_point.distance
        delta_t = delta_dist / prev_point.vel # v=∆x/∆t -> ∆t=∆x/v

        curr_point.time = prev_point.time + delta_t

        # TODO: check acc increasing while velocity limited by segment's max vel
        curr_point.acc = min(prev_point.acc + delta_t * MAX_JERK, MAX_ACC)

        if acc_forward:
            max_acc_forward = MAX_ACC * (1 - prev_point.vel/MAX_VEL)
            curr_point.acc = min(curr_point.acc, max_acc_forward)
        
        kinematic_vel = prev_point.vel + prev_point.acc * delta_t
        if curr_point.vel < kinematic_vel:
            curr_point.acc = 0
        else: curr_point.vel = kinematic_vel
        # curr_point.vel = min(prev_point.vel + prev_point.acc * delta_t, curr_point.vel)

def calculate_dt(trajectory: list[TrajectoryPoint]):
    for i in range(2, len(trajectory)-1):
        curr_point = trajectory[i]
        prev_point = trajectory[i-1]
        
        dt = (curr_point.distance - prev_point.distance) / prev_point.vel

        curr_point.time = prev_point.time + dt
	

def centrifugal_force(trajectory: list[TrajectoryPoint]):
    for i in range(1, len(trajectory)-1):
        curr_point = trajectory[i]
        prev_point = trajectory[i-1]
        next_point = trajectory[i+1]

        prev_to_curr = curr_point.pos - prev_point.pos
        curr_to_next = next_point.pos - curr_point.pos

        dist_to_prev = curr_point.distance - prev_point.distance
        delta_angle = wrap_angle(phase(curr_to_next) - phase(prev_to_curr))

        drive_radius = abs(dist_to_prev / delta_angle if delta_angle != 0 else inf)
        max_vel_according_to_centrifugal_force = sqrt(drive_radius * MAX_ACC)
        curr_point.vel = min(curr_point.vel, max_vel_according_to_centrifugal_force)

    calculate_dt(trajectory)

def search_for_time(trajectory: list[TrajectoryPoint], time: float, last_search_index: int) -> int:
    for i, point in enumerate(trajectory[last_search_index:]):
        if point.time >= time: return i + last_search_index

    return -1

def reverse_trajectory(trajectory: list[TrajectoryPoint]) -> list[TrajectoryPoint]:
    total_distance = max(trajectory[0].distance, trajectory[-1].distance)
    total_time = max(trajectory[0].time, trajectory[-1].time)

    reversed_trajectory: list[TrajectoryPoint] = []
    for point in reversed(trajectory):
        reversed_point = point.clone()
        reversed_point.distance = total_distance - point.distance
        reversed_point.time = total_time - point.time

        reversed_trajectory.append(reversed_point)

    return reversed_trajectory
