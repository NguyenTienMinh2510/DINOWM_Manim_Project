"""
DINO-WM — Part 1: "Why Predicting the Future Pixel-by-Pixel Is a Terrible Idea"
Manim Community v0.20+

Run individual scenes, e.g.:
    manim -pqh dino_wm_part1.py Scene1_IntroRobotKitchen
    manim -pqh dino_wm_part1.py Scene2_WorldModelFormula
    manim -pqh dino_wm_part1.py Scene3_PixelSpaceChaos
    manim -pqh dino_wm_part1.py Scene4_HumanConceptContrast
    manim -pqh dino_wm_part1.py Scene5_PixelToLatentTransform
    manim -pqh dino_wm_part1.py Scene6_Outro

Or render everything back to back:
    manim -pqh dino_wm_part1.py Scene1_IntroRobotKitchen Scene2_WorldModelFormula \
        Scene3_PixelSpaceChaos Scene4_HumanConceptContrast \
        Scene5_PixelToLatentTransform Scene6_Outro
"""

from manim import *
import numpy as np
import random

# ------------------------------------------------------------------
# GLOBAL PALETTE (kept consistent across every scene)
# ------------------------------------------------------------------
KITCHEN_ORANGE = "#FF9F1C"   # pixel-space accent
KITCHEN_RED    = "#E63946"   # pixel-space warning / emphasis
OIL_YELLOW     = "#FFD166"   # hot oil / chaos
LATENT_BLUE    = "#4361EE"   # latent-space accent
LATENT_PURPLE  = "#7209B7"   # latent-space title
BG_DARK        = "#0B0C10"   # background used everywhere
GREY_METAL     = "#8D99AE"   # robot body

random.seed(42)  # deterministic "randomness" so re-renders look identical


# ====================================================================
# SCENE 1  (0:00 - 0:35)
# VO: "Imagine you are a robot arm working in a fast-food kitchen all
#      day — frying chicken, scooping fries, over and over again...
#      To do this well you don't just need reflexes, you need to
#      IMAGINE. If I lift the basket now, what will the fries look
#      like in 3 seconds?"
# ====================================================================
class Scene1_IntroRobotKitchen(Scene):
    def construct(self):
        self.camera.background_color = BG_DARK

        robot = self.build_robot_arm().to_edge(LEFT, buff=1.2)
        pan = self.build_frying_pan().to_edge(RIGHT, buff=1.2)

        self.play(FadeIn(robot, shift=RIGHT * 0.3), run_time=1)
        self.play(FadeIn(pan, shift=LEFT * 0.3), run_time=1)
        self.wait(0.5)

        caption = Text(
            "A robot arm in a fast-food kitchen.",
            font_size=32, color=WHITE
        ).to_edge(UP, buff=0.6)
        self.play(FadeIn(caption, shift=DOWN * 0.2))
        self.wait(1.5)
        self.play(FadeOut(caption))

        # --- Prediction timeline -----------------------------------
        timeline = NumberLine(
            x_range=[0, 10, 1],
            length=8,
            color=GREY_B,
            include_numbers=False,
        ).to_edge(DOWN, buff=0.9)
        now_label = Text("now", font_size=24, color=WHITE).next_to(
            timeline.n2p(0), DOWN, buff=0.3
        )
        future_label = Text("+3s", font_size=24, color=WHITE).next_to(
            timeline.n2p(6), DOWN, buff=0.3
        )
        cursor = Dot(color=WHITE, radius=0.09).move_to(timeline.n2p(0))

        self.play(Create(timeline), FadeIn(now_label))
        self.play(FadeIn(cursor))
        self.wait(0.3)

        question = Text(
            "What will this look like in the future?",
            font_size=30, color=OIL_YELLOW
        ).to_edge(UP, buff=0.6)
        self.play(Write(question))

        self.play(
            cursor.animate.move_to(timeline.n2p(6)),
            FadeIn(future_label),
            run_time=2,
        )

        # Ghost frames = uncertain future predictions, fading in with
        # increasing opacity to suggest growing (but blurry) confidence
        ghost_frames = VGroup(*[
            Square(
                side_length=0.9,
                fill_color=OIL_YELLOW,
                fill_opacity=0.15 + 0.18 * i,
                stroke_color=OIL_YELLOW,
                stroke_opacity=0.4 + 0.15 * i,
            )
            for i in range(3)
        ]).arrange(RIGHT, buff=0.35).next_to(cursor, UP, buff=1.1)

        self.play(LaggedStart(
            *[FadeIn(f, scale=0.8) for f in ghost_frames],
            lag_ratio=0.35, run_time=1.5
        ))
        self.wait(2)

        self.play(
            *[FadeOut(m) for m in
              (robot, pan, timeline, now_label, future_label,
               cursor, question, ghost_frames)]
        )

    # -- helpers ------------------------------------------------------
    def build_robot_arm(self):
        base = RoundedRectangle(
            width=0.9, height=0.5, corner_radius=0.08,
            fill_color=GREY_METAL, fill_opacity=1, stroke_width=0
        )
        forearm = RoundedRectangle(
            width=0.28, height=1.6, corner_radius=0.08,
            fill_color=GREY_METAL, fill_opacity=1, stroke_width=0
        ).next_to(base, UP, buff=-0.05)
        joint = Circle(radius=0.16, fill_color=GREY_B, fill_opacity=1,
                        stroke_width=0).move_to(forearm.get_top())
        claw_l = Line(ORIGIN, RIGHT * 0.35, stroke_width=6,
                       color=GREY_METAL).next_to(joint, UR, buff=-0.05)
        claw_r = Line(ORIGIN, RIGHT * 0.35, stroke_width=6,
                       color=GREY_METAL).next_to(joint, DR, buff=-0.05)
        return VGroup(base, forearm, joint, claw_l, claw_r)

    def build_frying_pan(self):
        pan = Ellipse(width=4.4, height=1.6, fill_color=GREY_D,
                       fill_opacity=1, stroke_width=0)
        oil = Ellipse(width=4.0, height=1.25, fill_color=OIL_YELLOW,
                       fill_opacity=0.9, stroke_width=0).move_to(pan)
        return VGroup(pan, oil)


# ====================================================================
# SCENE 2  (0:35 - 1:20)
# VO: "That ability — predicting the future observation given an
#      action — is exactly what a World Model is. But what IS an
#      observation, really? This is where most AI takes a very
#      costly wrong turn."
# ====================================================================
class Scene2_WorldModelFormula(Scene):
    def construct(self):
        self.camera.background_color = BG_DARK

        title = Text("World Model", font_size=40, color=WHITE).to_edge(UP, buff=0.8)
        self.play(Write(title))
        self.wait(0.5)

        formula = MathTex(
            r"P(", r"O_{t+1}", r"\mid", r"O_{\le t}", r",", r"A_{\le t}", r")",
            font_size=64
        )
        formula.set_color(WHITE)
        self.play(Write(formula), run_time=2)
        self.wait(0.5)

        label_future = Text("future observation", font_size=22, color=OIL_YELLOW)
        label_past_obs = Text("past observations", font_size=22, color=LATENT_BLUE)
        label_actions = Text("past actions", font_size=22, color=KITCHEN_RED)

        label_future.next_to(formula[1], UP, buff=0.5)
        label_past_obs.next_to(formula[3], DOWN, buff=0.5)
        label_actions.next_to(formula[5], DOWN, buff=0.5)

        arrow_future = Arrow(
            label_future.get_bottom(), formula[1].get_top(),
            buff=0.1, stroke_width=2, color=OIL_YELLOW
        )
        arrow_past = Arrow(
            label_past_obs.get_top(), formula[3].get_bottom(),
            buff=0.1, stroke_width=2, color=LATENT_BLUE
        )
        arrow_actions = Arrow(
            label_actions.get_top(), formula[5].get_bottom(),
            buff=0.1, stroke_width=2, color=KITCHEN_RED
        )

        self.play(
            FadeIn(label_future, shift=DOWN * 0.2), GrowArrow(arrow_future)
        )
        self.play(
            FadeIn(label_past_obs, shift=UP * 0.2), GrowArrow(arrow_past)
        )
        self.play(
            FadeIn(label_actions, shift=UP * 0.2), GrowArrow(arrow_actions)
        )
        self.wait(1.5)

        self.play(
            *[FadeOut(m) for m in
              (label_past_obs, label_actions, arrow_past, arrow_actions)]
        )

        # Zoom emphasis on O_{t+1} — the key open question
        self.play(Circumscribe(formula[1], color=KITCHEN_RED, run_time=1.2))
        question_mark = Text("What IS an observation?", font_size=30,
                              color=KITCHEN_RED).next_to(formula, DOWN, buff=1.2)
        self.play(Write(question_mark))
        self.wait(2)

        self.play(*[FadeOut(m) for m in
                     (title, formula, label_future, arrow_future, question_mark)])


# ====================================================================
# SCENE 3  (1:20 - 3:00)
# VO: "The most intuitive answer: the observation IS the image, a
#      grid of RGB pixels. So imagining the future means... redrawing
#      every single pixel. But look closer at this frying oil: bubbles
#      bursting, steam curling, light flickering. To predict correctly,
#      the model must compute RGB values for every one of these,
#      for every future frame."
# ====================================================================
class Scene3_PixelSpaceChaos(MovingCameraScene):
    def construct(self):
        self.camera.background_color = BG_DARK

        # 1. Dựng chảo và dầu
        pan = Ellipse(width=6.4, height=2.6, fill_color=GREY_D, fill_opacity=1, stroke_width=0)
        oil = Ellipse(width=6.0, height=2.25, fill_color=OIL_YELLOW, fill_opacity=0.9, stroke_width=0).move_to(pan)
        kitchen = VGroup(pan, oil)
        self.play(FadeIn(kitchen))

        caption1 = Text("Observation = a grid of RGB pixels?", font_size=30, color=WHITE).to_edge(UP, buff=0.6)
        self.play(Write(caption1))
        self.wait(1)

        # 2. Tạo lưới Pixel ĐÃ ĐƯỢC CẮT GỌN NẰM GÓC TRONG CHẢO (Fix tràn viền)
        grid = self.build_pixel_grid(rows=16, cols=32, width=6.0, height=2.25, center=oil.get_center())
        self.play(FadeIn(grid), run_time=1.2)
        self.wait(0.5)
        self.play(FadeOut(caption1))

        # 3. Zoom Camera vào điểm trung tâm lưới
        zoom_target_point = oil.get_center() + LEFT * 1.5  # Zoom vào vùng bên trái sạch sẽ
        self.play(
            self.camera.frame.animate.scale(0.35).move_to(zoom_target_point),
            run_time=2.0,
        )
        self.wait(0.3)

        # Fix chữ chú thích khi camera đang Zoom (Gắn trực tiếp theo khung camera)
        caption2 = Text("Oil bubbles. Steam. Flickering light.", font_size=16, color=WHITE)
        caption2.move_to(self.camera.frame.get_top() + DOWN * 0.3)
        self.play(Write(caption2))

        # Bọt dầu nổi lên có trật tự hơn
        bubbles = self.spawn_bubbles(count=12, center=zoom_target_point, spread=0.5)
        self.play(LaggedStart(
            *[Succession(GrowFromCenter(b), FadeOut(b)) for b in bubbles],
            lag_ratio=0.15, run_time=2.0
        ))

        # Fix số RGB nằm gọn theo từng ô Pixel (Không bị đè chữ)
        rgb_numbers = self.spawn_grid_rgb_numbers(grid_center=zoom_target_point, count=8, font_size=8)
        self.play(LaggedStart(
            *[FadeIn(r, scale=0.8) for r in rgb_numbers],
            lag_ratio=0.1, run_time=1.8
        ))
        self.wait(1)

        self.play(FadeOut(caption2), FadeOut(rgb_numbers))

        # 4. Zoom out về lại toàn màn hình
        self.play(self.camera.frame.animate.scale(1/0.35).move_to(ORIGIN), run_time=1.5)

        # Mưa số RGB toàn màn hình (Căn khoảng cách tối thiểu giữa các số)
        full_rgb_rain = self.spawn_separated_rgb_numbers(count=25, font_size=12)
        self.play(LaggedStart(*[FadeIn(r) for r in full_rgb_rain], lag_ratio=0.04, run_time=2))

        overload_caption = Text("Thousands of numbers. Every single frame.", font_size=28, color=KITCHEN_RED).to_edge(UP, buff=0.6)
        self.play(Write(overload_caption))
        self.wait(2)

        self.play(*[FadeOut(m) for m in (kitchen, grid, full_rgb_rain, overload_caption)])

    # -- HELPER FUNCTIONS ĐÃ ĐƯỢC FIX TOÁN HỌC --
    def build_pixel_grid(self, rows, cols, width, height, center):
        cell_w, cell_h = width / cols, height / rows
        cells = VGroup()
        palette = [OIL_YELLOW, KITCHEN_ORANGE, WHITE]
        
        # Phương trình Elip cắt viền: (x/a)^2 + (y/b)^2 <= 1
        a, b = width / 2, height / 2
        for r in range(rows):
            for c in range(cols):
                x_pos = -width / 2 + c * cell_w + cell_w / 2
                y_pos = -height / 2 + r * cell_h + cell_h / 2
                
                # Chỉ vẽ những ô pixel nằm gọn hoàn toàn bên trong Elip chảo dầu
                if (x_pos / a)**2 + (y_pos / b)**2 <= 0.85:
                    color = random.choice(palette)
                    cell = Square(
                        side_length=min(cell_w, cell_h) * 0.95,
                        fill_color=color,
                        fill_opacity=random.uniform(0.15, 0.45),
                        stroke_width=0.3,
                        stroke_color=BG_DARK,
                    )
                    cell.move_to(center + np.array([x_pos, y_pos, 0]))
                    cells.add(cell)
        return cells

    def spawn_bubbles(self, count, center, spread):
        return VGroup(*[
            Circle(radius=random.uniform(0.02, 0.04), color=WHITE, fill_opacity=0.7, stroke_width=0.5)
            .move_to(center + np.array([random.uniform(-spread, spread), random.uniform(-spread*0.3, spread*0.3), 0]))
            for _ in range(count)
        ])

    def spawn_grid_rgb_numbers(self, grid_center, count, font_size):
        # Tạo vị trí đặt số theo mạng lưới đều (Grid Layout) để không đè lên nhau
        numbers = VGroup()
        offsets = [
            (-0.4, 0.2), (0.1, 0.3), (-0.2, -0.2), (0.4, -0.1),
            (-0.5, -0.3), (0.3, 0.2), (-0.1, 0.4), (0.0, -0.4)
        ]
        for idx in range(min(count, len(offsets))):
            ox, oy = offsets[idx]
            txt = Text(f"({random.randint(180,255)},{random.randint(100,180)},{random.randint(0,60)})",
                       font_size=font_size, color=WHITE)
            txt.move_to(grid_center + np.array([ox, oy, 0]))
            numbers.add(txt)
        return numbers

    def spawn_separated_rgb_numbers(self, count, font_size):
        # Sinh chuỗi số có thuật toán kiểm tra khoảng cách tối thiểu (Poisson-like disk filtering)
        numbers = VGroup()
        placed_positions = []
        attempts = 0
        while len(placed_positions) < count and attempts < 300:
            attempts += 1
            x = random.uniform(-2.5, 2.5)
            y = random.uniform(-0.8, 0.8)
            new_pos = np.array([x, y, 0])
            
            # Kiểm tra xem có bị quá gần điểm nào đã đặt chưa
            too_close = False
            for p in placed_positions:
                if np.linalg.norm(p - new_pos) < 0.6:  # Khoảng cách tối thiểu 0.6 unit
                    too_close = True
                    break
            
            if not too_close:
                placed_positions.append(new_pos)
                txt = Text(f"({random.randint(180,255)},{random.randint(100,180)},{random.randint(0,60)})",
                           font_size=font_size, color=WHITE)
                txt.move_to(new_pos)
                numbers.add(txt)
        return numbers

# ====================================================================
# SCENE 4  (3:00 - 3:20)
# VO: "But does a human cook think about every bubble? No. A cook
#      just needs to know one thing: is the chicken golden yet?"
# ====================================================================
class Scene4_HumanConceptContrast(Scene):
    def construct(self):
        self.camera.background_color = BG_DARK

        chicken = RoundedRectangle(
            width=2.6, height=1.6, corner_radius=0.4,
            fill_color=KITCHEN_ORANGE, fill_opacity=1, stroke_width=0
        ).shift(LEFT * 2.5)
        self.play(FadeIn(chicken))

        caption = Text(
            "A cook doesn't track every bubble.",
            font_size=30, color=WHITE
        ).to_edge(UP, buff=0.6)
        self.play(Write(caption))
        self.wait(1)

        labels = VGroup(
            Text("Color: golden brown", font_size=26, color=OIL_YELLOW),
            Text("Basket: 5 cm away", font_size=26, color=LATENT_BLUE),
            Text("Time frying: 6 minutes", font_size=26, color=KITCHEN_RED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).shift(RIGHT * 2.8)

        self.play(LaggedStart(
            *[Write(l) for l in labels], lag_ratio=0.4, run_time=2
        ))
        self.wait(1.5)

        concept_caption = Text(
            "Just a handful of CONCEPTS.",
            font_size=32, color=WHITE
        ).to_edge(DOWN, buff=0.8)
        self.play(FadeOut(caption), Write(concept_caption))
        self.wait(2)

        self.play(*[FadeOut(m) for m in (chicken, labels, concept_caption)])


# ====================================================================
# SCENE 5  (3:20 - 4:15)
# VO: "Predicting in PIXEL SPACE forces the model to waste almost all
#      its compute on details that don't matter for the decision. What
#      if, instead, the model imagined the future using the same kind
#      of concepts a human uses — a compact LATENT SPACE?"
# ====================================================================
class Scene5_PixelToLatentTransform(Scene):
    def construct(self):
        self.camera.background_color = BG_DARK

        left_title = Text("Pixel Space", font_size=30, color=KITCHEN_ORANGE)
        left_title.to_edge(UP, buff=0.7).shift(LEFT * 3.2)
        self.play(Write(left_title))

        pixel_dots = VGroup(*[
            Dot(radius=0.035, color=OIL_YELLOW, fill_opacity=random.uniform(0.5, 1))
            .move_to(np.array([
                random.uniform(-5.5, -1.2),
                random.uniform(-2.0, 1.8),
                0,
            ]))
            for _ in range(180)
        ])
        self.play(FadeIn(pixel_dots), run_time=1.2)

        waste_caption = Text(
            "Expensive. Wasteful. Mostly irrelevant.",
            font_size=24, color=KITCHEN_RED
        ).to_edge(DOWN, buff=0.6)
        self.play(Write(waste_caption))
        self.wait(1.5)
        self.play(FadeOut(waste_caption))

        right_title = Text("Latent Space", font_size=30, color=LATENT_BLUE)
        right_title.to_edge(UP, buff=0.7).shift(RIGHT * 3.2)

        axes = Axes(
            x_range=[-3, 3, 1], y_range=[-2, 2, 1],
            x_length=4, y_length=3, tips=False,
            axis_config={"color": GREY_B, "stroke_width": 1.5},
        ).shift(RIGHT * 3.2)

        target_positions = [
            axes.c2p(random.uniform(-2.6, 2.6), random.uniform(-1.6, 1.6))
            for _ in range(20)
        ]
        latent_dots = VGroup(*[
            Dot(radius=0.06, color=LATENT_BLUE).move_to(pos)
            for pos in target_positions
        ])

        # Reuse a random subset of the pixel dots to "become" the latent dots,
        # and fade out the rest — a visual metaphor for compression.
        movers = VGroup(*random.sample(list(pixel_dots), 20))
        leftovers = VGroup(*[d for d in pixel_dots if d not in movers])

        self.play(
            FadeIn(right_title),
            FadeIn(axes),
            FadeOut(leftovers, run_time=1.5),
            Transform(movers, latent_dots, run_time=2.5),
        )
        self.wait(1)

        compress_caption = Text(
            "A few clean numbers. The essence, not the noise.",
            font_size=24, color=LATENT_BLUE
        ).to_edge(DOWN, buff=0.6)
        self.play(Write(compress_caption))
        self.wait(2)

        self.play(*[FadeOut(m) for m in
                     (left_title, right_title, axes, movers, compress_caption)])


# ====================================================================
# SCENE 6  (4:15 - 4:30)
# VO: "This is the core idea behind DINO-WM, the model we'll dissect
#      next. Remember this messy frying pan — because the rest of the
#      story is about turning that chaos into a handful of clean
#      numbers, without losing what actually matters."
# ====================================================================
class Scene6_Outro(Scene):
    def construct(self):
        self.camera.background_color = BG_DARK

        title = Text("DINO-WM", font_size=64, color=LATENT_PURPLE)
        subtitle = Text(
            "World Models in Latent Space", font_size=28, color=GREY_B
        )
        group = VGroup(title, subtitle).arrange(DOWN, buff=0.3)

        self.play(Write(title))
        self.play(FadeIn(subtitle, shift=UP * 0.2))
        self.wait(2)
        self.play(FadeOut(group))
        self.wait(0.5)
