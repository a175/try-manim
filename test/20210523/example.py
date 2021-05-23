import manim

class MyScene(manim.scene.scene.Scene):
    def construct(self):
        circle = manim.mobject.geometry.Circle()
        polygon1 = manim.mobject.geometry.RegularPolygon(4,0.5*manim.constants.PI)
        polygon2 = polygon1.copy()
        polygon2.rotate(0.25*manim.constants.PI)
        vg = manim.mobject.types.vectorized_mobject.VGroup(circle,polygon1,polygon2)
        self.wait()
        fadeinanimation=manim.animation.fading.FadeIn(vg)
        self.play(fadeinanimation)
        self.wait()
        #self.play(manim.animation.creation.Create(polygon))
        self.wait()



