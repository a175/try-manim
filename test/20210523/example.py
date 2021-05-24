import manim

class MyScene(manim.scene.scene.Scene):
    def construct(self):
        poly = {'+':4,'-':4,'>':3,'<':3,'.':6,',':6}
        variant = {'+':False,'-':True,'>':False,'<':True,'.':False,',':True}
        codestr = '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++.+.+.>++++++++++.'
        #code = [('+',4),('-',4)]
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
        print(code)
#        code = [('+',10) for i in range(6)]
#        code = [('+',15) for i in range(4)]
#        code = code+[('+',5),('.',1),('+',1),('.',1),('.',1),('+',1),('.',1)]
        mcs = []

        for (i,(ci,ni)) in enumerate(reversed(code)):
            mc = CircleWithPolygons(poly[ci],ni,is_variant=variant[ci])
            mc.scale(1+0.3*i)
            mcs.append(mc)
            self.play(manim.animation.creation.Create(mc))
        self.wait()
        mcs.reverse()
        mcs_vg=manim.mobject.types.vectorized_mobject.VGroup(*mcs)
        mcs_vg_old=mcs_vg
        mcs_vg_new=mcs_vg_old.copy()
        mcs_vg_new.set_color("#AAAADD")
        self.play(manim.animation.transform.Transform(mcs_vg_old,mcs_vg_new))
        self.wait()

        
        mcs_vg_old=mcs_vg_new
        mcs_vg_new=mcs_vg_old.copy()
        mcs_vg_new.set_color("#777788")
        mcs_vg_new.set_z_index(-1)
        prev_out_anim=manim.animation.transform.Transform(mcs_vg_old,mcs_vg_new)
        i=0
        bf_tape=[0 for i in range(30000)]
        bf_pointer=0
        output_int=[]
        output_str=""
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
            elif code[i][0] == ']':
                if bf_tape[bf_pointer] != 0:
                    i=code[i][1]

            print(i,bf_pointer,bf_tape[:10])
                
            mc_0=mcs[i].copy()
            mc_0.set_circle_color("#AAAAFF")
            mc_0.set_circle_color("#EEEEFF")
            mc_0.set_z_index(2)
            ag = manim.animation.composition.AnimationGroup(
                manim.animation.fading.FadeIn(mc_0),
                prev_out_anim
            )
            self.play(ag)

            p0 = mc_0.get_one_polygon()            
            p0.set_z_index(1)
            p0.set_color("#8888FF")
            self.play(manim.animation.rotation.Rotate(p0,mc_0.angle,about_point=manim.constants.ORIGIN))
            self.remove(p0)
            prev_out_anim=manim.animation.fading.FadeOut(mc_0)
            
            i=i+1

        self.play(prev_out_anim)
        mcs_vg.set_color("#555555")
        self.play(manim.animation.transform.Transform(mcs_vg_new,mcs_vg))
        
        self.wait()

        # for mc in mcs0:
        #     mc = mc.copy()
        #     #mc.set_color("#BBBBEE")
        #     mc.set_color("#AAAADD")
        #     mcs1.append(mc)
        # mcs1_vg=manim.mobject.types.vectorized_mobject.VGroup(*mcs1)
        # self.play(manim.animation.transform.Transform(mcs0_vg,mcs1_vg))
        # self.wait()
        # mcs2=[]
        # for mc in mcs0:
        #     mc = mc.copy()
        #     #mc.set_color("#BBBBEE")
        #     mc.set_color("#777788")
        #     mcs2.append(mc)
        # mcs2_vg=manim.mobject.types.vectorized_mobject.VGroup(*mcs2)
        # self.play(manim.animation.transform.Transform(mcs1_vg,mcs2_vg))



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
        
        polygon0 = manim.mobject.geometry.RegularPolygon(n,0.5*manim.constants.PI)
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
