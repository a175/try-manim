import manim

class MyScene(manim.scene.scene.Scene):
    def construct(self):

        vg=self.magic_circle(3,2)        
        self.wait()
        self.play(manim.animation.creation.Create(vg))
        vg=self.magic_circle(4,4)        
        vg.scale(1.5)
        self.wait()
        self.play(manim.animation.creation.Create(vg))
        self.wait()


    def magic_circle(self,n,m):
        delta = -2.0*manim.constants.PI/n/m
        all_obj = []
        
        circle = manim.mobject.geometry.Circle()
        all_obj.append(circle)
        
        polygon0 = manim.mobject.geometry.RegularPolygon(n,0.5*manim.constants.PI)
        for i in range(m):
            all_obj.append(polygon0)
            polygon0=polygon0.copy()
            polygon0.rotate_about_origin(delta)
        mc = manim.mobject.types.vectorized_mobject.VGroup(*all_obj)
        return mc
