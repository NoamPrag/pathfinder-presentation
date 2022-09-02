from manim import *
from manim_revealjs import PresentationScene

config.video_dir = "./videos"

class BezierSlide(PresentationScene):
    def construct(self):
        title = Text("Bèzier curves")
        title.shift(UP*3)
        self.play(Write(title))
        self.wait(1)

        curve_sign_image = ImageMobject("./images/curve-sign.jpg")
        curve_sign_image.shift(LEFT*5)
        self.add(curve_sign_image)
        self.wait(1)
 
        solidworks_bezier_image = ImageMobject("./images/solidworks-bezier.jpg")
        solidworks_bezier_image.scale(0.8)
        self.add(solidworks_bezier_image)
        self.wait(1)

        bezier_font_image = ImageMobject("./images/bezier-font.png")
        bezier_font_image.shift(RIGHT*5)
        self.add(bezier_font_image)
        self.end_fragment()
