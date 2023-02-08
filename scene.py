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

def MathTex_at(
    text: str,
    point: list | ndarray,
    direction=RIGHT,
    color=BLACK
) -> MathTex:
    return MathTex(text).next_to(point, direction).set_color(color)

def point_and_MathTex(
    text: str,
    point: list | ndarray,
    direction=RIGHT,
    color=BLACK
):
    dot = Dot(point, color=color)
    dot_text = MathTex_at(text, point, direction, color)

    return VGroup(dot, dot_text)

def middle_point(p1: ndarray, p2: ndarray) -> ndarray:
    return Line(p1, p2).get_midpoint()

def angle_with_tex(
    mtex: MathTex,
    p1: ndarray,
    p2: ndarray,
    center: ndarray,
    radius=0.75,
    label_multiplier=1.5,
    color=BLACK,
    **kwargs
) -> VGroup:
    line1 = Line(center, p1)
    line2 = Line(center, p2)

    invisible_angle = Angle(
        line1,
        line2,
        radius=radius * label_multiplier,
        color=color,
        **kwargs
    )

    angle = Angle(
        line1,
        line2,
        radius=radius,
        color=color,
        **kwargs
    )

    return VGroup(
        angle,
        mtex.move_to(invisible_angle.point_from_proportion(0.5))
    )


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

        # Corner rect angles
        square1 = Square(0.5, color=BLACK).move_to(m_vertex).shift(0.25 * (RIGHT + UP))
        square2 = Square(0.5, color=BLACK).move_to(n_vertex).shift(0.25 * (LEFT + UP))

        # Vertex text for trapezoid
        p_point = point_and_MathTex('P', p_vertex, LEFT + UP)
        q_point = point_and_MathTex('Q', q_vertex, RIGHT + UP)
        m_point = point_and_MathTex('M', m_vertex, DOWN + LEFT)
        n_point = point_and_MathTex('N', n_vertex, DOWN + RIGHT)

        corner_angles = VGroup(square1, square2)
        trapezoid_tex = VGroup(p_point, q_point, m_point, n_point)


        # Vertex for center triangle
        r_vertex = triangle.get_vertices()[2]
        r_point = point_and_MathTex('R', r_vertex, DOWN)

        # Right triangle text
        a1_tex = MathTex_at('a', middle_point(q_vertex, n_vertex), RIGHT * 0.5)
        b1_tex = MathTex_at('b', middle_point(r_vertex, n_vertex), DOWN * 0.35)
        c1_tex = MathTex_at('c', middle_point(r_vertex, q_vertex), LEFT)
        right_triangle_tex = VGroup(a1_tex, b1_tex, c1_tex)

        # Left triangle text
        a2_tex = MathTex_at('a', middle_point(m_vertex, r_vertex), DOWN * 0.65)
        b2_tex = MathTex_at('b', middle_point(m_vertex, p_vertex), LEFT * 0.5)
        c2_tex = MathTex_at('c', middle_point(p_vertex, r_vertex), UP * 0.3 + RIGHT)
        left_triangle_tex = VGroup(a2_tex, b2_tex, c2_tex)


        # Angles
        alpha_tex = MathTex(r'\alpha', color=BLACK)
        beta_tex = MathTex(r'\beta', color=BLACK)

        triangles_angles = VGroup(
            angle_with_tex(alpha_tex, q_vertex, n_vertex, r_vertex, other_angle=True),    #Alpha right
            angle_with_tex(beta_tex, r_vertex, n_vertex, q_vertex),                       # Beta right

            angle_with_tex(alpha_tex.copy(), m_vertex, r_vertex, p_vertex),   # Alpha left
            angle_with_tex(beta_tex.copy(), p_vertex, m_vertex, r_vertex, label_multiplier=1.75),    # Beta left
        )

        all_figures = VGroup(
            trpzd,
            triangle,
            corner_angles,
            triangles_angles,
            right_triangle_tex,
            left_triangle_tex
        )

        # Animations
        # Initial things
        self.play(Write(VGroup(trpzd, trapezoid_tex, corner_angles)))
        self.wait(1)

        self.play(
            Write(VGroup(triangle, r_point, right_triangle_tex, left_triangle_tex)),
            FadeOut(trapezoid_tex)
        )
        self.wait(1)

        # Angles
        self.play(
            FadeOut(r_point),
            Write(triangles_angles),
        )

        # Shrink and move
        self.play(
            all_figures.animate.scale(0.5).move_to(LEFT * 4 + UP * 2)
        )

        self.wait(2)
