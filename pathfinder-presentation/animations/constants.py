from manim import *

from algorithm.pathfinder import *
from utils.bezier import Bezier

MAX_JERK = 50
MAX_ACC = 7.5
MAX_VEL = 3.83

example_path: list[Segment] = [
    Segment(bezier=Bezier([-1, 1j, 0, 0.75]), max_vel=1.5),
    Segment(bezier=Bezier([0.75, 1.5, 9+2j, 1.5+2j]), max_vel=3.5),
    Segment(bezier=Bezier([1.5+2j, -1.5+2j, -1.5+3j, -1.5+1.5j]), max_vel=2),
]
path_length = sum([seg.bezier.length() for seg in example_path])

segments_lengths: list[float] = [seg.bezier.length() for seg in example_path]

segments_colors = colors = [GREEN, RED, BLUE]

colors = {
    "x": TEAL,
    "v": RED,
    "a": BLUE,
    "j": PURPLE,
    "t": YELLOW,
}
