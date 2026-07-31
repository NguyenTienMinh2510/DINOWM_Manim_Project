from manim import Scene, Text


class ZeroShotScene(Scene):
    """Placeholder scene for Part 3: Zero-shot."""

    def construct(self):
        title = Text("DINO-WM: Zero-shot")
        self.play(title.animate.scale(1.2))
        self.wait()
