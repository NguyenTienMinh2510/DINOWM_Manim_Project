"""
DINO-WM — Part 2: "Seeing in Latent Space"

Render the complete part:
    manim -pqh scenes/part2_latent_space.py LatentSpaceScene

Render one section:
    manim -pqh scenes/part2_latent_space.py Scene1_DINOv2Encoder
    manim -pqh scenes/part2_latent_space.py Scene2_PatchesAndVectors
    manim -pqh scenes/part2_latent_space.py Scene3_ViTTransition
    manim -pqh scenes/part2_latent_space.py Scene4_MissingDecoder
"""

from manim import *
import numpy as np
import random


# Keep the visual language aligned with Parts 1 and 3.
BG_DARK = "#0B0C10"
LATENT_BLUE = "#4361EE"
LATENT_PURPLE = "#7209B7"
OIL_YELLOW = "#FFD166"
KITCHEN_ORANGE = "#FF9F1C"
KITCHEN_RED = "#E63946"
TARGET_GREEN = "#2A9D8F"
GREY_METAL = "#8D99AE"

random.seed(42)
np.random.seed(42)


class Part2Visuals:
    """Shared visual builders and narrative beats for every Part 2 render."""

    def setup_part2(self):
        self.camera.background_color = BG_DARK

    def section_title(self, number, title, color=WHITE):
        kicker = Text(number, font_size=22, color=GREY_METAL)
        heading = Text(title, font_size=38, color=color, weight=BOLD)
        group = VGroup(kicker, heading).arrange(DOWN, buff=0.16)
        group.to_edge(UP, buff=0.35)
        return group

    def model_block(self, label, width=2.4, height=1.35, color=LATENT_PURPLE):
        outer = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.16,
            color=color,
            stroke_width=3,
            fill_color=color,
            fill_opacity=0.13,
        )
        inner = RoundedRectangle(
            width=width - 0.16,
            height=height - 0.16,
            corner_radius=0.12,
            color=color,
            stroke_width=1,
            stroke_opacity=0.45,
        )
        text = Text(label, font_size=28, color=WHITE, weight=BOLD)
        return VGroup(outer, inner, text)

    def observation(self, width=4.8, height=3.0):
        """A procedural robot-arm, block, and table observation."""
        frame = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.12,
            color=GREY_METAL,
            stroke_width=2,
            fill_color="#17212B",
            fill_opacity=1,
        )
        floor = Rectangle(
            width=width - 0.12,
            height=0.74,
            fill_color="#37414C",
            fill_opacity=1,
            stroke_width=0,
        ).align_to(frame, DOWN).shift(UP * 0.06)
        table_line = Line(
            frame.get_left() + UP * 0.04,
            frame.get_right() + UP * 0.04,
            color=GREY_METAL,
            stroke_width=5,
        ).shift(DOWN * 0.46)

        base = RoundedRectangle(
            width=0.72,
            height=0.38,
            corner_radius=0.06,
            fill_color=GREY_METAL,
            fill_opacity=1,
            stroke_width=0,
        ).move_to(frame.get_left() + RIGHT * 0.72 + DOWN * 0.83)
        shoulder = Dot(base.get_top() + UP * 0.10, radius=0.14, color=LATENT_BLUE)
        upper = Line(shoulder.get_center(), shoulder.get_center() + UP * 0.92 + RIGHT * 0.45,
                     color=GREY_METAL, stroke_width=12)
        elbow = Dot(upper.get_end(), radius=0.13, color=LATENT_BLUE)
        forearm = Line(elbow.get_center(), elbow.get_center() + RIGHT * 0.95 + DOWN * 0.20,
                       color=GREY_METAL, stroke_width=11)
        wrist = Dot(forearm.get_end(), radius=0.11, color=LATENT_BLUE)
        claw_top = Line(wrist.get_center(), wrist.get_center() + RIGHT * 0.32 + UP * 0.17,
                        color=OIL_YELLOW, stroke_width=6)
        claw_bottom = Line(wrist.get_center(), wrist.get_center() + RIGHT * 0.32 + DOWN * 0.17,
                           color=OIL_YELLOW, stroke_width=6)
        block = RoundedRectangle(
            width=0.62,
            height=0.62,
            corner_radius=0.06,
            fill_color=KITCHEN_ORANGE,
            fill_opacity=1,
            color=OIL_YELLOW,
            stroke_width=2,
        ).move_to(frame.get_center() + RIGHT * 1.35 + DOWN * 0.52)

        scene = VGroup(
            frame,
            floor,
            table_line,
            base,
            upper,
            shoulder,
            elbow,
            forearm,
            wrist,
            claw_top,
            claw_bottom,
            block,
        )
        # Keep references to scene mobjects rather than snapshot coordinates so
        # highlights stay registered when the complete observation is shifted.
        anchors = {
            "arm": upper,
            "gripper": claw_top,
            "block": block,
            "background": frame,
        }
        return scene, anchors

    def pixel_grid(self, rows=8, cols=12, width=4.6, height=2.8):
        palette = [KITCHEN_ORANGE, OIL_YELLOW, KITCHEN_RED, GREY_METAL, LATENT_BLUE]
        cells = VGroup()
        cell_w = width / cols
        cell_h = height / rows
        for row in range(rows):
            for col in range(cols):
                index = (row * 7 + col * 11) % len(palette)
                opacity = 0.22 + 0.09 * ((row + 2 * col) % 5)
                cell = Rectangle(
                    width=cell_w * 0.94,
                    height=cell_h * 0.92,
                    stroke_color=BG_DARK,
                    stroke_width=0.7,
                    fill_color=palette[index],
                    fill_opacity=opacity,
                )
                cell.move_to(
                    np.array([
                        -width / 2 + (col + 0.5) * cell_w,
                        -height / 2 + (row + 0.5) * cell_h,
                        0,
                    ])
                )
                cells.add(cell)
        border = RoundedRectangle(
            width=width + 0.08,
            height=height + 0.08,
            corner_radius=0.1,
            color=KITCHEN_ORANGE,
            stroke_width=2,
        )
        return VGroup(cells, border)

    def patch_grid(self, target, divisions=16):
        left, right = target.get_left()[0], target.get_right()[0]
        bottom, top = target.get_bottom()[1], target.get_top()[1]
        lines = VGroup()
        for index in range(divisions + 1):
            x = left + (right - left) * index / divisions
            y = bottom + (top - bottom) * index / divisions
            lines.add(Line([x, bottom, 0], [x, top, 0], color=WHITE,
                           stroke_width=0.65, stroke_opacity=0.48))
            lines.add(Line([left, y, 0], [right, y, 0], color=WHITE,
                           stroke_width=0.65, stroke_opacity=0.48))
        return lines

    def vector_column(self, values, color=LATENT_BLUE):
        cells = VGroup()
        for value in values:
            box = RoundedRectangle(
                width=1.15,
                height=0.38,
                corner_radius=0.05,
                color=color,
                fill_color=color,
                fill_opacity=0.14,
                stroke_width=1.4,
            )
            number = (
                MathTex(r"\vdots", font_size=24, color=GREY_METAL)
                if value is None
                else Text(f"{value:+.2f}", font_size=18, color=WHITE)
            )
            cells.add(VGroup(box, number))
        cells.arrange(DOWN, buff=0.05)
        brackets = VGroup(
            Line(cells.get_corner(UL) + LEFT * 0.13, cells.get_corner(DL) + LEFT * 0.13,
                 color=GREY_METAL, stroke_width=2),
            Line(cells.get_corner(UR) + RIGHT * 0.13, cells.get_corner(DR) + RIGHT * 0.13,
                 color=GREY_METAL, stroke_width=2),
        )
        return VGroup(cells, brackets)

    def token_row(self, count=8, future=False):
        tokens = VGroup()
        palette = [LATENT_BLUE, LATENT_BLUE, KITCHEN_ORANGE, OIL_YELLOW,
                   LATENT_BLUE, TARGET_GREEN, LATENT_BLUE, LATENT_BLUE]
        for index in range(count):
            color = palette[index % len(palette)]
            token = RoundedRectangle(
                width=0.62,
                height=1.05,
                corner_radius=0.09,
                color=color,
                fill_color=color,
                fill_opacity=0.17,
                stroke_width=2,
            )
            bars = VGroup(*[
                Line(LEFT * (0.17 + 0.025 * ((index + j) % 3)),
                     RIGHT * (0.17 + 0.025 * ((index + j) % 3)),
                     color=color, stroke_width=2)
                for j in range(3)
            ]).arrange(DOWN, buff=0.12).move_to(token)
            item = VGroup(token, bars)
            if future and index in (2, 3):
                item.shift(RIGHT * 0.08 + UP * 0.08)
                item.set_color(TARGET_GREEN)
            tokens.add(item)
        tokens.arrange(RIGHT, buff=0.13)
        return tokens

    def attention_curve(self, start, end, color=LATENT_BLUE, opacity=1.0, lift=1.0):
        delta = end - start
        return CubicBezier(
            start,
            start + RIGHT * delta[0] * 0.35 + UP * lift,
            end - RIGHT * delta[0] * 0.35 + UP * lift,
            end,
            color=color,
            stroke_width=3,
            stroke_opacity=opacity,
        )

    def reset_stage(self):
        self.clear()
        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES)

    # -----------------------------------------------------------------
    # Narrative beat 1: frozen DINOv2 encoder and semantic attention.
    # -----------------------------------------------------------------
    def beat_dinov2_encoder(self):
        title = self.section_title("2.1", "Borrowing a Pre-trained Brain", LATENT_PURPLE)
        pixel_grid = self.pixel_grid().scale(0.73).shift(LEFT * 4.55 + DOWN * 0.25)
        pixel_label = Text("pixels", font_size=24, color=KITCHEN_ORANGE).next_to(pixel_grid, DOWN, buff=0.22)
        encoder = self.model_block("DINOv2", color=LATENT_PURPLE).shift(DOWN * 0.20)
        frozen = VGroup(
            Text("FROZEN", font_size=18, color=LATENT_BLUE, weight=BOLD),
            Text("pre-trained encoder", font_size=16, color=GREY_METAL),
        ).arrange(DOWN, buff=0.05).next_to(encoder, DOWN, buff=0.18)

        latent_nodes = VGroup(*[
            Dot(radius=0.11 + 0.02 * (index % 3), color=[LATENT_BLUE, TARGET_GREEN, OIL_YELLOW][index % 3])
            .move_to([3.2 + 0.55 * (index % 4), -0.75 + 0.65 * (index // 4), 0])
            for index in range(12)
        ])
        connections = VGroup()
        for index, dot in enumerate(latent_nodes):
            if index % 3 != 1:
                connections.add(Line(dot.get_center(), latent_nodes[(index + 1) % 12].get_center(),
                                     color=LATENT_BLUE, stroke_width=1, stroke_opacity=0.35))
        manifold = VGroup(connections, latent_nodes)
        latent_label = Text("spatial features", font_size=24, color=LATENT_BLUE).next_to(manifold, DOWN, buff=0.25)
        arrow_in = Arrow(pixel_grid.get_right(), encoder.get_left(), buff=0.22, color=GREY_METAL)
        arrow_out = Arrow(encoder.get_right(), manifold.get_left(), buff=0.22, color=LATENT_BLUE)

        self.play(FadeIn(title, shift=DOWN * 0.15), run_time=1.2)
        self.wait(0.8)
        self.play(FadeIn(pixel_grid), FadeIn(pixel_label), run_time=2.2)
        self.wait(1.8)
        self.play(
            GrowArrow(arrow_in),
            FadeIn(encoder, shift=DOWN * 0.2),
            FadeIn(frozen),
            run_time=2.2,
        )
        self.wait(1.0)
        self.play(
            GrowArrow(arrow_out),
            LaggedStart(*[GrowFromCenter(dot) for dot in latent_nodes], lag_ratio=0.07),
            Create(connections),
            run_time=3.0,
        )
        self.wait(2.0)
        self.play(FadeIn(latent_label), run_time=1.4)
        self.play(Indicate(manifold, color=OIL_YELLOW, scale_factor=1.06), run_time=1.8)
        self.wait(1.3)

        self.play(*[FadeOut(mob) for mob in (
            pixel_grid, pixel_label, encoder, frozen, manifold, latent_label, arrow_in, arrow_out
        )], run_time=1.3)

        observation, anchors = self.observation(width=6.0, height=3.25)
        observation.shift(DOWN * 0.28)
        attention_label = Text(
            "Illustrative semantic attention",
            font_size=24,
            color=WHITE,
        ).to_edge(DOWN, buff=0.3)
        attention_label.add_background_rectangle(color=BG_DARK, opacity=0.85, buff=0.12)
        dimmer = observation[0].copy().set_fill(BG_DARK, opacity=0.48).set_stroke(opacity=0)
        heat = VGroup(
            Circle(radius=0.72, fill_color=LATENT_BLUE, fill_opacity=0.22,
                   stroke_color=LATENT_BLUE, stroke_opacity=0.55).move_to(anchors["arm"].get_center()),
            Circle(radius=0.54, fill_color=OIL_YELLOW, fill_opacity=0.28,
                   stroke_color=OIL_YELLOW, stroke_opacity=0.65).move_to(anchors["gripper"].get_center()),
            Circle(radius=0.62, fill_color=KITCHEN_ORANGE, fill_opacity=0.32,
                   stroke_color=KITCHEN_ORANGE, stroke_opacity=0.7).move_to(anchors["block"].get_center()),
        )
        self.play(FadeIn(observation, scale=0.96), run_time=1.8)
        self.wait(1.0)
        self.play(
            FadeIn(dimmer),
            LaggedStart(*[GrowFromCenter(circle) for circle in heat], lag_ratio=0.25),
            FadeIn(attention_label),
            run_time=2.8,
        )
        self.wait(2.5)
        self.play(Flash(observation[-1], color=OIL_YELLOW, line_length=0.28, num_lines=10), run_time=1.3)
        self.wait(1.2)
        self.play(FadeOut(VGroup(title, observation, dimmer, heat, attention_label)), run_time=1.5)
        self.reset_stage()

    # -----------------------------------------------------------------
    # Narrative beat 2: patches, vectors, and an explicit 3D projection.
    # -----------------------------------------------------------------
    def beat_patches_and_vectors(self):
        title = self.section_title("2.2", "Slicing the World", LATENT_BLUE)
        observation, anchors = self.observation(width=5.0, height=3.0)
        observation.shift(LEFT * 2.8 + DOWN * 0.30)
        grid = self.patch_grid(observation[0], divisions=16)
        grid_label = Text("16 × 16 patch grid", font_size=22, color=WHITE).next_to(observation, DOWN, buff=0.22)

        self.play(FadeIn(title, shift=DOWN * 0.15), FadeIn(observation), run_time=1.5)
        self.wait(1.5)
        self.play(Create(grid), FadeIn(grid_label), run_time=2.3)
        self.wait(2.5)

        patch = Square(side_length=0.52, color=OIL_YELLOW, stroke_width=4,
                       fill_color=KITCHEN_ORANGE, fill_opacity=0.28)
        patch.move_to(anchors["block"].get_center() + LEFT * 0.02 + UP * 0.02)
        patch_label = Text("one patch", font_size=20, color=OIL_YELLOW).next_to(patch, UP, buff=0.12)
        self.play(Create(patch), FadeIn(patch_label), run_time=1.5)
        self.wait(1.0)

        vector = self.vector_column([0.84, -0.12, None, 0.91, -0.35], color=LATENT_BLUE)
        vector.shift(RIGHT * 4.3 + DOWN * 0.12)
        vector_label = VGroup(
            Text("high-dimensional embedding", font_size=20, color=LATENT_BLUE),
            MathTex(r"\mathbf{v}\in\mathbb{R}^{E}", font_size=28, color=LATENT_BLUE),
        ).arrange(DOWN, buff=0.05).next_to(vector, DOWN, buff=0.15)
        arrow = Arrow(patch.get_right(), vector.get_left(), buff=0.18, color=LATENT_BLUE)
        patch_copy = patch.copy()
        self.add(patch_copy)
        self.play(GrowArrow(arrow), Transform(patch_copy, vector), FadeIn(vector_label), run_time=2.4)
        self.wait(1.8)
        self.play(Circumscribe(vector, color=LATENT_BLUE), run_time=1.5)
        self.wait(1.0)

        self.play(*[FadeOut(mob) for mob in (
            title, observation, grid, grid_label, patch, patch_label, patch_copy, vector_label, arrow
        )], run_time=1.2)
        self.clear()

        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-2, 2, 1],
            x_length=6.6,
            y_length=5.0,
            z_length=3.8,
            axis_config={"color": GREY_METAL, "stroke_width": 1.5},
        )
        projection_title = Text("Latent space — 3D projection", font_size=34, color=WHITE).to_edge(UP, buff=0.35)
        legend = VGroup(
            VGroup(Dot(color=KITCHEN_ORANGE), Text("block", font_size=20, color=KITCHEN_ORANGE)).arrange(RIGHT, buff=0.12),
            VGroup(Dot(color=OIL_YELLOW), Text("gripper", font_size=20, color=OIL_YELLOW)).arrange(RIGHT, buff=0.12),
            VGroup(Dot(color=LATENT_BLUE), Text("table", font_size=20, color=LATENT_BLUE)).arrange(RIGHT, buff=0.12),
        ).arrange(RIGHT, buff=0.45).to_edge(DOWN, buff=0.26)
        self.add_fixed_in_frame_mobjects(projection_title, legend)
        self.set_camera_orientation(phi=62 * DEGREES, theta=-68 * DEGREES, zoom=0.86)
        self.play(Create(axes), FadeIn(projection_title), FadeIn(legend), run_time=1.8)
        self.move_camera(
            phi=70 * DEGREES,
            theta=-52 * DEGREES,
            zoom=0.86,
            run_time=2.2,
        )

        cluster_specs = [
            (KITCHEN_ORANGE, np.array([1.55, 1.20, 0.60])),
            (OIL_YELLOW, np.array([-1.35, 1.10, 0.35])),
            (LATENT_BLUE, np.array([0.15, -1.45, -0.55])),
        ]
        clusters = VGroup()
        for cluster_index, (color, center) in enumerate(cluster_specs):
            for point_index in range(7):
                angle = TAU * point_index / 7 + 0.3 * cluster_index
                offset = np.array([
                    0.36 * np.cos(angle),
                    0.27 * np.sin(angle),
                    0.20 * ((point_index % 3) - 1),
                ])
                clusters.add(Dot3D(point=axes.c2p(*(center + offset)), radius=0.085, color=color))
        self.play(LaggedStart(*[GrowFromCenter(dot) for dot in clusters], lag_ratio=0.06), run_time=2.6)
        self.begin_ambient_camera_rotation(rate=0.07)
        self.wait(2.4)
        self.stop_ambient_camera_rotation()
        self.play(FadeOut(clusters), FadeOut(axes), FadeOut(projection_title), FadeOut(legend), run_time=1.4)
        self.clear()
        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES, zoom=1)

        tokens = self.token_row()
        token_label = MathTex(r"z_t \in \mathbb{R}^{N \times E}", color=LATENT_BLUE).next_to(tokens, UP, buff=0.42)
        caption = Text("one spatial token per patch", font_size=24, color=GREY_METAL).next_to(tokens, DOWN, buff=0.36)
        self.play(
            LaggedStart(*[FadeIn(token, shift=UP * 0.12) for token in tokens], lag_ratio=0.08),
            FadeIn(token_label),
            FadeIn(caption),
            run_time=2.2,
        )
        self.wait(2.5)
        self.play(FadeOut(VGroup(tokens, token_label, caption)), run_time=1.4)
        self.reset_stage()

    # -----------------------------------------------------------------
    # Narrative beat 3: action-conditioned causal ViT transition.
    # -----------------------------------------------------------------
    def beat_vit_transition(self):
        title = self.section_title("2.3", "The Engine of Imagination", LATENT_PURPLE)
        current = self.token_row().scale(0.72).shift(LEFT * 4.15 + DOWN * 0.25)
        current_label = MathTex(r"z_t", color=LATENT_BLUE).next_to(current, UP, buff=0.30)
        action_arrow = Arrow(LEFT * 0.75, RIGHT * 0.75, color=TARGET_GREEN, stroke_width=7)
        action = VGroup(
            action_arrow,
            MathTex(r"a_t", color=TARGET_GREEN).next_to(action_arrow, DOWN, buff=0.12),
        ).scale(0.75).next_to(current, DOWN, buff=0.65)
        transformer = self.model_block("Causal ViT", width=2.45, height=1.45, color=LATENT_PURPLE)
        transformer.shift(DOWN * 0.15)
        transformer_note = Text("action-conditioned", font_size=18, color=GREY_METAL).next_to(transformer, DOWN, buff=0.15)
        future = self.token_row(future=True).scale(0.72).shift(RIGHT * 4.15 + DOWN * 0.25)
        future_label = MathTex(r"z_{t+1}", color=TARGET_GREEN).next_to(future, UP, buff=0.30)

        self.play(FadeIn(title, shift=DOWN * 0.15), run_time=1.5)
        self.wait(1.0)
        self.play(
            LaggedStart(*[FadeIn(token) for token in current], lag_ratio=0.06),
            FadeIn(current_label),
            run_time=2.4,
        )
        self.wait(2.2)
        self.play(GrowArrow(action_arrow), Write(action[1]), run_time=1.8)
        self.wait(1.5)

        curves = VGroup()
        for index, token in enumerate(current):
            strong = index in (2, 3)
            curves.add(self.attention_curve(
                action_arrow.get_right(),
                token.get_top(),
                color=OIL_YELLOW if strong else LATENT_BLUE,
                opacity=0.95 if strong else 0.20,
                lift=0.55 + 0.07 * index,
            ))
        attention_label = Text("attention focuses on affected patches", font_size=21, color=OIL_YELLOW)
        attention_label.to_edge(DOWN, buff=0.35).shift(LEFT * 3.3)
        attention_label.add_background_rectangle(color=BG_DARK, opacity=0.92, buff=0.12)
        self.play(
            LaggedStart(*[Create(curve) for curve in curves], lag_ratio=0.06),
            FadeIn(attention_label),
            run_time=2.8,
        )
        self.wait(2.3)
        self.play(FadeIn(transformer, scale=0.92), FadeIn(transformer_note), run_time=2.0)
        self.wait(1.5)

        matrix = MathTex(r"W\,[z_t\,;\,a_t]", color=WHITE).scale(0.75).move_to(transformer)
        self.play(FadeOut(transformer[2]), FadeIn(matrix), run_time=1.8)
        self.wait(1.2)
        self.play(Indicate(matrix, color=OIL_YELLOW), run_time=1.4)
        self.wait(1.0)
        self.play(FadeOut(matrix), FadeIn(transformer[2]), run_time=1.4)

        state_path = Arrow(current.get_right(), transformer.get_left(), buff=0.18, color=LATENT_BLUE)
        action_path = Arrow(action.get_right(), transformer.get_bottom(), buff=0.18, color=TARGET_GREEN)
        path_out = Arrow(transformer.get_right(), future.get_left(), buff=0.18, color=TARGET_GREEN)
        self.play(
            FadeOut(curves),
            FadeOut(attention_label),
            GrowArrow(state_path),
            GrowArrow(action_path),
            run_time=2.0,
        )
        self.wait(1.4)

        predicted = current.copy()
        self.add(predicted)
        self.play(
            GrowArrow(path_out),
            Transform(predicted, future),
            FadeIn(future_label),
            run_time=3.0,
        )
        self.wait(2.0)
        self.play(Indicate(VGroup(predicted[2], predicted[3]), color=OIL_YELLOW, scale_factor=1.14), run_time=1.8)

        equation = MathTex(
            r"z_{t+1} = \operatorname{ViT}(z_t, a_t)",
            color=WHITE,
        ).scale(0.86)
        simplified = Text("simplified one-step view", font_size=18, color=GREY_METAL)
        equation_group = VGroup(equation, simplified).arrange(DOWN, buff=0.08)
        equation_group.to_edge(DOWN, buff=0.30)
        self.play(Write(equation), FadeIn(simplified), run_time=2.0)
        self.wait(3.0)
        self.play(FadeOut(VGroup(
            title, current, current_label, action, transformer, transformer_note,
            predicted, future_label, state_path, action_path, path_out, equation_group
        )), run_time=1.5)
        self.reset_stage()

    # -----------------------------------------------------------------
    # Narrative beat 4: optional decoder and fast latent rollouts.
    # -----------------------------------------------------------------
    def beat_missing_decoder(self):
        title = self.section_title("2.4", "The Optional Decoder", OIL_YELLOW)
        future = self.token_row(future=True).scale(0.78).shift(LEFT * 4.25 + DOWN * 0.1)
        future_label = MathTex(r"z_{t+1}", color=TARGET_GREEN).next_to(future, UP, buff=0.30)
        decoder = self.model_block("Decoder", width=2.35, height=1.45, color=KITCHEN_RED).shift(DOWN * 0.1)
        optional = Text("optional visualization only", font_size=19, color=GREY_METAL).next_to(decoder, DOWN, buff=0.18)
        preview, _ = self.observation(width=3.25, height=2.05)
        preview.shift(RIGHT * 4.55 + DOWN * 0.12)
        preview_label = Text("reconstructed pixels", font_size=20, color=KITCHEN_ORANGE).next_to(preview, DOWN, buff=0.15)
        route_a = Arrow(future.get_right(), decoder.get_left(), buff=0.20, color=KITCHEN_RED)
        route_b = Arrow(decoder.get_right(), preview.get_left(), buff=0.20, color=KITCHEN_RED)

        self.play(FadeIn(title, shift=DOWN * 0.15), run_time=1.5)
        self.wait(1.2)
        self.play(FadeIn(future), FadeIn(future_label), run_time=2.0)
        self.wait(1.0)
        self.play(GrowArrow(route_a), FadeIn(decoder), FadeIn(optional), run_time=2.3)
        self.wait(1.0)
        self.play(GrowArrow(route_b), FadeIn(preview), FadeIn(preview_label), run_time=2.2)
        self.wait(1.5)

        cross = Cross(decoder, stroke_color=KITCHEN_RED, stroke_width=8)
        not_required = Text("not required for training or planning", font_size=23, color=OIL_YELLOW)
        not_required.to_edge(DOWN, buff=0.32)
        self.play(Create(cross), FadeIn(not_required), run_time=1.8)
        self.wait(1.7)

        rng = np.random.default_rng(42)
        particles = VGroup(*[
            Dot(radius=0.035, color=KITCHEN_RED).move_to(
                decoder.get_center() + np.array([rng.uniform(-0.9, 0.9), rng.uniform(-0.5, 0.5), 0])
            )
            for _ in range(26)
        ])
        particle_targets = [
            particle.get_center() + np.array([rng.uniform(-1.3, 1.3), rng.uniform(-1.0, 1.0), 0])
            for particle in particles
        ]
        self.play(
            FadeOut(VGroup(decoder, cross, optional, preview, preview_label, route_a, route_b)),
            FadeIn(particles),
            run_time=1.0,
        )
        self.play(
            *[particle.animate.move_to(target).set_opacity(0) for particle, target in zip(particles, particle_targets)],
            FadeOut(not_required),
            run_time=1.6,
        )
        self.play(FadeOut(VGroup(future, future_label)), FadeOut(particles), run_time=1.0)

        current = self.token_row().scale(0.62).shift(LEFT * 4.1 + DOWN * 0.18)
        vit = self.model_block("Causal ViT", width=2.25, height=1.30, color=LATENT_PURPLE).shift(DOWN * 0.18)
        next_state = self.token_row(future=True).scale(0.62).shift(RIGHT * 4.1 + DOWN * 0.18)
        current_text = MathTex(r"z_t", color=LATENT_BLUE).next_to(current, UP, buff=0.25)
        next_text = MathTex(r"z_{t+1}", color=TARGET_GREEN).next_to(next_state, UP, buff=0.25)
        forward_1 = Arrow(current.get_right(), vit.get_left(), buff=0.18, color=LATENT_BLUE)
        forward_2 = Arrow(vit.get_right(), next_state.get_left(), buff=0.18, color=TARGET_GREEN)
        feedback = CurvedArrow(
            next_state.get_bottom() + DOWN * 0.08,
            current.get_bottom() + DOWN * 0.08,
            angle=-TAU / 5,
            color=OIL_YELLOW,
            stroke_width=3,
        )
        feedback_text = MathTex(r"z_{t+1}\rightarrow z_t", color=OIL_YELLOW).scale(0.68)
        infinity = MathTex(r"\infty", color=OIL_YELLOW).scale(0.92)
        loop_label = VGroup(feedback_text, infinity).arrange(RIGHT, buff=0.25)
        loop_label.next_to(feedback, DOWN, buff=0.05)

        self.play(
            FadeIn(current),
            FadeIn(current_text),
            FadeIn(vit),
            FadeIn(next_state),
            FadeIn(next_text),
            run_time=1.8,
        )
        self.wait(1.0)
        self.play(
            GrowArrow(forward_1),
            GrowArrow(forward_2),
            Create(feedback),
            FadeIn(loop_label),
            run_time=2.2,
        )
        self.wait(1.3)
        loop_path = VMobject().set_points_smoothly([
            current.get_center(),
            vit.get_center(),
            next_state.get_center(),
            feedback.get_bottom(),
            current.get_center(),
        ])
        pulses = VGroup(*[
            Dot(radius=0.09, color=color).move_to(current.get_center())
            for color in (LATENT_BLUE, TARGET_GREEN, OIL_YELLOW)
        ])
        self.add(pulses)
        pulse_animations = [
            Succession(
                Wait(index * 0.55),
                MoveAlongPath(pulse, loop_path, run_time=3.3, rate_func=linear),
                FadeOut(pulse, run_time=0.35),
            )
            for index, pulse in enumerate(pulses)
        ]
        self.play(AnimationGroup(*pulse_animations, lag_ratio=0), run_time=5.0)

        statement = Text("Predict features, not pixels.", font_size=40, color=WHITE, weight=BOLD)
        statement.to_edge(DOWN, buff=0.34)
        underline = Line(statement.get_left(), statement.get_right(), color=OIL_YELLOW, stroke_width=4)
        underline.next_to(statement, DOWN, buff=0.10)
        self.play(FadeOut(loop_label), FadeIn(statement, shift=UP * 0.12), Create(underline), run_time=1.8)
        self.play(Indicate(statement, color=OIL_YELLOW, scale_factor=1.04), run_time=1.3)
        self.wait(2.2)
        self.play(FadeOut(VGroup(
            title, current, current_text, vit, next_state, next_text,
            forward_1, forward_2, feedback, statement, underline
        )), run_time=1.5)
        self.reset_stage()


class Scene1_DINOv2Encoder(Part2Visuals, ThreeDScene):
    def construct(self):
        self.setup_part2()
        self.beat_dinov2_encoder()


class Scene2_PatchesAndVectors(Part2Visuals, ThreeDScene):
    def construct(self):
        self.setup_part2()
        self.beat_patches_and_vectors()


class Scene3_ViTTransition(Part2Visuals, ThreeDScene):
    def construct(self):
        self.setup_part2()
        self.beat_vit_transition()


class Scene4_MissingDecoder(Part2Visuals, ThreeDScene):
    def construct(self):
        self.setup_part2()
        self.beat_missing_decoder()


class LatentSpaceScene(Part2Visuals, ThreeDScene):
    """README-compatible aggregate render of all four Part 2 sections."""

    def construct(self):
        self.setup_part2()
        self.beat_dinov2_encoder()
        self.beat_patches_and_vectors()
        self.beat_vit_transition()
        self.beat_missing_decoder()
