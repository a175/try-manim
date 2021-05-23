import manim

class MyScene(manim.scene.scene.Scene):
    def construct(self):
        
        circle = manim.mobject.geometry.Circle()
        polygon1 = manim.mobject.geometry.RegularPolygon(4,0.5*manim.constants.PI)
        polygon2 = polygon1.copy()
        polygon2.rotate(0.25*manim.constants.PI)
        listofobj = [circle,polygon1,polygon2]
        vg = manim.mobject.types.vectorized_mobject.VGroup(*listofobj)
        self.wait()
        self.play(manim.animation.creation.Create(vg))
        #fadeinanimation=manim.animation.fading.FadeIn(vg)
        #self.play(fadeinanimation)
        self.wait()



    
