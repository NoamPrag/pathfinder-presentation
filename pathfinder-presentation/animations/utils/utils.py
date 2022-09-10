from typing import Tuple

from manim import *


def dot_from_complex(z: complex) -> Dot:
    return Dot(complex_to_array(z))

def line_from_complex(start: complex, end: complex) -> Line:
    return Line(start=complex_to_tuple(start), end=complex_to_tuple(end))

def create_all(objects: list[Mobject]) -> list[Create]:
    return [Create(obj) for obj in objects]

def write_all(texts) -> list[Write]:
    return [Write(text) for text in texts]

def dot_with_title(dot: Dot, title) -> tuple[Animation]:
    return Create(dot), Write(title)

def complex_to_array(z: complex):
    return [z.real, z.imag, 0]

def complex_to_tuple(z: complex) -> Tuple[float, float, float]:
    return (z.real, z.imag, 0)

def dot_from_complex(z: complex) -> Dot:
    return Dot(complex_to_array(z))

def lerp(x: complex, y: complex, t: float) -> complex:
    return (1-t)*x+t*y

def quadratic_lerp(x: complex, y: complex, z: complex, t: float) -> complex:
    return lerp(lerp(x,y,t), lerp(y,z,t), t)

def connect_the_dots(points: list[complex]) -> list[Line]:
    return [line_from_complex(start, end) for start, end in zip(points, points[1:])]
