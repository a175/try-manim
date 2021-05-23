import manim

class MyScene(manim.scene.scene.Scene):
    def construct(self):
        circle = manim.mobject.geometry.Circle()
        polygon = manim.mobject.geometry.RegularPolygon(4,0.5*manim.constants.PI)
        self.wait()
        fadeinanimation=manim.animation.fading.FadeIn(circle)
        self.play(fadeinanimation)
        self.wait()
        self.add(polygon)
        self.wait()
        polygon=polygon.copy()
        polygon.rotate(0.25*manim.constants.PI)
        self.play(manim.animation.creation.Create(polygon))
        self.wait()



