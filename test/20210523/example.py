import manim

class MyScene(manim.scene.scene.Scene):
    def construct(self):
        vg=CircleWithPolygons(3,2)
        #vg=self.magic_circle(3,2)        
        self.wait()
        self.play(manim.animation.creation.Create(vg))
        #vg=self.magic_circle(4,4)        
        vg=CircleWithPolygons(4,3,is_variant=True)
        vg.scale(0.8)
        #self.wait()
        self.play(manim.animation.creation.Create(vg))
        self.wait()


class CircleWithPolygons(manim.mobject.types.vectorized_mobject.VGroup):
    def __init__(self,n,m,is_variant=False):
        delta = 2.0*manim.constants.PI/n/m
        all_obj = []

        default_color = '#CCCCCC' 
        colors = [default_color for i in range(m)] + [default_color]
        
        circle = manim.mobject.geometry.Circle(color=colors[-1])
        all_obj.append(circle)
        
        polygon0 = manim.mobject.geometry.RegularPolygon(n,0.5*manim.constants.PI)
        for i in range(m):
            if i == 0 and is_variant:
                line=manim.mobject.geometry.Line(manim.constants.LEFT,manim.constants.ORIGIN,color=colors[i])
                line.rotate_about_origin(-(-1.0/n+1.0)*manim.constants.PI)
                line.scale_about_point(0.1,manim.constants.ORIGIN)
                line.shift(manim.constants.UP)
                all_obj.append(line)
                
            polygon0.set_color(colors[i])
            all_obj.append(polygon0)
            polygon0=polygon0.copy()
            polygon0.rotate_about_origin(-delta)
            
            if i == 0 and is_variant:
                line=manim.mobject.geometry.Line(manim.constants.ORIGIN,manim.constants.RIGHT,color=colors[i])
                line.rotate_about_origin((-1.0/n+1.0)*manim.constants.PI)
                line.scale_about_point(0.1,manim.constants.ORIGIN)
                line.shift(manim.constants.UP)
                all_obj.append(line)
        super().__init__(*all_obj)

