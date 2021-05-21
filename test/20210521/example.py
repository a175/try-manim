import manim

class SquareToCircle(manim.scene.scene.Scene):
    def construct(self):
        circle = manim.mobject.geometry.Circle()
        square = manim.mobject.geometry.Square()
        square.flip(manim.constants.RIGHT)
        square.rotate(-3 * manim.constants.TAU / 8)
        circle.set_fill(manim.utils.color.PINK, opacity=0.5)

        self.play(manim.animation.creation.Create(square))
        self.play(manim.animation.transform.Transform(square, circle))
        self.play(manim.animation.fading.FadeOut(square))
