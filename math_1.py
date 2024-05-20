from manim import *

# https://github.com/CaftBotti/manim_pi_creatures/tree/main/PiCreature
class MathScene(Scene):
    def construct(self):
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
        self.add(plane)
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
        self.wait()
        # Add braces and labels
        brace_red = always_redraw(lambda: Brace(Line(point_c.update().get_center() + LEFT*6, ORIGIN + LEFT*6), DOWN))
        brace_blue = always_redraw(lambda: Brace(Line(point_c.update().get_center() + LEFT, ORIGIN + LEFT), DOWN))
        brace_green = always_redraw(lambda: Brace(Line(point_c.update().get_center() + RIGHT*4, ORIGIN + RIGHT*4), DOWN))

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

        self.play(Transform(tan_equation_blue, arctan_equation_blue), Transform(tan_equation_green, arctan_equation_green))
        self.wait()