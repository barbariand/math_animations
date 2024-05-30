from manim import *
import math
# https://github.com/CaftBotti/manim_pi_creatures/tree/main/PiCreature
class MathScene(Scene):
    def construct(self):
        name=Text("Vinkel Problemet - Dante Nilsson").shift(UP*3)
        self.play(Create(name))
        img=ImageMobject("image.png").shift(DOWN)
        self.add(img)
        self.wait(20)
        # Create the number plane 
        
        plane = NumberPlane(x_range=[-10, 10, 1], y_range=[-10, 10, 1])
        plane.set_background_color("#385723")

        # Value tracker for distance
        distance = ValueTracker(2)

        # The dots
        point_a = Dot([0, 1.0, 0], color=GREEN)
        point_b = Dot([0, 2.5, 0], color=BLUE)
        point_c = Dot([distance.get_value(), 0, 0], color=RED)

        # Updater for point_c position
        point_c.add_updater(lambda m: m.move_to([distance.get_value(), 0, 0]))

        # Connecting lines
        line_ac = always_redraw(lambda: Line(point_a.get_center(), point_c.get_center()))
        line_cb = always_redraw(lambda: Line(point_b.get_center(), point_c.get_center()))
        line_co = always_redraw(lambda: Line(point_c.get_center(), ORIGIN))

        # Angle between lines
        angle_acb = always_redraw(lambda: Angle(line_cb, line_ac, radius=1.0, quadrant=(-1, -1)))

        # Add objects to the scene
        self.play(FadeIn(plane),FadeOut(img),FadeOut(name))
        self.wait(3)
        self.play(Write(point_a), Write(point_b), Write(point_c), lag_ratio=1.0)
        self.play(Create(line_ac), Create(line_cb))
        self.play(Create(angle_acb))

        # Animate the dot movement
        self.play(distance.animate.set_value(0.1))
        self.play(distance.animate.set_value(5), run_time=3)
        self.play(distance.animate.set_value(2), run_time=2)

        tri_blue = Polygon(point_b.get_center(), ORIGIN, point_c.get_center(), fill_opacity=1.0, fill_color=BLUE)
        tri_green = Polygon(point_a.get_center(), point_c.get_center(), ORIGIN, fill_opacity=1.0, fill_color=GREEN)
        tri_red = Polygon(point_a.get_center(), point_b.get_center(), point_c.get_center(), fill_opacity=1.0, fill_color=RED)

        # Create angle annotations
        angle_red = Angle(line_cb, line_ac, radius=1, quadrant=(-1, -1), color=WHITE)
        angle_green = Angle(line_ac, line_co, radius=1, quadrant=(-1, 1))
        angle_blue = Angle(line_cb, line_co, radius=1, quadrant=(-1, 1))

        self.remove(angle_acb)
        self.add(angle_red)
        self.play(Create(angle_green))
        angle_red.set_z_index(1)
        angle_green.set_z_index(1)
        self.play(Create(tri_blue), run_time=3)
        self.play(Create(tri_green), Create(tri_red), run_time=3)

        self.play(Unwrite(point_a), Unwrite(point_b), Unwrite(point_c), Unwrite(line_ac), Unwrite(line_cb))
        self.add(angle_blue)
        self.wait()

        # Move triangles and angles to final positions
        self.play(
            AnimationGroup(
                tri_blue.animate.shift(LEFT*1),
                angle_blue.animate.shift(LEFT*1)
            ),
            AnimationGroup(
                tri_red.animate.shift(LEFT*6),
                angle_red.animate.shift(LEFT*6)
            ),
            AnimationGroup(
                tri_green.animate.shift(RIGHT*4),
                angle_green.animate.shift(RIGHT*4)
            )
        )

        minus = MathTex("-").scale(3).shift(UP*0.5 + RIGHT*2.5)
        equals = MathTex("=").scale(3).shift(UP*0.5 + LEFT*2.5)
        self.play(FadeOut(plane))
        self.play(
            AnimationGroup(
                FadeIn(minus),
                FadeIn(equals),
                run_time=4
            )
        )
        self.wait()
        
        # Clone polygons and add updaters to stretch them along the x-axis
        tri_red_clone = tri_red.copy().add_updater(
            lambda m: m.become(Polygon(
                UP + LEFT*6, 
                UP*2.5 + LEFT*6, 
                point_c.get_center() + LEFT*6, 
                fill_opacity=1.0, 
                fill_color=RED
            ))
        )
        tri_blue_clone = tri_blue.copy().add_updater(
            lambda m: m.become(Polygon(
                UP*2.5 + LEFT*1, 
                ORIGIN + LEFT*1, 
                point_c.get_center() + LEFT*1, 
                fill_opacity=1.0, 
                fill_color=BLUE
            ))
        )
        tri_green_clone = tri_green.copy().add_updater(
            lambda m: m.become(Polygon(
                UP + RIGHT*4, 
                ORIGIN + RIGHT*4,
                point_c.get_center() + RIGHT*4, 
                fill_opacity=1.0, 
                fill_color=GREEN
            ))
        )

        # Connecting lines
        line_ac_red = Line(point_a.get_center() + LEFT*6, point_c.get_center() + LEFT*6).add_updater(lambda l: l.become(Line(point_a.get_center() + LEFT*6, point_c.get_center() + LEFT*6)))
        line_cb_red = Line(point_b.get_center() + LEFT*6, point_c.get_center() + LEFT*6).add_updater(lambda l: l.become(Line(point_b.get_center() + LEFT*6, point_c.get_center() + LEFT*6)))
        line_co_red = Line(point_c.get_center() + LEFT*6, ORIGIN + LEFT*6).add_updater(lambda l: l.become(Line(point_c.update().get_center() + LEFT*6, ORIGIN + LEFT*6)))

        angle_red_clone = always_redraw(
            lambda: Angle(
                line_cb_red.update(), line_ac_red.update(), radius=1, quadrant=(-1, -1), color=WHITE
            )
        )

        # Connecting lines
        line_cb_blue = Line(point_b.get_center() + LEFT*1, point_c.get_center() + LEFT*1).add_updater(lambda l: l.become(Line(point_b.get_center() + LEFT*1, point_c.get_center() + LEFT*1)))
        line_co_blue = Line(point_c.get_center() + LEFT*1, ORIGIN + LEFT*1).add_updater(lambda l: l.become(
            Line(point_c.update().get_center() + LEFT*1, ORIGIN + LEFT*1)))

        angle_blue_clone = always_redraw(
            lambda: Angle(
                line_cb_blue.update(), line_co_blue.update(), radius=1, quadrant=(-1, 1)
            )
        )

        # Connecting lines
        line_ac_green = Line(point_a.get_center() + RIGHT*4, point_c.get_center() + RIGHT*4).add_updater(
            lambda l: l.become(
                Line(point_a.get_center() + RIGHT*4, point_c.get_center() + RIGHT*4)
            )
        )
        line_co_green = Line(point_c.get_center() + RIGHT*4, ORIGIN + RIGHT*4).add_updater(lambda l: l.become(
            Line(point_c.update().get_center() + RIGHT*4, ORIGIN + RIGHT*4)
        ))

        angle_green_clone = always_redraw(lambda: Angle(
            line_ac_green.update(), line_co_green.update(), radius=1, quadrant=(-1, 1)
        ))
        def update_brace(shift):
            def func():
                #ln=Line(point_c.update().get_center() + shift, ORIGIN + shift)
                p=point_c.update()
                print("point: ",p.get_center()," update suspended: ",p.updating_suspended," distance:",distance.get_value())
                return BraceBetweenPoints(p.get_center()+shift,ORIGIN+shift,DOWN)
            return func

        # Add braces and labels
        brace_red = always_redraw(update_brace(LEFT*6))
        brace_blue = always_redraw(update_brace(LEFT))
        brace_green = always_redraw(update_brace(RIGHT*4))

        self.remove(tri_red, tri_blue, tri_green, angle_red, angle_blue, angle_green)
        self.add(tri_red_clone, tri_blue_clone, tri_green_clone, angle_red_clone, angle_blue_clone, angle_green_clone)

        # Debug: print the vertices of the polygons
        print(f"tri_red_clone vertices: {[point_a.get_center() + LEFT*6, point_b.get_center() + LEFT*6, point_c.get_center() + LEFT*6]}")
        print(f"tri_blue_clone vertices: {[point_b.get_center() + LEFT*1, ORIGIN + LEFT*1, point_c.get_center() + LEFT*1]}")
        print(f"tri_green_clone vertices: {[point_a.get_center() + RIGHT*4, ORIGIN + RIGHT*4, point_c.get_center() + RIGHT*4]}")

        

        
        # Animate the dot movement
        self.play(distance.animate.set_value(3))
        self.play(distance.animate.set_value(1), run_time=2)
        self.play(distance.animate.set_value(2), run_time=1)
        self.play(AnimationGroup(Create(brace_blue),Create(brace_green),Create(brace_red)))
        label_red = always_redraw(lambda: brace_red.update().get_text("t"))
        label_blue = always_redraw(lambda: brace_blue.update().get_text("t"))
        label_green = always_redraw(lambda: brace_green.update().get_text("t"))
        self.play(Create(label_red),Create(label_blue), Create(label_green),lag_ration=0.3)
        self.wait()
        self.play(
            Unwrite(tri_red_clone),
            Unwrite(tri_blue_clone),
            Unwrite(tri_green_clone),
            Unwrite(angle_blue_clone),
            Unwrite(angle_green_clone),
            Unwrite(label_blue),
            Unwrite(label_red),
            Unwrite(label_green)
        )
        self.play(Unwrite(brace_blue),Unwrite(brace_green),Unwrite(brace_red))
        
        # Display the tangent equations
        tan_equation_blue = MathTex(r"\tan(v) = \frac{2.5}{t}").shift(UP*0.5)
        tan_equation_green = MathTex(r"\tan(v) = \frac{1}{t}").shift(UP*0.5+RIGHT*5)

        self.play(Write(tan_equation_blue), Write(tan_equation_green))
        self.wait()

        # Replace equations with arctan
        arctan_equation_blue = MathTex(r"\arctan\left(\frac{2.5}{t}\right)",color=BLUE).shift(UP*0.5)
        arctan_equation_green = MathTex(r"\arctan\left(\frac{1}{t}\right)",color=GREEN).shift(UP*0.5+RIGHT*5)

        self.play(ReplacementTransform(tan_equation_blue, arctan_equation_blue), ReplacementTransform(tan_equation_green, arctan_equation_green))
        self.wait()
        
        group=Group(arctan_equation_blue,arctan_equation_green,equals,minus,angle_red_clone)
        tex=MathTex(r"v = \arctan\left(\frac{2.5}{t}\right)-\arctan\left(t^{-1}\right)")
        self.play(ReplacementTransform(group,tex))
        self.wait()
        arctan_derivative=MathTex(r"d/dx(arctan (x))= \frac{x'}{1+x^2}").shift(UP*3+RIGHT*3)
        derivative=MathTex(r"v'=\frac{1}{1+2.5/t}*\frac{-2}{t^2}-\frac{1}{1+1/t}*\frac{-1}{t^2}")
        derivative_2=MathTex(r"v'=\frac{3.75-1.5t^2}{t^4+7.25t^2+6.25}")
        self.play(Create(arctan_derivative))
        self.wait()
        self.play(ReplacementTransform(tex,derivative))
        self.wait()
        self.play(ReplacementTransform(derivative,derivative_2))
        self.wait(3)
        def func_2(x):
            return (3.75 - 1.5 * x**2) / (6.25 + 7.25 * x**2 + x**4)
        plane=Axes([-4,4,1],[-0.2,1,0.1])
        func=plane.plot(func_2)
        self.play(derivative_2.animate.shift(3*LEFT).scale(0.75), Create(plane))
        self.play(Create(func))
        awns=MathTex(r"t=\pm \sqrt{\frac{5}{2}}").shift(UP*2+LEFT*2)
        self.play(Create(awns))
        t1=Dot(plane.coords_to_point([[math.sqrt(5/2),0]]))
        t1_text=MathTex("\\left(0,\sqrt(\\frac{5}{2})\\right)").shift(plane.coords_to_point([[math.sqrt(5/2),0]])+UP*0.5).scale(0.5)
        t2=Dot(plane.coords_to_point([[-math.sqrt(5/2),0]]))
        t2_text=MathTex("\\left(0,-\sqrt(\\frac{5}{2})\\right)").shift(plane.coords_to_point([[-math.sqrt(5/2),0]])+UP*0.5).scale(0.5)
        self.play(Create(t1),Create(t1_text),Create(t2),Create(t2_text))
        self.wait(10)
        

class ThreeDTest(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()

        x_label = axes.get_x_axis_label(Tex("x"))
        y_label = axes.get_y_axis_label(Tex("y")).shift(UP * 1.8)

        # 3D variant of the Dot() object
        cube = Cube(2).stretch_to_fit_depth(5).stretch_to_fit_height(1.5).stretch_to_fit_width(0.1).shift(UP*1.75)
        
        # zoom out so we see the axes
        self.set_camera_orientation(zoom=0.5)

        self.play(FadeIn(axes),FadeIn(x_label), FadeIn(y_label))
        self.wait()
        
        self.wait(0.5)

        # animate the move of the camera to properly see the axes
        self.move_camera(phi=75 * DEGREES, theta=30 * DEGREES, zoom=1, run_time=1.5)
        
        self.play(Create(cube))
        # built-in updater which begins camera rotation
        self.begin_ambient_camera_rotation(rate=-0.60)
        
        self.wait(2)
        self.stop_ambient_camera_rotation()
        slizing_plane = Polygon(
            [1, 5, 0],  # Vertex 1
            [-1, 5, 0],  # Vertex 2
            [-1, -5, 0],  # Vertex 3
            [1, -5, 0],  # Vertex 4
            color=GREEN,
            fill_opacity=0.5
        )
        self.play(Create(slizing_plane))
        self.move_camera(phi=0,theta=PI/2,gamma=PI,run_time=2)
        self.wait(1)
        plane = Polygon(
            [0.1, 2.5, 0],  # Vertex 1
            [-0.1, 2.5, 0],  # Vertex 2
            [-0.1, 1, 0],  # Vertex 3
            [0.1, 1, 0],  # Vertex 4
            color=RED,
            fill_opacity=0.5
        )
        self.play(ReplacementTransform(cube,plane))
        self.wait()
        