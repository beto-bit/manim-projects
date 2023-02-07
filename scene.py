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

    @property
    def top_right(self):
        return self.get_vertices()[0]

    @property
    def top_left(self):
        return self.get_vertices()[1]

    @property
    def bottom_left(self):
        return self.get_vertices()[2]

    @property
    def bottom_right(self):
        return self.get_vertices()[3]


    def fitting_triangle(self) -> Polygon:
        middle = self.bottom_left + [self.b_length, 0, 0]

        return Polygon(
            self.top_right,
            self.top_left,
            middle
        )


class Test(Scene):
    def construct(self):
        trapezoid = Trapezoid(2, 6, center=True)
        triangle = trapezoid.fitting_triangle()

        self.play(Write(trapezoid))
        self.play(Write(triangle))
        self.wait(1)

        pass