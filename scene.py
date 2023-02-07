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

def tex_at(
    text: str,
    point: list | ndarray,
    direction=RIGHT,
    color=BLACK
):
    return Tex(text).next_to(point, direction).set_color(color)

def point_and_tex(
    text: str,
    point: list | ndarray,
    direction=RIGHT,
    color=BLACK
):
    dot = Dot(point, color=color)
    dot_text = tex_at(text, point, direction, color)

    return VGroup(dot, dot_text)


def middle_point(p1: ndarray, p2: ndarray) -> ndarray:
    return Line(p1, p2).get_midpoint()


class Test(Scene):
    def construct(self):
        # Shapes
        trpzd = Trapezoid(3.3, 6, center=True, color=BLACK)
        triangle = trpzd.fitting_triangle(color=BLACK)

        # Vertex
        p_vertex = trpzd.top_left
        q_vertex = trpzd.top_right
        m_vertex = trpzd.bottom_left
        n_vertex = trpzd.bottom_right

        # Vertex text for trapezoid
        p_point = point_and_tex('P', p_vertex, LEFT + UP)
        q_point = point_and_tex('Q', q_vertex, RIGHT)
        m_point = point_and_tex('M', m_vertex, DOWN)
        n_point = point_and_tex('N', n_vertex, DOWN)

        trapezoid_tex = VGroup(p_point, q_point, m_point, n_point)

        # Vertex for center triangle
        r_vertex = triangle.get_vertices()[2]
        r_point = point_and_tex('R', r_vertex, DOWN)

        # Right triangle text
        a1_tex = tex_at('a', middle_point(q_vertex, n_vertex))
        b1_tex = tex_at('b', middle_point(r_vertex, n_vertex), DOWN * 0.35)
        c1_tex = tex_at('c', middle_point(r_vertex, q_vertex), LEFT)
        right_triangle_tex = VGroup(a1_tex, b1_tex, c1_tex)

        # Left triangle text
        a2_tex = tex_at('a', middle_point(m_vertex, r_vertex), DOWN * 0.65)
        b2_tex = tex_at('b', middle_point(m_vertex, p_vertex), LEFT)
        c2_tex = tex_at('c', middle_point(p_vertex, r_vertex), UP * 0.3 + RIGHT)
        left_triangle_tex = VGroup(a2_tex, b2_tex, c2_tex)


        # Animations
        self.play(Write(VGroup(trpzd, trapezoid_tex)))
        self.play(Write(VGroup(triangle, r_point, right_triangle_tex, left_triangle_tex)))

        self.wait(2)
