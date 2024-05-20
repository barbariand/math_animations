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
        point_c = Dot([distance.get_value(), 0, 0],color=RED)

        # Updater for point_c position
        point_c.add_updater(lambda m: m.move_to([distance.get_value(), 0, 0]))

        # Connecting lines
        line_ac = always_redraw(lambda: Line(point_a.get_center(), point_c.get_center()))
        line_cb = always_redraw(lambda: Line(point_b.get_center(), point_c.get_center()))
        line_co=Line(point_c.get_center(),ORIGIN)
        # Angle between lines
        angle_acb = always_redraw(lambda: Angle(line_cb, line_ac, radius=1.0, quadrant=(-1, -1)))

        # Add objects to the scene
        self.add(plane)
        self.play(Write(point_a), Write(point_b), Write(point_c), lag_ratio=1.0)
        self.play(Create(line_ac),Create(line_cb))
        self.play(Create(angle_acb))
        # Animate the dot movement
        self.play(distance.animate.set_value(0.1))
        self.play(distance.animate.set_value(5), run_time=3)
        self.play(distance.animate.set_value(2), run_time=2)

        tri_blue=Polygon(point_b.get_center(),ORIGIN,point_c.get_center(),fill_opacity=1.0,fill_color=BLUE)
        tri_green=Polygon(point_a.get_center(),ORIGIN,point_c.get_center(),fill_opacity=1.0,fill_color=GREEN)
        tri_red=Polygon(point_a.get_center(),point_b.get_center(),point_c.get_center(),fill_opacity=1.0,fill_color=RED)
        angle_acb.set_z_index(1)
        self.play(Create(tri_blue),Create(tri_green),Create(tri_red),run_time=3)
        vertices=tri_red.get_vertices()

        # Create an angle annotation at vertex B (between line BC and line BA)
        angle_red = Angle(line_cb,line_ac, radius=1, quadrant=(-1, -1), color=WHITE)
        angle_green = Angle(line_ac,line_co,radius=1,quadrant=(-1,1))
        angle_blue=Angle(line_cb,line_co,radius=1,quadrant=(-1,1))
        self.remove(angle_acb),
        self.add(angle_red)
        self.play(Unwrite(point_a),Unwrite(point_b),Unwrite(point_c),Unwrite(line_ac),Unwrite(line_cb),Unwrite(plane),Create(angle_green))
        self.add(angle_blue)
        self.wait()
        self.play(
            AnimationGroup([tri_red.animate.shift(LEFT*6),
            angle_red.animate.shift(LEFT*6)]),
            AnimationGroup([tri_blue.animate.shift(LEFT*1),
            angle_blue.animate.shift(LEFT*1)]),
            AnimationGroup([tri_green.animate.shift(RIGHT*4),
            angle_green.animate.shift(RIGHT*4)]))
        minus=Tex("-").scale(3).shift(UP*0.5+RIGHT*2.5)
        equals=Tex("=").scale(3).shift(UP*0.5+LEFT*2.5)
        self.play(FadeIn(minus),FadeIn(equals),run_time=4)
        self.wait(2)
