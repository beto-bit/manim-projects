from manim import *

class Trapezoid(Polygon):
    def __init__(
        self,
        a: int,
        b: int,
        center=False,
        **kwargs
    ):
        self.a_length = a
        self.b_length = b

        super().__init__(
            [a + b, b, 0],  # Top right
            [0, a, 0],      # Top left
            [0, 0, 0],      # Bottom left
            [a + b, 0, 0],  # Bottom right
        )

        if center:
            self.shift(DOWN * b / 2 + LEFT * (a + b) / 2)


class Test(Scene):
    def construct(self):
        trapezoid = Trapezoid(2, 6, center=True)


        self.play(Write(trapezoid))
        self.wait(1)

        pass