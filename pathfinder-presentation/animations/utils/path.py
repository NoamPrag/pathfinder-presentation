from __future__ import annotations

from manim import *

from utils.bezier import Bezier


class Path:
    def __init__(self, beziers: list[Bezier] = []) -> Path:
        self.beziers = beziers

    def add_bezier(self, bezier: Bezier): self.beziers.append(bezier)

    def translate(self, translation: complex) -> Path:
        return Path([bezier.translate(translation) for bezier in self.beziers])

    def scale(self, factor: float) -> Path:
        return Path([bezier.scale(factor) for bezier in self.beziers])
    
    def manim_vgroup(self) -> VGroup:
        vgroup = VGroup()
        for bezier in self.beziers: vgroup.add(bezier.manim_bezier())
        return vgroup
