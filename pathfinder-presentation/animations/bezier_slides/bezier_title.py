from manim import *
from manim_revealjs import PresentationScene

config.video_dir = "./videos"

class BezierTitle(PresentationScene):
    def construct(self):
        title = Text("Bèzier curves")
        title.shift(UP*3)
        self.play(Write(title))
        self.wait(1)

        curve_sign_image = ImageMobject("./images/curve-sign.jpg")
        curve_sign_image.shift(LEFT*4.5)
        self.play(FadeIn(curve_sign_image))
        self.wait(0.5)
 
        solidworks_bezier_image = ImageMobject("./images/solidworks-bezier.jpg")
        solidworks_bezier_image.scale(0.8)
        self.play(FadeIn(solidworks_bezier_image))
        self.wait(0.5)

        bezier_font_image = ImageMobject("./images/bezier-font.png")
        bezier_font_image.shift(RIGHT*4.5)
        self.play(FadeIn(bezier_font_image))
        self.end_fragment()

        
        self.play(FadeOut(curve_sign_image), FadeOut(solidworks_bezier_image), FadeOut(bezier_font_image))
        pierre_bezier_image = ImageMobject("./images/pierre-bezier.jpeg")
        pierre_bezier_image.shift(LEFT*4)
        pierre_bezier_image.scale(3)
        car_model_image = ImageMobject("./images/car-model-bezier.webp")
        car_model_image.scale(0.2)
        car_model_image.shift(RIGHT*4)
        self.play(FadeIn(pierre_bezier_image), FadeIn(car_model_image))
        self.end_fragment()
