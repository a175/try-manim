import manim
manim._config.utils.ManimConfig.frame_width=40

#class MyScene(manim.scene.scene.Scene):
class MyScene(manim.scene.three_d_scene.ThreeDScene):
    def codestr2code(self,codestr):
        code=[(None,None)]
        cix=None
        stack=[]
        for (i,ci) in enumerate(codestr):
            if ci == '[':
                stack.append(len(code))
                code.append((ci,None))
            elif ci == ']':
                j=stack.pop()
                code[j]=('[',len(code)-1)
                code.append((ci,j-1))
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

    def get_mc(self,nn,i,ci,ni):
        if ci == "]":
            return None
        if ci == "[":
            mc = BraKet(self.get_mc_size(nn-i),self.get_mc_size(nn-ni))
            return mc
        if ci == "+":
            p=4
            v=False
        if ci == "-":
            p=4
            v=True
        if ci == ">":
            p=4
            v=False
        if ci == "<":
            p=4
            v=True
        if ci == ".":
            p=6
            v=False
        if ci == ",":
            p=6
            v=True
        mc = CircleWithPolygons(p,ni,is_variant=v)
        mc.scale(self.get_mc_size(nn-i))
        return mc
        
    def construct(self):
        codestr='+++++++++[>++++++++>+++++++++++>+++>+<<<<-]>.>++.+++++++..+++.>+++++.<<+++++++++++++++.>.+++.------.--------.>+.>+.'
        #codestr = '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++.+.+.>++++++++++.'
        #codestr = '>++++++.+++++++++.'
        
        #codestr = '++[-]'
        #code = [('+',4),('-',4)]
        code = self.codestr2code(codestr)
        print(codestr)
        print(code)
        nn=len(code)
        #self.move_camera(distance=5000000)


        print(nn,self.camera.get_distance())
        
        #self.camera.set_distance(nn*10)
        
        mcs = []
        mcs_vg=manim.mobject.types.vectorized_mobject.VGroup()
        for (i,(ci,ni)) in enumerate(code):
            if ci == "]":
                mcs.append(mcs[ni])
            else:
                mc=self.get_mc(nn,i,ci,ni)
                mcs.append(mc)
                mcs_vg.add(mc)

        #self.set_camera_orientation(phi=0.4 * manim.constants.PI, theta=-0.25 * manim.constants.PI)
        for i in range(nn):
            if code[nn-i-1][0] != '[':
                self.play(manim.animation.creation.Create(mcs[nn-i-1]))

        self.play(mcs_vg.animate.set_color("#AAAADD"))
        self.move_camera(phi=0.3 * manim.constants.PI,theta=-0.52*manim.constants.PI)        
        prev_out_anim=mcs_vg.animate.set_color("#777788")
        bf_tape=[0 for i in range(20)]
        bf_pointer=0

        pointer = manim.mobject.geometry.Line([0,0,0],8.5*manim.constants.OUT)
        pointer.set_color("#6666AA")
        self.play(manim.animation.creation.Create(pointer))
        tape = manim.mobject.types.vectorized_mobject.VGroup()
        tt=[]
        for i,ti in enumerate(bf_tape):
            tape_text = manim.mobject.svg.text_mobject.Text("0")
            tape_text.scale(0.5)
            tape_text.rotate(-0.5*manim.constants.PI,axis=manim.constants.LEFT,about_point=manim.constants.ORIGIN)
            tape_text.shift(8*manim.constants.OUT)
            tape_text.shift(i*manim.constants.RIGHT)
            tape.add(tape_text)
            tt.append(tape_text)
        self.play(manim.animation.creation.Write(tape))
        output_int=[]
        output_str=""
        output = None
        #self.add(output)
        #return
        
        i=0
        while i < len(mcs):
            mc_0=mcs[i].copy()
            current_in_anim=mc_0.animate.set_color_to_hilight("#EEEEFF",code[i][0])
            ag = manim.animation.composition.AnimationGroup(
                current_in_anim,
                prev_out_anim
            )
            self.play(ag)
            self.play(mc_0.animate.shift(0.4*manim.constants.OUT))

            tape_anim=None
            if code[i][0] == '+':
                bf_tape[bf_pointer]=bf_tape[bf_pointer]+code[i][1]
                old_tape_text=tt[bf_pointer]
                tape_text = manim.mobject.svg.text_mobject.Text("%d" % bf_tape[bf_pointer])
                #tt[bf_pointer]=tape_text                
                tape_text.scale(0.5)
                tape_text.rotate(-0.5*manim.constants.PI,axis=manim.constants.LEFT,about_point=manim.constants.ORIGIN)
                tape_text.align_to(old_tape_text,direction=[1,1,1])
                tape_anim = manim.animation.transform.Transform(old_tape_text,tape_text)



            elif code[i][0] == '-':
                bf_tape[bf_pointer]=bf_tape[bf_pointer]-code[i][1]
                tape_text = manim.mobject.svg.text_mobject.Text("%d" % bf_tape[bf_pointer])
                tape_text.scale(0.5)
                tape_text.rotate(-0.5*manim.constants.PI,axis=manim.constants.LEFT,about_point=manim.constants.ORIGIN)
                tape_text.align_to(tt[bf_pointer],direction=[1,1,1])
                tape_anim = manim.animation.transform.Transform(tt[bf_pointer],tape_text)
                tt[bf_pointer]=tape_text

            elif code[i][0] == '>':
                bf_pointer=bf_pointer+code[i][1]
                tape_anim = tape.animate.shift(code[i][1]*manim.constants.LEFT)
                if bf_pointer >= len(bf_tape):
                    for q in range(bf_pointer-len(bf_tape)+1):
                        bf_tape.append(0)
                
            elif code[i][0] == '<':
                tape_anim = tape.animate.shift(code[i][1]*manim.constants.RIGHT)
                bf_pointer=bf_pointer-code[i][1]

            elif code[i][0] == '.':
                ta = []
                ss=""
                for j in range(code[i][1]):
                    output_int.append(bf_tape[bf_pointer])
                    s=chr(bf_tape[bf_pointer])
                    ss=ss+s
                output_str=output_str+ss
                print("BF:",output_int,output_str,ss)
                if ss.isprintable() and not ss.isspace():
                    output_text = manim.mobject.svg.text_mobject.Text(ss)
                    print("MCBFTAPE:",ss,bf_tape[bf_pointer])
                    #output_text.rotate(-0.5*manim.constants.PI,axis=manim.constants.LEFT,about_point=manim.constants.ORIGIN)
                    if output == None:
                        output_text.shift(9*manim.constants.OUT)
                    else:
                        output_text.next_to(output)

                    tape_anim=manim.animation.creation.Write(output_text)
                    output=output_text

            elif code[i][0] == ',':
                pass
            elif code[i][0] == '[':
                if bf_tape[bf_pointer] == 0:
                    i=code[i][1]
                    tape_anim=(True,True)
                else:
                    tape_anim=(True,False)
            elif code[i][0] == ']':
                if bf_tape[bf_pointer] != 0:
                    i=code[i][1]
                    tape_anim=(False,True)
                else:
                    tape_anim=(False,False)

            print(i,bf_pointer,bf_tape[:10])
                

            aa = mc_0.play_animation_for_run(self,tape_anim)

            self.play(mc_0.animate.shift(-0.4*manim.constants.OUT))
            prev_out_anim=manim.animation.fading.FadeOut(mc_0)
            
            i=i+1

        self.play(prev_out_anim)
        self.play(mcs_vg.animate.set_color("#555555"))
        
        self.wait()


class BraKet(manim.mobject.types.vectorized_mobject.VGroup):
    def __init__(self,bra,ket,default_color= '#555555',is_variant=False):
        self.bra = manim.mobject.geometry.Line(bra*manim.constants.UP+bra*manim.constants.LEFT,bra*manim.constants.UP+bra*manim.constants.RIGHT)
        self.ket = manim.mobject.geometry.Line(ket*manim.constants.UP+bra*manim.constants.LEFT,ket*manim.constants.UP+bra*manim.constants.RIGHT)
        side_1=manim.mobject.geometry.Line(bra*manim.constants.UP+bra*manim.constants.LEFT,ket*manim.constants.UP+bra*manim.constants.LEFT)
        side_2=manim.mobject.geometry.Line(bra*manim.constants.UP+bra*manim.constants.RIGHT,ket*manim.constants.UP+bra*manim.constants.RIGHT)
        super().__init__(self.bra,self.ket,side_1,side_2)
        self.set_color(default_color)
        
    def set_color_to_hilight(self,color,code):
        if code == "[":
            self.hilighted_line = self.bra
        else:
            self.hilighted_line = self.ket
        self.hilighted_line.set_color(color)

    def play_animation_for_run(self,scene,tape_anim):
        (is_bra, should_rotate) = tape_anim
        #p0.set_color("#8888FF")
        if is_bra:
            self.hilighted_line = self.bra
        else:
            self.hilighted_line = self.ket
        center=0.5*(self.bra.get_center()+self.ket.get_center())
        if should_rotate:
            if is_bra:
                scene.play(self.hilighted_line.animate.rotate(manim.constants.PI,axis=manim.constants.LEFT,about_point=center))
            else:
                scene.play(self.hilighted_line.animate.rotate(manim.constants.PI,axis=manim.constants.LEFT,about_point=center))
                        
        #scene.remove(self.hilighted_line)


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
        if is_variant:
            self.angle=delta*(m-1)
        else:
            self.angle=-delta*(m-1)
        super().__init__(*all_obj)


        
    def get_one_polygon(self):
        return self.onepolygon.copy()
    
    def set_circle_color(self,color):
        self.submobjects[0].set_color(color)

    def set_color_to_hilight(self,color,code):
        self.set_color(color)

    def play_animation_for_run(self,scene,tape_anim):
        ans=[]
        p0 = self.get_one_polygon()            
        p0.set_color("#8888FF")
        scene.play(p0.animate.shift(0.2*manim.constants.OUT))
        if tape_anim == None:
            scene.play(manim.animation.rotation.Rotate(p0,self.angle,about_point=manim.constants.ORIGIN))
        else:
            ag = manim.animation.composition.AnimationGroup(
                manim.animation.rotation.Rotate(p0,self.angle,about_point=manim.constants.ORIGIN),tape_anim)
            scene.play(ag)
        scene.play(p0.animate.shift(-0.2*manim.constants.OUT))
        scene.remove(p0)

