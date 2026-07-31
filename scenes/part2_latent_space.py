from manim import Scene, Text


class LatentSpaceScene(Scene):
    """Placeholder scene for Part 2: Latent Space."""

    def construct(self):
        title = Text("DINO-WM: Latent Space")
        self.play(title.animate.scale(1.2))
        self.wait()
