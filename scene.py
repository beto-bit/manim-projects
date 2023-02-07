from manim import *

config.background_color = "#ece6e2"

class Trapezoid(Polygon):
    def __init__(
        self,
        a: float,
        b: float,
        center=False,
        **kwargs
    ):
        self.a_length = a
        self.b_length = b
        self.base_length = a + b

        super().__init__(
            [a + b, b, 0],  # Top right
            [0, a, 0],      # Top left
            [0, 0, 0],      # Bottom left
            [a + b, 0, 0],  # Bottom right
            **kwargs
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


    def fitting_triangle(self, **kwargs) -> Polygon:
        middle = self.bottom_left + [self.b_length, 0, 0]

        return Polygon(
            self.top_right,
            self.top_left,
            middle,
            **kwargs
        )

    def enclosing_rectangle(self, **kwargs) -> Rectangle:
        return Rectangle(
            width=self.base_length,
            height=max(self.a_length, self.b_length),
            **kwargs
        ).move_to(self)


class Test(Scene):
    def construct(self):
        trapezoid = Trapezoid(3.3, 6, center=True, color=BLACK)
        triangle = trapezoid.fitting_triangle(color=BLACK)
        rectangle = trapezoid.enclosing_rectangle(color=BLACK)

        figure = VGroup(trapezoid, triangle, rectangle)

        self.play(Write(figure))

        self.wait(1)
