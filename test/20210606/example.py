import manim

#class MyScene(manim.scene.scene.Scene):
class MyScene(manim.scene.three_d_scene.ThreeDScene):
    def codestr2code(self,codestr):
        code=[(None,None)]
        cix=None
        stack=[]
        for (i,ci) in enumerate(codestr):
            if ci == '[':
                stack.append(ci)
                code.append((ci,None))
            elif ci == ']':
                j=stack.pop()
                code[j]=('[',i)
                code.append((ci,j))
            else:
                if code[-1][0] == ci:
                    cjn=code[-1][1]
                    if cjn <10:
                        code[-1]=(ci,cjn+1)
                    else:
                        code.append((ci,1))
                else:
                    code.append((ci,1))
        code=code[1:]
        return code

    def get_mc_size(self,i):
        return 1+0.3*i

    def get_mc(self,i,ci,ni):
        if ci == "]":
            return None
        if ci == "[":
            return None
        if ci == "+":
            p=4
            v=False
        if ci == "-":
            p=4
            v=True
        if ci == ">":
            p=4
            v=False
            v=True
        if ci == "<":
            p=4
            v=True
        if ci == ".":
            p=6
            v=False
            v=True
        if ci == ",":
            p=6
            v=True
        mc = CircleWithPolygons(p,ni,is_variant=v)
        mc.scale(self.get_mc_size(i))
        return mc
        
    def construct(self):
        codestr = '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++.+.+.>++++++++++.'
        #codestr = '+.>++++++++++.'
        #code = [('+',4),('-',4)]
        code = self.codestr2code(codestr)
        print(code)        
        mcs = []
        
        #self.set_camera_orientation(phi=0.4 * manim.constants.PI, theta=-0.25 * manim.constants.PI)
        for (i,(ci,ni)) in enumerate(reversed(code)):
            print((i,(ci,ni)))
            mc=self.get_mc(i,ci,ni)
            mcs.append(mc)
            print(mc)
            mca=manim.animation.creation.Create(mc)
            self.play(mca)
        self.wait()
        
        mcs.reverse()
        mcs_vg=manim.mobject.types.vectorized_mobject.VGroup(*mcs)
        self.play(mcs_vg.animate.set_color("#AAAADD"))
        self.move_camera(phi=0.3 * manim.constants.PI)        
        prev_out_anim=mcs_vg.animate.set_color("#777788")
        bf_tape=[0 for i in range(30000)]
        bf_pointer=0
        output_int=[]
        output_str=""
        i=0
        while i < len(mcs):
            if code[i][0] == '+':
                bf_tape[bf_pointer]=bf_tape[bf_pointer]+code[i][1]

            elif code[i][0] == '-':
                bf_tape[bf_pointer]=bf_tape[bf_pointer]-code[i][1]

            elif code[i][0] == '>':
                bf_pointer=bf_pointer+code[i][1]
                if bf_pointer >= len(bf_tape):
                    for q in range(bf_pointer-len(bf_tape)+1):
                        bf_tape.append(0)
            elif code[i][0] == '<':
                bf_pointer=bf_pointer-code[i][1]

            elif code[i][0] == '.':
                output_int.append(bf_tape[bf_pointer])
                output_str=output_str+chr(bf_tape[bf_pointer])
                print("BF:",output_int,output_str)

            elif code[i][0] == ',':
                pass
            elif code[i][0] == '[':
                if bf_tape[bf_pointer] == 0:
                    i=code[i][1]
                continue
            elif code[i][0] == ']':
                if bf_tape[bf_pointer] != 0:
                    i=code[i][1]
                continue

            print(i,bf_pointer,bf_tape[:10])
                
            mc_0=mcs[i].copy()
            #current_in_anim=mc_0.animate.set_circle_color("#EEEEFF")
            current_in_anim=mc_0.animate.set_color("#EEEEFF")
            #current_in_anim2=mc_0.animate.shift(0.4*manim.constants.OUT)
            ag = manim.animation.composition.AnimationGroup(
                current_in_anim,
                #current_in_anim2,
                prev_out_anim
            )
            self.play(ag)
            self.play(mc_0.animate.shift(0.4*manim.constants.OUT))

            p0 = mc_0.get_one_polygon()            
            p0.set_color("#8888FF")
            self.play(p0.animate.shift(0.2*manim.constants.OUT))
            self.play(manim.animation.rotation.Rotate(p0,mc_0.angle,about_point=manim.constants.ORIGIN))
            self.play(p0.animate.shift(-0.2*manim.constants.OUT))
            self.remove(p0)

            self.play(mc_0.animate.shift(-0.4*manim.constants.OUT))
            prev_out_anim=manim.animation.fading.FadeOut(mc_0)
            
            i=i+1

        self.play(prev_out_anim)
        self.play(mcs_vg.animate.set_color("#555555"))
        
        self.wait()




class CircleWithPolygons(manim.mobject.types.vectorized_mobject.VGroup):
    def __init__(self,n,m,default_color= '#555555',is_variant=False):
        self.n=n
        self.m=m
        delta = 2.0*manim.constants.PI/n/m
        if is_variant:
            delta = -delta
            
        all_obj = []

        colors = [default_color for i in range(m)] + [default_color]
        
        circle = manim.mobject.geometry.Circle(color=colors[-1])
        all_obj.append(circle)
        
        polygon0 = manim.mobject.geometry.RegularPolygon(n,start_angle=0.5*manim.constants.PI)
        self.onepolygon=polygon0
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
        self.angle=-delta*(m-1)
        super().__init__(*all_obj)


        
    def get_one_polygon(self):
        return self.onepolygon.copy()
    
    def set_circle_color(self,color):
        self.submobjects[0].set_color(color)
