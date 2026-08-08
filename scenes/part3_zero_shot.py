"""
DINO-WM — Part 3: "Zero-Shot Planning (Connecting the Dots)"
Manim Community v0.20+

Run individual scenes, e.g.:
    manim -pqh part3_zero_shot.py Scene1_TheSetup
    manim -pqh part3_zero_shot.py Scene2_BranchingFutures
    manim -pqh part3_zero_shot.py Scene3_PickingBestPath
    manim -pqh part3_zero_shot.py Scene4_ResultsChart

Or render everything back to back:
    manim -pqh part3_zero_shot.py Scene1_TheSetup Scene2_BranchingFutures Scene3_PickingBestPath Scene4_ResultsChart
"""

from manim import *
import numpy as np
import random

BG_DARK        = "#0B0C10"   # background used everywhere
LATENT_BLUE    = "#4361EE"   # start dot / latent space accent
LATENT_PURPLE  = "#7209B7"   # DINO-WM branding color
OIL_YELLOW     = "#FFD166"   # winning path / highlights
KITCHEN_RED    = "#E63946"   # distance lines (error/cost)
GREY_METAL     = "#8D99AE"   # simulated branches / prior SOTA
TARGET_GREEN   = "#2A9D8F"   # target dot 

random.seed(42)
np.random.seed(42)

# ====================================================================
# BASE CLASS (Utility)
# Defines the shared 3D environment for Scenes 1, 2, and 3.
# ====================================================================
class BaseLatentSpace(ThreeDScene):
    def setup_base(self):
        self.camera.background_color = BG_DARK 
        
        self.axes = ThreeDAxes(
            x_range=[-5, 5, 1], y_range=[-5, 5, 1], z_range=[-4, 4, 1],
            axis_config={"color": GREY_D}
        )
        
        self.pos_start = self.axes.c2p(-3, -2, -1)
        self.pos_goal = self.axes.c2p(3, 2, 2)
        
        self.start_dot = Sphere(center=self.pos_start, radius=0.15, color=LATENT_BLUE)
        self.goal_dot = Sphere(center=self.pos_goal, radius=0.15, color=TARGET_GREEN)
        
        self.start_label = Text("Start", color=LATENT_BLUE, font_size=24).next_to(self.start_dot, DOWN)
        self.goal_label = Text("Target", color=TARGET_GREEN, font_size=24).next_to(self.goal_dot, UP)
        
        # Simulated Timelines Data
        self.bad_paths = VGroup()
        for i in range(20):
            path_points = [self.pos_start]
            current_pos = np.array([-3.0, -2.0, -1.0])
            for _ in range(4):
                step = np.random.uniform(-1.5, 2.5, 3)
                current_pos += step
                path_points.append(self.axes.c2p(*current_pos))
            
            path = VMobject().set_points_as_corners(path_points)
            path.set_stroke(color=GREY_METAL, width=1.5, opacity=0.3)
            self.bad_paths.add(path)

        winning_points = [
            self.pos_start, self.axes.c2p(-1.5, -0.5, 0), self.axes.c2p(0.5, 1, 1),
            self.axes.c2p(2, 1.5, 1.8), self.axes.c2p(2.8, 1.9, 1.9)
        ]
        self.winning_path = VMobject().set_points_as_corners(winning_points)
        self.winning_path.set_stroke(color=OIL_YELLOW, width=3, opacity=0.8)


# ====================================================================
# SCENE 1
# ====================================================================
class Scene1_TheSetup(BaseLatentSpace):
    def construct(self):
        self.setup_base()
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        self.add_fixed_orientation_mobjects(self.start_label, self.goal_label)

        self.wait(4)
        self.play(Create(self.axes), run_time=3)
        self.wait(4)
        
        self.play(FadeIn(self.start_dot, shift=UP), Write(self.start_label), run_time=2)
        self.wait(2)
        
        self.play(FadeIn(self.goal_dot, shift=DOWN), Write(self.goal_label), run_time=2)
        self.move_camera(phi=65 * DEGREES, theta=-20 * DEGREES, run_time=5)
        self.wait(2)


# ====================================================================
# SCENE 2
# ====================================================================
class Scene2_BranchingFutures(BaseLatentSpace):
    def construct(self):
        self.setup_base()
        self.set_camera_orientation(phi=65 * DEGREES, theta=-20 * DEGREES)
        self.add_fixed_orientation_mobjects(self.start_label, self.goal_label)
        
        self.add(self.axes, self.start_dot, self.goal_dot)
        self.begin_ambient_camera_rotation(rate=0.04)

        self.wait(4)
        self.play(AnimationGroup(
            *[Create(path) for path in self.bad_paths],
            Create(self.winning_path),
            lag_ratio=0.15
        ), run_time=23)
        self.wait(4)
        
        self.stop_ambient_camera_rotation()


# ====================================================================
# SCENE 3
# ====================================================================
class Scene3_PickingBestPath(BaseLatentSpace):
    def construct(self):
        self.setup_base()
        self.set_camera_orientation(phi=65 * DEGREES, theta=10 * DEGREES) 
        self.add_fixed_orientation_mobjects(self.start_label, self.goal_label)
        
        self.add(self.axes, self.start_dot, self.goal_dot, self.bad_paths, self.winning_path)
        
        distance_lines = VGroup()
        for path in self.bad_paths[:4]:
            d_line = DashedLine(path.points[-1], self.pos_goal, color=KITCHEN_RED, dash_length=0.1)
            distance_lines.add(d_line)
            
        winning_d_line = DashedLine(self.winning_path.points[-1], self.pos_goal, color=OIL_YELLOW, dash_length=0.1)
        
        self.play(Create(distance_lines), run_time=4)
        self.wait(1)
        self.play(Create(winning_d_line), run_time=3)
        self.wait(3)
        
        self.play(
            FadeOut(self.bad_paths),
            FadeOut(distance_lines),
            FadeOut(winning_d_line),
            self.winning_path.animate.set_color(OIL_YELLOW).set_stroke(width=8, opacity=1),
            run_time=3
        )
        self.wait(1)

        # HIGHTLIGHT EFFECT (3B1B Style)
        highlight_dot = Sphere(center=self.winning_path.points[0], radius=0.12, color=WHITE)
        flash_path = self.winning_path.copy().set_color(WHITE).set_stroke(width=12, opacity=0.8)
        
        self.play(FadeIn(highlight_dot), run_time=0.5)
        
        self.play(
            MoveAlongPath(highlight_dot, self.winning_path),
            Create(flash_path),
            run_time=2.5,
            rate_func=linear
        )
        
        self.play(
            FadeOut(flash_path),
            FadeOut(highlight_dot),
            Flash(self.goal_dot, color=OIL_YELLOW, line_length=0.5, num_lines=12),
            run_time=1
        )
        
        self.wait(3)


# ====================================================================
# SCENE 4
# ====================================================================
class Scene4_ResultsChart(Scene):
    def construct(self):
        self.camera.background_color = BG_DARK

        title = Text("Performance on Contact-Rich Tasks", font_size=40, weight=BOLD)
        title.to_edge(UP, buff=1)
        
        chart = BarChart(
            values=[100, 145],
            bar_names=["Prior State-of-the-Art", "DINO-WM"],
            y_range=[0, 160, 40],
            y_length=4.5,
            x_length=7,
            bar_colors=[GREY_METAL, LATENT_PURPLE], 
            bar_fill_opacity=0.9
        )
        chart.next_to(title, DOWN, buff=0.5)
        
        baseline = DashedLine(start=chart.c2p(0, 100), end=chart.c2p(2, 100), color=GREY_B)
        improvement_text = Text("+ 45% Improvement!", font_size=36, color=OIL_YELLOW)
        improvement_text.next_to(chart.bars[1], UP, buff=0.3)
        
        self.wait(3)
        self.play(Write(title), run_time=3)
        self.wait(3)
        self.play(Create(chart.x_axis), Create(chart.y_axis), run_time=3)
        self.wait(2)
        
        self.play(Create(chart.bars[0]), run_time=3)
        self.play(Create(baseline), run_time=2)
        self.wait(3)
        
        self.play(Create(chart.bars[1]), run_time=3)
        self.wait(1)
        self.play(Write(improvement_text), run_time=2)
        self.play(Indicate(improvement_text, color=OIL_YELLOW, scale_factor=1.2), run_time=2)
        self.wait(5)
