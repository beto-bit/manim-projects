from manim import *

def create_trapezoid(a: int, b: int, center=False) -> Polygon:
    trapezoid = Polygon(
        [a + b, b, 0],  # Top right
        [0, a, 0],      # Top left
        [0, 0, 0],      # Bottom left
        [a + b, 0, 0],  # Bottom right 
    )

    if not center:
        return trapezoid

    return trapezoid.shift(DOWN * b / 2 + LEFT * (a + b) / 2)


class Test(Scene):
    def construct(self):
        trapezoid = create_trapezoid(2, 6, center=True)

        self.play(Write(trapezoid))
        self.wait(1)

        pass