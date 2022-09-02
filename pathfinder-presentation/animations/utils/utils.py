from typing import Tuple

from manim import *


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
