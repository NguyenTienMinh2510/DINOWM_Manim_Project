from manim import Scene, Text


class PixelSpaceScene(Scene):
    """Placeholder scene for Part 1: Pixel Space."""

    def construct(self):
        title = Text("DINO-WM: Pixel Space")
        self.play(title.animate.scale(1.2))
        self.wait()
