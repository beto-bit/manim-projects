from manim import *
from numpy import ndarray

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
    def top_right(self) -> ndarray:
        return self.get_vertices()[0]

    @property
    def top_left(self) -> ndarray:
        return self.get_vertices()[1]

    @property
    def bottom_left(self) -> ndarray:
        return self.get_vertices()[2]

    @property
    def bottom_right(self) -> ndarray:
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


def point_and_tex(
    text: str,
    point: list | ndarray,
    direction = RIGHT,
    color=BLACK
):
    dot = Dot(point, color=color)
    dot_text = Tex(text).next_to(dot, direction).set_color(color)

    return VGroup(dot, dot_text)


def middle_point(p1: ndarray, p2: ndarray) -> ndarray:
    return Line(p1, p2).get_midpoint()


class Test(Scene):
    def construct(self):
        # Shapes
        trpzd = Trapezoid(3.3, 6, center=True, color=BLACK)
        triangle = trpzd.fitting_triangle(color=BLACK)

        # Point text
        p_point = point_and_tex('P', trpzd.top_left, LEFT + UP)
        q_point = point_and_tex('Q', trpzd.top_right, RIGHT)
        m_point = point_and_tex('M', trpzd.bottom_left, DOWN)
        n_point = point_and_tex('N', trpzd.bottom_right, DOWN)

        r_point = point_and_tex('R', triangle.get_vertices()[2], DOWN)

        juan = point_and_tex('Z', middle_point(trpzd.top_right, trpzd.top_left), UP)

        # Animations
        self.play(Write(VGroup(trpzd, p_point, q_point, m_point, n_point)))

        self.wait(1)
        self.play(Write(VGroup(triangle, r_point, juan)))

        self.wait(1)
