import manim

class MyScene(manim.scene.scene.Scene):
    def construct(self):
        circle = manim.mobject.geometry.Circle()
        self.add(circle)
        self.wait()
