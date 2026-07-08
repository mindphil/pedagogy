from manim import *

config.background_color = WHITE

INK    = BLACK
ACCENT = RED_D      # new info / right-angle marks / the "look here" color
GHOST  = GREY_B     # dotted origin shapes (the square/equilateral behind examples)
BANK   = BLUE_D     # optional second accent for banked results (e.g., the ratio in the corner)
LEG = TEAL_D      # the two congruent legs / 45° sides
HYP = PURPLE_D    # the hypotenuse / 90° side
LONG = GOLD_E     # the long leg / 60° side  (teal stays short leg, purple stays hypotenuse)

Mobject.set_default(color=INK)
Text.set_default(color=INK)
MathTex.set_default(color=INK)

class TitlePage(Scene):
    """title page"""

    def construct(self):
        EQ_SIZE = 100
        LABEL_SIZE = 34

        sp = MathTex(r"\text{Special}", font_size=EQ_SIZE).set_color(ACCENT)
        r = MathTex(r"\text{Right}", font_size=EQ_SIZE)
        tr = MathTex(r"\text{Triangles}", font_size=EQ_SIZE).set_color(BANK)

        title = VGroup(sp, r, tr).arrange(RIGHT, buff=0.25)
        title.move_to(UP * 0.5)

        lb = MathTex(r"\text{Philip Umeadi}",
                     font_size=LABEL_SIZE)
        lb.next_to(title, DOWN, buff=0.6)

        self.add(title, lb)
        self.wait()



class LineRecap(Scene):
    """Scene 1: y = mx + b with each component labeled.
    STILL — final frame is the deliverable."""

    def construct(self):
        EQ_SIZE = 140      # tweak: equation size
        LABEL_SIZE = 34    # tweak: label size
        BUFF = 0.3         # tweak: brace distance from equation

        eq = MathTex("y", "=", "m", "x", "+", "b", font_size=EQ_SIZE)
        eq.move_to(ORIGIN)

        y_, m_, x_, b_ = eq[0], eq[2], eq[3], eq[5]
        m_.set_color(ACCENT)   # slope highlighted
        b_.set_color(BANK)     # bias highlighted

        def tag(part, text, direction, color=INK):
            brace = Brace(part, direction, buff=BUFF, color=color)
            label = Text(text, font_size=LABEL_SIZE, color=color)
            label.next_to(brace, direction, buff=0.15)
            return VGroup(brace, label)

        tags = VGroup(
            tag(y_, "dependent variable", DOWN),
            tag(m_, "slope", DOWN, ACCENT),
            tag(x_, "independent variable", UP),
            tag(b_, "y-intercept", DOWN, BANK),
        )

        self.add(eq, tags)
        self.wait()

class TwoWaysToALine(Scene):
    """Scene 2: LEFT — two points determine a line.
    RIGHT — a point + slope; line slides until pinned to the point.
    VIDEO — set 'Loop until Stopped' in PowerPoint."""

    def construct(self):
        M, B = 0.75, -1.0                     # tweak: the target line (both panels)
        P1 = (-2, M * -2 + B)                 # left panel: chosen points
        P2 = (2,  M *  2 + B)
        PIVOT = (-1, M * -1 + B)              # right panel: chosen point

        def make_plane():
            return NumberPlane(
                x_range=[-4, 4, 1], y_range=[-4, 4, 1],
                x_length=5.2, y_length=5.2,
                background_line_style={
                    "stroke_color": GREY_B, "stroke_width": 1, "stroke_opacity": 0.7,
                },
                axis_config={"color": INK, "stroke_width": 2, "include_ticks": False},
            )

        left, right = make_plane(), make_plane()
        VGroup(left, right).arrange(RIGHT, buff=0.9).to_edge(DOWN, buff=0.5)

        t_left = Text("two points", font_size=30).next_to(left, UP, buff=0.25)
        t_right = Text("a point and a slope", font_size=30).next_to(right, UP, buff=0.25)
        self.add(left, right, t_left, t_right)
        self.wait(0.5)

        # ---------- LEFT PANEL ----------
        d1 = Dot(left.c2p(*P1), color=ACCENT, radius=0.09)
        d2 = Dot(left.c2p(*P2), color=ACCENT, radius=0.09)
        line_L = left.plot(lambda x: M * x + B, x_range=[-4, 4],
                           color=INK, stroke_width=5)

        self.play(FadeIn(d1, scale=2))
        self.play(FadeIn(d2, scale=2))
        self.play(Create(line_L), run_time=1.5)
        self.wait(0.5)

        # ---------- RIGHT PANEL ----------
        pivot = Dot(right.c2p(*PIVOT), color=ACCENT, radius=0.09)
        self.play(FadeIn(pivot, scale=2))

        # slope indicator: run 1, rise m
        run = Line(right.c2p(*PIVOT), right.c2p(PIVOT[0] + 1, PIVOT[1]),
                   color=BANK, stroke_width=4)
        rise = Line(right.c2p(PIVOT[0] + 1, PIVOT[1]),
                    right.c2p(PIVOT[0] + 1, PIVOT[1] + M),
                    color=BANK, stroke_width=4)
        m_lbl = MathTex("m", color=BANK, font_size=40)
        m_lbl.next_to(rise, RIGHT, buff=0.12)

        self.play(Create(run), Create(rise), FadeIn(m_lbl))
        self.wait(0.5)

        # sliding line: same slope, wandering bias, clamped to the grid
        b_tr = ValueTracker(B + 2.2)          # tweak: starting offset

        def sliding_line():
            b = b_tr.get_value()
            x_lo = max(-4, (-4 - b) / M)
            x_hi = min(4, (4 - b) / M)
            return right.plot(lambda x: M * x + b, x_range=[x_lo, x_hi],
                              color=INK, stroke_width=5)

        line_R = always_redraw(sliding_line)
        self.play(Create(line_R), run_time=0.8)

        self.play(b_tr.animate.set_value(B - 1.8), run_time=1.4,
                  rate_func=smooth)
        self.play(b_tr.animate.set_value(B + 1.0), run_time=1.2,
                  rate_func=smooth)
        self.play(b_tr.animate.set_value(B), run_time=1.0,
                  rate_func=rate_functions.ease_out_back)  # little settle
        self.play(Flash(pivot, color=ACCENT, flash_radius=0.35))
        self.wait(1.5)

class PythBase(Scene):
    """Scenes 2a/2b: non-special right triangle, legs 3 and 4,
    hypotenuse unknown. Only the 90° angle is marked.
    STILL x2 — subclasses toggle the solution."""

    SHOW_SOLUTION = False

    # ---- tweak knobs ----
    UNIT = 0.85            # grid-units → screen-units scale
    TRI_SHIFT = LEFT * 3.2 + DOWN * 1.2
    SIDE_SIZE = 60         # side-label font size
    WORK_SIZE = 54         # math-work font size

    def construct(self):
        U = self.UNIT
        # right angle at origin corner; legs 4 (base) and 3 (vertical)
        A = ORIGIN
        B = RIGHT * 4 * U
        C = UP * 3 * U

        tri = Polygon(A, B, C, color=INK, stroke_width=6, fill_opacity=0)

        ra = RightAngle(Line(A, B), Line(A, C),
                        length=0.35, color=ACCENT, stroke_width=5)

        base_lbl = MathTex("4", font_size=self.SIDE_SIZE)
        base_lbl.next_to(Line(A, B).get_center(), DOWN, buff=0.3)

        leg_lbl = MathTex("3", font_size=self.SIDE_SIZE)
        leg_lbl.next_to(Line(A, C).get_center(), LEFT, buff=0.3)

        hyp_mid = Line(B, C).get_center()
        hyp_dir = normalize(UP + RIGHT)          # outward from the hypotenuse
        hyp_lbl = MathTex("?", font_size=self.SIDE_SIZE, color=ACCENT)
        if self.SHOW_SOLUTION:
            hyp_lbl = MathTex("5", font_size=self.SIDE_SIZE, color=ACCENT)
        hyp_lbl.move_to(hyp_mid + hyp_dir * 0.45)

        figure = VGroup(tri, ra, base_lbl, leg_lbl, hyp_lbl)
        figure.shift(self.TRI_SHIFT)
        self.add(figure)

        if self.SHOW_SOLUTION:
            work = VGroup(
                MathTex("a^2 + b^2 = c^2", font_size=self.WORK_SIZE),
                MathTex("3^2 + 4^2 = c^2", font_size=self.WORK_SIZE),
                MathTex("9 + 16 = 25 = c^2", font_size=self.WORK_SIZE),
                MathTex("c = \\sqrt{25} = 5", font_size=self.WORK_SIZE,
                        color=ACCENT),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
            work.to_edge(RIGHT, buff=1.0)
            self.add(work)

        self.wait()


class PythSetup(PythBase):
    SHOW_SOLUTION = False


class PythSolved(PythBase):
    SHOW_SOLUTION = False

class OneSideStuck(Scene):
    """Scene 3: same triangle, but now only the base (4) and the
    right angle are known. Question marks on the other two sides.
    STILL — the 'stuck' frame."""

    # ---- tweak knobs (kept identical to PythBase) ----
    UNIT = 0.85
    TRI_SHIFT = LEFT * 3.2 + DOWN * 1.2
    SIDE_SIZE = 60

    def construct(self):
        U = self.UNIT
        A = ORIGIN
        B = RIGHT * 4 * U
        C = UP * 3 * U

        tri = Polygon(A, B, C, color=INK, stroke_width=6)
        ra = RightAngle(Line(A, B), Line(A, C),
                        length=0.35, color=ACCENT, stroke_width=5)

        base_lbl = MathTex("4", font_size=self.SIDE_SIZE)
        base_lbl.next_to(Line(A, B).get_center(), DOWN, buff=0.3)

        leg_q = MathTex("?", font_size=self.SIDE_SIZE, color=ACCENT)
        leg_q.next_to(Line(A, C).get_center(), LEFT, buff=0.3)

        hyp_q = MathTex("?", font_size=self.SIDE_SIZE, color=ACCENT)
        hyp_q.move_to(Line(B, C).get_center() + normalize(UP + RIGHT) * 0.45)

        figure = VGroup(tri, ra, base_lbl, leg_q, hyp_q)
        figure.shift(self.TRI_SHIFT)
        self.add(figure)

        # the doomed attempt — tweak or delete
        # work = VGroup(
        #     MathTex("a^2 + b^2 = c^2", font_size=54),
        #     MathTex("a^2 + 4^2 = c^2", font_size=54),
        #     MathTex("a^2 + 16 = c^2\\,\\,?", font_size=54, color=ACCENT),
        # ).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        # work.to_edge(RIGHT, buff=1.0)
        # self.add(work)

        self.wait()

class AngleAndSideDemo(Scene):
    """Scene 4: VIDEO, loop in PowerPoint.
    Beat 1 — angle grows/shrinks, opposite side responds (shape changes).
    Beat 2 — side grows/shrinks, whole triangle scales (size changes)."""

    # ---- tweak knobs ----
    U = 0.9                  # screen scale
    BASE = 4                 # base length in grid units
    THETA0 = 35 * DEGREES    # resting angle
    ANCHOR = LEFT * 3.4 + DOWN * 2.0   # fixed right-angle corner

    def construct(self):
        theta = ValueTracker(self.THETA0)   # angle at B
        s = ValueTracker(1.0)               # scale factor

        def verts():
            b = self.BASE * s.get_value() * self.U
            h = self.BASE * np.tan(theta.get_value()) * s.get_value() * self.U
            A = self.ANCHOR                 # right angle here
            B = A + RIGHT * b
            C = A + UP * h
            return A, B, C

        def make_tri():
            A, B, C = verts()
            return Polygon(A, B, C, color=INK, stroke_width=6)

        def make_ra():
            A, B, C = verts()
            return RightAngle(Line(A, B), Line(A, C),
                              length=0.3, color=INK, stroke_width=4)

        def make_arc():
            A, B, C = verts()
            r = 0.7 * s.get_value()          # tweak: scale arc with triangle
            return Angle(Line(B, C), Line(B, A), radius=r,
                         color=ACCENT, stroke_width=5)

        def make_opp():
            A, B, C = verts()
            return Line(A, C, color=ACCENT, stroke_width=7)

        tri = always_redraw(make_tri)
        ra = always_redraw(make_ra)
        arc = always_redraw(make_arc)
        opp = always_redraw(make_opp)

        caption = Text("changing an angle changes the shape",
                       font_size=36).to_edge(UP, buff=0.5)

        self.add(tri, ra)
        self.play(FadeIn(caption))
        self.play(Create(arc), run_time=0.6)
        self.add(opp)

        # ---- beat 1: angle oscillates, opposite side responds ----
        self.play(theta.animate.set_value(55 * DEGREES), run_time=1.6,
                  rate_func=smooth)
        self.play(theta.animate.set_value(18 * DEGREES), run_time=1.8,
                  rate_func=smooth)
        self.play(theta.animate.set_value(self.THETA0), run_time=1.2,
                  rate_func=smooth)
        self.wait(0.4)

        # ---- reset styling for beat 2 ----
        caption2 = Text("changing a side changes the size",
                        font_size=36).to_edge(UP, buff=0.5)
        self.remove(opp)

        def make_base():
            A, B, C = verts()
            return Line(A, B, color=BANK, stroke_width=7)

        base_hl = always_redraw(make_base)
        self.play(FadeOut(caption), FadeIn(caption2), FadeIn(base_hl))

        # ---- beat 2: side oscillates, triangle scales proportionally ----
        self.play(s.animate.set_value(1.45), run_time=1.6, rate_func=smooth)
        self.play(s.animate.set_value(0.65), run_time=1.8, rate_func=smooth)
        self.play(s.animate.set_value(1.0), run_time=1.2, rate_func=smooth)
        self.wait(0.8)

class MeetTheSpecials(Scene):
    """Scene 5: the two special right triangles side by side,
    interior angles labeled, NO side lengths yet.
    STILL — the introduction frame."""

    # ---- tweak knobs ----
    U = 2.15              # overall scale of both triangles
    GAP = 2.4             # horizontal gap between the two figures
    ANGLE_SIZE = 44       # angle-label font size
    NAME_SIZE = 0        # name font size
    ARC_R = 0.55          # radius of angle arcs

    def construct(self):
        U = self.U

        # ================= 45-45-90 =================
        # right angle at bottom-right, equal legs
        A1 = ORIGIN                    # 45° (left)
        B1 = RIGHT * 2 * U             # 90°
        C1 = RIGHT * 2 * U + UP * 2 * U  # 45° (top)

        t45 = Polygon(A1, B1, C1, color=INK, stroke_width=6)
        ra45 = RightAngle(Line(B1, A1), Line(B1, C1),
                          length=0.32, color=ACCENT, stroke_width=5)

        arc_a1 = Angle(Line(A1, B1), Line(A1, C1), radius=self.ARC_R,
                       color=INK, stroke_width=4)
        arc_c1 = Angle(Line(C1, A1), Line(C1, B1), radius=self.ARC_R,
                       color=INK, stroke_width=4)

        lbl_a1 = MathTex("45^\\circ", font_size=self.ANGLE_SIZE)
        lbl_a1.move_to(A1 + normalize(RIGHT * 2 + UP * 0.9) * 1.05)
        lbl_c1 = MathTex("45^\\circ", font_size=self.ANGLE_SIZE)
        lbl_c1.move_to(C1 + normalize(DOWN * 2 + LEFT * 0.9) * 1.05)
        lbl_b1 = MathTex("90^\\circ", font_size=self.ANGLE_SIZE, color=ACCENT)
        lbl_b1.move_to(B1 + normalize(UP * 0.9 + LEFT * 0.9) * 0.95)

        # congruence ticks on the two equal legs (the "perforated" convention)
        def tick(line, color=INK):
            m = line.get_center()
            d = normalize(line.get_end() - line.get_start())
            n = rotate_vector(d, PI / 2)
            return Line(m - n * 0.12, m + n * 0.12,
                        color=color, stroke_width=5)

        tick1 = tick(Line(A1, B1))
        tick2 = tick(Line(B1, C1))

        g45 = VGroup(t45, ra45, arc_a1, arc_c1,
                     lbl_a1, lbl_b1, lbl_c1, tick1, tick2)
        name45 = Text("45-45-90", font_size=self.NAME_SIZE)
        name45.next_to(g45, DOWN, buff=0.5)
        fig45 = VGroup(g45, name45)

        # ================= 30-60-90 =================
        # right angle at bottom-right; base sqrt(3), height 1, correct shape
        A2 = ORIGIN                          # 30° (left)
        B2 = RIGHT * np.sqrt(3) * 1.35 * U   # 90°
        C2 = B2 + UP * 1.35 * U              # 60° (top)

        t3060 = Polygon(A2, B2, C2, color=INK, stroke_width=6)
        ra3060 = RightAngle(Line(B2, A2), Line(B2, C2),
                            length=0.32, color=ACCENT, stroke_width=5)

        arc_a2 = Angle(Line(A2, B2), Line(A2, C2), radius=self.ARC_R + 0.15,
                       color=INK, stroke_width=4)
        arc_c2 = Angle(Line(C2, A2), Line(C2, B2), radius=self.ARC_R,
                       color=INK, stroke_width=4)

        lbl_a2 = MathTex("30^\\circ", font_size=self.ANGLE_SIZE)
        lbl_a2.move_to(A2 + normalize(RIGHT * 2.4 + UP * 0.55) * 1.25)
        lbl_c2 = MathTex("60^\\circ", font_size=self.ANGLE_SIZE)
        lbl_c2.move_to(C2 + normalize(DOWN * 1.5 + LEFT * 0.55) * 0.95)
        lbl_b2 = MathTex("90^\\circ", font_size=self.ANGLE_SIZE, color=ACCENT)
        lbl_b2.move_to(B2 + normalize(UP * 0.9 + LEFT * 0.9) * 0.95)

        g3060 = VGroup(t3060, ra3060, arc_a2, arc_c2,
                       lbl_a2, lbl_b2, lbl_c2)
        name3060 = Text("30-60-90", font_size=self.NAME_SIZE)
        name3060.next_to(g3060, DOWN, buff=0.5)
        fig3060 = VGroup(g3060, name3060)

        # ================= layout =================
        pair = VGroup(fig45, fig3060).arrange(RIGHT, buff=self.GAP)
        pair.move_to(ORIGIN).shift(DOWN * 0.2)
        self.add(pair)

        self.wait()

class SquareDerivationBase(Scene):
    """Shared geometry for scenes 6a-6c. The square lives in the same
    position in every frame so slide advances read as continuous."""

    # ---- tweak knobs ----
    S = 2.6                          # square side length on screen
    SQ_SHIFT = LEFT * 3.0 + DOWN * 0.4   # square position (6a, 6b)
    SIDE_SIZE = 56                   # side-label font size
    ANGLE_SIZE = 40                  # angle-label font size

    def square_pts(self):
        s = self.S
        bl = self.SQ_SHIFT + LEFT * s / 2 + DOWN * s / 2
        return {
            "bl": bl,
            "br": bl + RIGHT * s,
            "tr": bl + RIGHT * s + UP * s,
            "tl": bl + UP * s,
        }

    def make_square(self, color=INK, dashed=False):
        p = self.square_pts()
        sq = Polygon(p["bl"], p["br"], p["tr"], p["tl"],
                     color=color, stroke_width=6)
        if dashed:
            sq = DashedVMobject(sq, num_dashes=40)
        return sq

    def side_labels(self):
        p = self.square_pts()
        lbls = VGroup(
            MathTex("1", font_size=self.SIDE_SIZE).next_to(
                Line(p["bl"], p["br"]).get_center(), DOWN, buff=0.25),
            MathTex("1", font_size=self.SIDE_SIZE).next_to(
                Line(p["br"], p["tr"]).get_center(), RIGHT, buff=0.25),
            MathTex("1", font_size=self.SIDE_SIZE).next_to(
                Line(p["tr"], p["tl"]).get_center(), UP, buff=0.25),
            MathTex("1", font_size=self.SIDE_SIZE).next_to(
                Line(p["tl"], p["bl"]).get_center(), LEFT, buff=0.25),
        )
        return lbls

    def corner_marks(self, corners=("bl", "br", "tr", "tl")):
        p = self.square_pts()
        # inward direction pairs for each corner's right-angle mark
        arms = {
            "bl": (p["br"], p["tl"]),
            "br": (p["bl"], p["tr"]),
            "tr": (p["tl"], p["br"]),
            "tl": (p["tr"], p["bl"]),
        }
        marks = VGroup()
        for c in corners:
            a, b = arms[c]
            marks.add(RightAngle(Line(p[c], a), Line(p[c], b),
                                 length=0.28, color=ACCENT, stroke_width=4))
        return marks


class UnitSquare(SquareDerivationBase):
    """Scene 6a: the unit square. Sides all 1, right angles marked.
    STILL."""

    def construct(self):
        self.add(self.make_square(), self.side_labels(), self.corner_marks())

        caption = Text("side lengths 1, every angle 90°", font_size=36)
        caption.to_edge(UP, buff=0.5)
        self.add(caption)
        self.wait()


class SquareCut(SquareDerivationBase):
    """Scene 6b: the diagonal cut. Two 45s appear where the corners
    split; the lower triangle is emphasized. STILL."""

    def construct(self):
        p = self.square_pts()
        self.add(self.make_square(), self.side_labels())
        # right-angle marks only on the two corners the diagonal misses
        self.add(self.corner_marks(corners=("br", "tl")))

        # the cut
        diag = Line(p["bl"], p["tr"], color=ACCENT, stroke_width=6)
        self.add(diag)

        # emphasize the lower-right triangle
        lower = Polygon(p["bl"], p["br"], p["tr"],
                        stroke_width=0, fill_color=ACCENT, fill_opacity=0.1)
        self.add(lower)

        # split corners: 45° on the lower triangle's side of the diagonal
        arc_bl = Angle(Line(p["bl"], p["br"]), Line(p["bl"], p["tr"]),
                       radius=0.5, color=INK, stroke_width=4)
        lbl_bl = MathTex("45^\\circ", font_size=self.ANGLE_SIZE)
        lbl_bl.move_to(p["bl"] + normalize(RIGHT * 2 + UP * 0.85) * 0.95)

        arc_tr = Angle(Line(p["tr"], p["bl"]), Line(p["tr"], p["br"]),
                       radius=0.5, color=INK, stroke_width=4)
        lbl_tr = MathTex("45^\\circ", font_size=self.ANGLE_SIZE)
        lbl_tr.move_to(p["tr"] + normalize(LEFT * 2 + DOWN * 0.85) * 0.95)

        self.add(arc_bl, lbl_bl, arc_tr, lbl_tr)

        caption = Text("cut along the diagonal: 90° splits into 45° + 45°",
                       font_size=36)
        caption.to_edge(UP, buff=0.5)
        self.add(caption)
        self.wait()


class FortyFiveDerived(SquareDerivationBase):
    """Scene 6c: extracted 45-45-90, color-coded. Ghost square behind,
    Pythagorean work right, ratio banked top-left. STILL."""

    WORK_SIZE = 50

    def construct(self):
        p = self.square_pts()

        ghost_sq = self.make_square(color=GHOST, dashed=False)
        ghost_diag = DashedLine(p["bl"], p["tr"], color=GHOST,
                                stroke_width=4)
        self.add(ghost_sq, ghost_diag)

        STEP = RIGHT * 0
        A = p["bl"] + STEP
        B = p["br"] + STEP
        C = p["tr"] + STEP

        tri = Polygon(A, B, C, color=INK, stroke_width=6)
        ra = RightAngle(Line(B, A), Line(B, C),
                        length=0.28, color=ACCENT, stroke_width=5)

        base_lbl = MathTex("1", font_size=self.SIDE_SIZE, color=LEG)
        base_lbl.next_to(Line(A, B).get_center(), DOWN, buff=0.25)
        leg_lbl = MathTex("1", font_size=self.SIDE_SIZE, color=LEG)
        leg_lbl.next_to(Line(B, C).get_center(), RIGHT, buff=0.25)
        hyp_lbl = MathTex("\\sqrt{2}", font_size=self.SIDE_SIZE, color=HYP)
        hyp_lbl.move_to(Line(A, C).get_center() +
                        normalize(UP + LEFT) * 0.45)

        arc_a = Angle(Line(A, B), Line(A, C), radius=0.5,
                      color=INK, stroke_width=4)
        lbl_a = MathTex("45^\\circ", font_size=self.ANGLE_SIZE)
        lbl_a.move_to(A + normalize(RIGHT * 2 + UP * 0.85) * 0.95)
        arc_c = Angle(Line(C, A), Line(C, B), radius=0.5,
                      color=INK, stroke_width=4)
        lbl_c = MathTex("45^\\circ", font_size=self.ANGLE_SIZE)
        lbl_c.move_to(C + normalize(LEFT * .35 + DOWN * 0.85) * 0.95)

        self.add(tri, ra, base_lbl, leg_lbl, hyp_lbl,
                 arc_a, lbl_a, arc_c, lbl_c)

        # Pythagorean work — the c-line lands in HYP color
        work = VGroup(
            MathTex("a^2 + b^2 = c^2", font_size=self.WORK_SIZE),
            MathTex("1^2 + 1^2 = c^2", font_size=self.WORK_SIZE),
            MathTex("c^2 = 2", font_size=self.WORK_SIZE),
            MathTex("c = \\sqrt{2}", font_size=self.WORK_SIZE, color=HYP),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        work.to_edge(RIGHT, buff=0.9).shift(DOWN * 0.4)
        self.add(work)

        # color-coded banked ratio
        bank = MathTex("1", ":", "1", ":", "\\sqrt{2}", font_size=64)
        bank[0].set_color(LEG)
        bank[2].set_color(LEG)
        bank[4].set_color(HYP)
        bank.to_corner(UL, buff=0.6)
        self.add(bank, SurroundingRectangle(bank, color=INK, buff=0.25,
                                            corner_radius=0.1,
                                            stroke_width=3))
        self.wait()

class FortyFiveExampleBase(Scene):
    """Scenes 7a-7c: 45-45-90 examples, unsolved. Given side labeled,
    question marks on the other two sides. Color-coded: LEG ties the
    ratio's 1s to the legs, HYP ties sqrt(2) to the hypotenuse.
    Ghost square behind the triangle. Banked ratio top-left. STILL x3."""

    GIVEN = "1"          # overridden per example
    GIVEN_SIDE = "base"  # "base" | "leg" | "hyp" — where the given goes
    S = 2.2              # screen size of the square/legs — overridden

    # ---- tweak knobs ----
    SHIFT = LEFT * 2.6 + DOWN * 0.6   # figure position
    SIDE_SIZE = 60
    ANGLE_SIZE = 38
    SHOW_TICKS = False                 # congruence ticks on the two legs

    def construct(self):
        s = self.S
        bl = self.SHIFT + LEFT * s / 2 + DOWN * s / 2
        br = bl + RIGHT * s
        tr = br + UP * s
        tl = bl + UP * s

        # ghost square + its unused half
        ghost = DashedVMobject(
            Polygon(bl, br, tr, tl, color=GHOST, stroke_width=5),
            num_dashes=40)
        self.add(ghost)

        # the triangle itself
        tri = Polygon(bl, br, tr, color=INK, stroke_width=6)
        ra = RightAngle(Line(br, bl), Line(br, tr),
                        length=0.28, color=ACCENT, stroke_width=5)

        # ---- side labels: given on chosen side, ? on the other two ----
        # every label (given or ?) wears its side's role color
        base_pt = Line(bl, br).get_center()
        leg_pt = Line(br, tr).get_center()
        hyp_pt = Line(bl, tr).get_center()

        given_color = HYP if self.GIVEN_SIDE == "hyp" else LEG
        given = MathTex(self.GIVEN, font_size=self.SIDE_SIZE,
                        color=given_color)
        q_base = MathTex("?", font_size=self.SIDE_SIZE, color=LEG)
        q_leg = MathTex("?", font_size=self.SIDE_SIZE, color=LEG)
        q_hyp = MathTex("?", font_size=self.SIDE_SIZE, color=HYP)

        if self.GIVEN_SIDE == "base":
            base_lbl, leg_lbl, hyp_lbl = given, q_leg, q_hyp
        elif self.GIVEN_SIDE == "leg":
            base_lbl, leg_lbl, hyp_lbl = q_base, given, q_hyp
        else:  # "hyp"
            base_lbl, leg_lbl, hyp_lbl = q_base, q_leg, given

        base_lbl.next_to(base_pt, DOWN, buff=0.3)
        leg_lbl.next_to(leg_pt, RIGHT, buff=0.3)
        hyp_lbl.move_to(hyp_pt + normalize(UP + LEFT) * 0.5)

        # interior angles
        arc_bl = Angle(Line(bl, br), Line(bl, tr), radius=0.45,
                       color=INK, stroke_width=4)
        lbl_bl = MathTex("45^\\circ", font_size=self.ANGLE_SIZE)
        lbl_bl.move_to(bl + normalize(RIGHT * 2 + UP * 0.85) * 0.9)

        arc_tr = Angle(Line(tr, bl), Line(tr, br), radius=0.45,
                       color=INK, stroke_width=4)
        lbl_tr = MathTex("45^\\circ", font_size=self.ANGLE_SIZE)
        lbl_tr.move_to(tr + normalize(LEFT * 2 + DOWN * 0.85) * 0.9)

        self.add(tri, ra, base_lbl, leg_lbl, hyp_lbl,
                 arc_bl, lbl_bl, arc_tr, lbl_tr)

        if self.SHOW_TICKS:
            for seg in (Line(bl, br), Line(br, tr)):
                m = seg.get_center()
                d = normalize(seg.get_end() - seg.get_start())
                n = rotate_vector(d, PI / 2)
                self.add(Line(m - n * 0.12, m + n * 0.12,
                              color=INK, stroke_width=5))

        # standing reference: color-coded banked ratio, same corner as 6c
        bank = MathTex("1", ":", "1", ":", "\\sqrt{2}", font_size=64)
        bank[0].set_color(LEG)
        bank[2].set_color(LEG)
        bank[4].set_color(HYP)
        bank.to_corner(UL, buff=0.6)
        self.add(bank, SurroundingRectangle(bank, color=INK, buff=0.25,
                                            corner_radius=0.1,
                                            stroke_width=3))
        self.wait()


class FortyFive_Ex1(FortyFiveExampleBase):
    GIVEN = "\\sqrt{2}"
    GIVEN_SIDE = "hyp"
    S = 3.8


class FortyFive_Ex2(FortyFiveExampleBase):
    GIVEN = "2"
    GIVEN_SIDE = "base"
    S = 3.8


class FortyFive_ExX(FortyFiveExampleBase):
    GIVEN = "x"
    GIVEN_SIDE = "leg"
    S = 3.8

class FortyFive_Ratio(Scene):
    """Scene 8: the three solved examples side by side -> same ratio,
    plus the x/÷ sqrt(2) arrow diagram. STILL."""

    SHOW_EXAMPLES = False    # False -> arrow diagram only, centered

    # ---- tweak knobs ----
    MINI_S = 1.35           # size of each mini triangle
    MINI_LBL = 42           # mini side-label font size
    ROW_BUFF = 2.0          # gap between mini triangles
    NODE_SIZE = 84          # 45/90 node font size
    OP_SIZE = 56            # x sqrt2 / ÷ sqrt2 font size
    NODE_GAP = 4.2          # horizontal distance between nodes

    def mini(self, base_s, leg_s, hyp_s):
        """A small solved 45-45-90 with color-coded labels."""
        s = self.MINI_S
        bl, br, tr = ORIGIN, RIGHT * s, RIGHT * s + UP * s
        tri = Polygon(bl, br, tr, color=INK, stroke_width=5)
        ra = RightAngle(Line(br, bl), Line(br, tr),
                        length=0.2, color=ACCENT, stroke_width=4)
        base = MathTex(base_s, font_size=self.MINI_LBL, color=LEG)
        base.next_to(Line(bl, br).get_center(), DOWN, buff=0.2)
        leg = MathTex(leg_s, font_size=self.MINI_LBL, color=LEG)
        leg.next_to(Line(br, tr).get_center(), RIGHT, buff=0.2)
        hyp = MathTex(hyp_s, font_size=self.MINI_LBL, color=HYP)
        hyp.move_to(Line(bl, tr).get_center() +
                    normalize(UP + LEFT) * 0.42)
        return VGroup(tri, ra, base, leg, hyp)

    def construct(self):
        # ---- top: the three solved examples, centered ----
        if self.SHOW_EXAMPLES:
            row = VGroup(
                self.mini("1", "1", "\\sqrt{2}"),
                self.mini("2", "2", "2\\sqrt{2}"),
                self.mini("x", "x", "x\\sqrt{2}"),
            ).arrange(RIGHT, buff=self.ROW_BUFF, aligned_edge=DOWN)
            row.to_edge(UP, buff=0.9)
            self.add(row)

        # ---- bottom: the arrow diagram ----
        n45 = MathTex("45^\\circ", font_size=self.NODE_SIZE, color=LEG)
        n90 = MathTex("90^\\circ", font_size=self.NODE_SIZE, color=HYP)
        n45.move_to(LEFT * self.NODE_GAP / 2)
        n90.move_to(RIGHT * self.NODE_GAP / 2)
        diagram = VGroup(n45, n90)

        top_arrow = CurvedArrow(
            n45.get_top() + UP * 0.15 + RIGHT * 0.2,
            n90.get_top() + UP * 0.15 + LEFT * 0.2,
            angle=-TAU / 8, color=INK, stroke_width=5,
            tip_length=0.25)
        op_mult = MathTex("\\times \\sqrt{2}", font_size=self.OP_SIZE)
        op_mult.next_to(top_arrow, UP, buff=0.2)

        bot_arrow = CurvedArrow(
            n90.get_bottom() + DOWN * 0.15 + LEFT * 0.2,
            n45.get_bottom() + DOWN * 0.15 + RIGHT * 0.2,
            angle=-TAU / 8, color=INK, stroke_width=5,
            tip_length=0.25)
        op_div = MathTex("\\div \\sqrt{2}", font_size=self.OP_SIZE)
        op_div.next_to(bot_arrow, DOWN, buff=0.2)

        diagram.add(top_arrow, op_mult, bot_arrow, op_div)

        if self.SHOW_EXAMPLES:
            diagram.to_edge(DOWN, buff=1.2)
        else:
            diagram.move_to(ORIGIN)
        self.add(diagram)

        # heuristic caption — delete if it lives in your narration
        # heur = Text("longer side: multiply   ·   shorter side: divide",
        #             font_size=32, slant=ITALIC)
        # heur.next_to(diagram, DOWN, buff=0.4)
        # if heur.get_bottom()[1] < -3.8:      # keep on screen
        #     heur.next_to(diagram, DOWN, buff=0.2)
        # self.add(heur)
        # self.wait()

class SAT4545Base(Scene):
    """Scene 12: capstone 45-45-90 problem. B is the circle's center,
    AC = 16. Find the area of triangle ABC.
    Setup frame gives NOTHING away — no 45s, no tick marks.
    Identified frame reveals the radius argument. STILL x2."""

    SHOW_IDENTIFICATION = False

    # ---- tweak knobs ----
    R = 2.2                    # circle radius on screen (shrunk for header room)
    CIRC_SHIFT = LEFT * 2.0 + DOWN * 1.0
    LBL_SIZE = 48              # vertex letters
    SIDE_SIZE = 54
    Q_SIZE = 44                # question text size

    def construct(self):
        O = self.CIRC_SHIFT
        circle = Circle(radius=self.R, color=INK, stroke_width=5)
        circle.move_to(O)

        # B at center, A on circle (up), C on circle (right)
        B = O
        A = O + UP * self.R
        C = O + RIGHT * self.R

        tri = Polygon(A, B, C, color=INK, stroke_width=6)
        ra = RightAngle(Line(B, A), Line(B, C),
                        length=0.3, color=ACCENT, stroke_width=5)

        lbl_A = MathTex("A", font_size=self.LBL_SIZE)
        lbl_A.next_to(A, UP + LEFT * 0.3, buff=0.15)
        lbl_B = MathTex("B", font_size=self.LBL_SIZE)
        lbl_B.next_to(B, DOWN + LEFT * 0.3, buff=0.15)
        lbl_C = MathTex("C", font_size=self.LBL_SIZE)
        lbl_C.next_to(C, RIGHT, buff=0.15)

        # the given: AC = 16 on the hypotenuse (outward, down-right of midpoint)
        hyp_lbl = MathTex("16", font_size=self.SIDE_SIZE, color=HYP)
        hyp_lbl.move_to(Line(A, C).get_center() +
                        normalize(RIGHT *.5 + DOWN * -.1) * 0.55)

        self.add(circle, tri, ra, lbl_A, lbl_B, lbl_C)

        # ---- header: two lines across the TOP, centered ----
        header = VGroup(
            Text("B is the center of the circle.  AC = 16.",
                 font_size=self.Q_SIZE),
            Text("What is the area of △ABC?",
                 font_size=self.Q_SIZE, weight=BOLD),
        ).arrange(DOWN, buff=0.4)
        header.to_edge(UP, buff=0.5)
        self.add(header)

        if self.SHOW_IDENTIFICATION:
            # radii highlighted — the key insight
            rad1 = Line(B, A, color=LEG, stroke_width=7)
            rad2 = Line(B, C, color=LEG, stroke_width=7)

            # tick marks: BA and BC are congruent (both radii)
            for seg in (Line(B, A), Line(B, C)):
                m = seg.get_center()
                d = normalize(seg.get_end() - seg.get_start())
                n = rotate_vector(d, PI / 2)
                self.add(Line(m - n * 0.13, m + n * 0.13,
                              color=LEG, stroke_width=6))

            self.add(rad1, rad2, ra, lbl_A, lbl_B, lbl_C)  # re-add on top

            arc_A = Angle(Line(A, C), Line(A, B), radius=0.45,
                          color=INK, stroke_width=4)
            lbl_45A = MathTex("45^\\circ", font_size=38, color=LEG)
            lbl_45A.move_to(A + normalize(DOWN * 1.6 + RIGHT * 0.62) * 0.85)

            arc_C = Angle(Line(C, B), Line(C, A), radius=0.45,
                          color=INK, stroke_width=4)
            lbl_45C = MathTex("45^\\circ", font_size=38, color=LEG)
            lbl_45C.move_to(C + normalize(UP * 1.05 + LEFT * 1.30) * 1.0)

            self.add(arc_A, arc_C, lbl_45A, lbl_45C)

            insight = VGroup(
                Text("BA and BC are radii", font_size=36, color=LEG),
                MathTex("\\Rightarrow BA = BC \\Rightarrow 45\\text{-}45\\text{-}90",
                        font_size=44),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
            insight.to_edge(RIGHT, buff=0.6).shift(DOWN * 1.8)
            self.add(insight)

        self.wait()


class SAT_4545_Setup(SAT4545Base):
    SHOW_IDENTIFICATION = False


class SAT_4545_Identified(SAT4545Base):
    SHOW_IDENTIFICATION = False

class EquilateralDerivationBase(Scene):
    """Shared geometry for scenes 9a-9c. The equilateral (and its
    ghost square) sit in the same position in every frame."""

    # ---- tweak knobs ----
    SIDE = 3.2                        # screen length of one side (= 2x)
    SHIFT = LEFT * 4.2 + DOWN * 2.2   # bottom-left vertex position
    SIDE_SIZE = 54                    # side-label font size
    ANGLE_SIZE = 38                   # angle-label font size

    def pts(self):
        s = self.SIDE
        A = self.SHIFT                          # bottom-left  (60°)
        B = A + RIGHT * s                       # bottom-right (60°)
        E = A + RIGHT * s / 2 + UP * s * np.sqrt(3) / 2   # apex (60°)
        M = A + RIGHT * s / 2                   # midpoint of base
        return A, B, E, M

    def equilateral(self, color=INK, dashed=False):
        A, B, E, _ = self.pts()
        tri = Polygon(A, B, E, color=color, stroke_width=6)
        if dashed:
            tri = DashedVMobject(tri, num_dashes=36)
        return tri

    def base_sixty_arcs(self):
        """60° arcs + labels at the two base vertices (shared by 9a/9b)."""
        A, B, E, _ = self.pts()
        arc_A = Angle(Line(A, B), Line(A, E), radius=0.5,
                      color=INK, stroke_width=4)
        lbl_A = MathTex("60^\\circ", font_size=self.ANGLE_SIZE)
        lbl_A.move_to(A + normalize(RIGHT * 1.9 + UP * 1.1) * 1.0)

        arc_B = Angle(Line(B, E), Line(B, A), radius=0.5,
                      color=INK, stroke_width=4)
        lbl_B = MathTex("60^\\circ", font_size=self.ANGLE_SIZE)
        lbl_B.move_to(B + normalize(LEFT * 1.9 + UP * 1.1) * 1.0)
        return VGroup(arc_A, lbl_A, arc_B, lbl_B)


class Equilateral(EquilateralDerivationBase):
    """Scene 9a: the equilateral triangle, all sides 2x, all angles 60°,
    ghost square behind it showing where it was constructed. STILL."""

    def construct(self):
        A, B, E, _ = self.pts()

        self.add(self.equilateral())

        # side labels — all 2x
        lbl_base = MathTex("2x", font_size=self.SIDE_SIZE)
        lbl_base.next_to(Line(A, B).get_center(), DOWN, buff=0.28)
        lbl_left = MathTex("2x", font_size=self.SIDE_SIZE)
        lbl_left.move_to(Line(A, E).get_center() +
                         normalize(UP * 0.5 + LEFT * np.sqrt(3) / 2) * 0.55)
        lbl_right = MathTex("2x", font_size=self.SIDE_SIZE)
        lbl_right.move_to(Line(B, E).get_center() +
                          normalize(UP * 0.5 + RIGHT * np.sqrt(3) / 2) * 0.55)
        self.add(lbl_base, lbl_left, lbl_right)

        # angles: the two base 60s + the apex 60
        self.add(self.base_sixty_arcs())
        arc_E = Angle(Line(E, A), Line(E, B), radius=0.5,
                      color=INK, stroke_width=4)
        lbl_E = MathTex("60^\\circ", font_size=self.ANGLE_SIZE)
        lbl_E.move_to(E + DOWN * 0.95)
        self.add(arc_E, lbl_E)

        caption = Text("an equilateral triangle: every side 2x, every angle 60°",
                       font_size=34)
        caption.to_edge(UP, buff=0.5)
        self.add(caption)
        self.wait()


class EquilateralCut(EquilateralDerivationBase):
    """Scene 9b: the altitude drops from the apex. 60° splits into
    30° + 30°, the base splits into x + x, right angle at the foot.
    STILL."""

    def construct(self):
        A, B, E, M = self.pts()

        self.add(self.equilateral())

        # the cut
        alt = Line(E, M, color=ACCENT, stroke_width=6)
        ra = RightAngle(Line(M, B), Line(M, E),
                        length=0.26, color=ACCENT, stroke_width=5)
        self.add(alt, ra)

        # slanted sides keep their 2x
        lbl_left = MathTex("2x", font_size=self.SIDE_SIZE)
        lbl_left.move_to(Line(A, E).get_center() +
                         normalize(UP * 0.5 + LEFT * np.sqrt(3) / 2) * 0.55)
        lbl_right = MathTex("2x", font_size=self.SIDE_SIZE)
        lbl_right.move_to(Line(B, E).get_center() +
                          normalize(UP * 0.5 + RIGHT * np.sqrt(3) / 2) * 0.55)
        self.add(lbl_left, lbl_right)

        # base splits: x + x
        lbl_x1 = MathTex("x", font_size=self.SIDE_SIZE)
        lbl_x1.next_to(Line(A, M).get_center(), DOWN, buff=0.28)
        lbl_x2 = MathTex("x", font_size=self.SIDE_SIZE)
        lbl_x2.next_to(Line(M, B).get_center(), DOWN, buff=0.28)
        self.add(lbl_x1, lbl_x2)

        # base 60s stay; apex 60 becomes 30 + 30
        self.add(self.base_sixty_arcs())
        arc_l = Angle(Line(E, A), Line(E, M), radius=0.62,
                      color=INK, stroke_width=4, other_angle=False)
        arc_r = Angle(Line(E, M), Line(E, B), radius=0.62,
                      color=INK, stroke_width=4, other_angle=False)
        lbl_30l = MathTex("30^\\circ", font_size=self.ANGLE_SIZE)
        lbl_30l.move_to(E + UP * .05 + LEFT * 0.42)
        lbl_30r = MathTex("30^\\circ", font_size=self.ANGLE_SIZE)
        lbl_30r.move_to(E + UP * .05 + RIGHT * 0.42)
        self.add(arc_l, arc_r, lbl_30l, lbl_30r)

        caption = Text("drop the altitude: 60° splits into 30° + 30°, "
                       "the base splits into x + x", font_size=34)
        caption.to_edge(UP, buff=0.5)
        self.add(caption)
        self.wait()


class ThirtySixtyDerived(EquilateralDerivationBase):
    """Scene 9c: the extracted 30-60-90 (left half), color-coded.
    Ghost equilateral + altitude behind, Pythagorean work right,
    ratio x : x√3 : 2x banked top-left. STILL."""

    WORK_SIZE = 46

    def construct(self):
        A, B, E, M = self.pts()

        # ghosts: the equilateral and the cut that made this triangle
        self.add(self.equilateral(color=GHOST, dashed=True))
        self.add(DashedLine(E, M, color=GHOST, stroke_width=3))

        # extracted RIGHT half, stepped out
        STEP = (RIGHT * (self.SIDE / 2 + 1.5)) * 0    # tweak: extraction offset
        B2, M2, E2 = B + STEP, M + STEP, E + STEP

        tri = Polygon(B2, M2, E2, color=INK, stroke_width=6)
        ra = RightAngle(Line(M2, B2), Line(M2, E2),
                        length=0.26, color=ACCENT, stroke_width=5)
        self.add(tri, ra)

        # color-coded side labels
        short_lbl = MathTex("x", font_size=self.SIDE_SIZE, color=LEG)
        short_lbl.next_to(Line(B2, M2).get_center(), DOWN, buff=0.28)
        long_lbl = MathTex("x\\sqrt{3}", font_size=self.SIDE_SIZE, color=LONG)
        long_lbl.next_to(Line(M2, E2).get_center(), LEFT, buff=0.25)
        hyp_lbl = MathTex("2x", font_size=self.SIDE_SIZE, color=HYP)
        hyp_lbl.move_to(Line(B2, E2).get_center() +
                        normalize(UP * 0.5 + RIGHT * np.sqrt(3) / 2) * 0.55)
        self.add(short_lbl, long_lbl, hyp_lbl)

        # angles: 60 at the base vertex, 30 at the apex
        arc_B = Angle(Line(B2, E2), Line(B2, M2), radius=0.5,
                      color=INK, stroke_width=4)
        lbl_60 = MathTex("60^\\circ", font_size=self.ANGLE_SIZE)
        lbl_60.move_to(B2 + normalize(LEFT * 1.9 + UP * 1.1) * 1.0)
        arc_E = Angle(Line(E2, M2), Line(E2, B2), radius=0.62,
                      color=INK, stroke_width=4, other_angle=False)
        lbl_30 = MathTex("30^\\circ", font_size=self.ANGLE_SIZE)
        lbl_30.move_to(E2 + UP * .02 + RIGHT * 0.40)
        self.add(arc_B, lbl_60, arc_E, lbl_30)

        # Pythagorean work, right side
        work = VGroup(
            MathTex("x^2 + h^2 = (2x)^2", font_size=self.WORK_SIZE),
            MathTex("h^2 = 4x^2 - x^2 = 3x^2", font_size=self.WORK_SIZE),
            MathTex("h = x\\sqrt{3}", font_size=self.WORK_SIZE, color=LONG),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        work.to_edge(RIGHT, buff=0.7).shift(DOWN * 0.9)
        self.add(work)

        # the banked ratio, color-coded, usual corner
        bank = MathTex("x", ":", "x\\sqrt{3}", ":", "2x", font_size=60)
        bank[0].set_color(LEG)
        bank[2].set_color(LONG)
        bank[4].set_color(HYP)
        bank.to_corner(UL, buff=0.6)
        self.add(bank, SurroundingRectangle(bank, color=INK, buff=0.25,
                                            corner_radius=0.1,
                                            stroke_width=3))
        self.wait()

class ThirtySixtyExampleBase(Scene):
    """Scenes 10a-10c: 30-60-90 examples, unsolved. Given side labeled,
    question marks on the other two. Color-coded: LEG = short leg (30°),
    LONG = long leg (60°), HYP = hypotenuse (90°). Ghost equilateral
    behind the triangle. Banked ratio top-left. STILL x3."""

    GIVEN = "2"           # overridden per example
    GIVEN_SIDE = "short"  # "short" | "long" | "hyp"
    S = 1.9               # screen length of the SHORT leg (= x)

    # ---- tweak knobs ----
    SHIFT = LEFT * 3.4 + DOWN * 2.4   # bottom-left vertex position
    SIDE_SIZE = 60
    ANGLE_SIZE = 38

    def construct(self):
        s = self.S
        # left half of an equilateral with side 2s:
        A = self.SHIFT                       # 60° vertex (bottom-left)
        M = A + RIGHT * s                    # right angle (foot of altitude)
        E = A + RIGHT * s + UP * s * np.sqrt(3)   # 30° vertex (apex)
        B = A + RIGHT * 2 * s                # ghost's far base vertex

        # ghost: the full equilateral this triangle was cut from
        ghost = DashedVMobject(
            Polygon(A, B, E, color=GHOST, stroke_width=5),
            num_dashes=40)
        self.add(ghost)

        # the triangle itself
        tri = Polygon(A, M, E, color=INK, stroke_width=6)
        ra = RightAngle(Line(M, A), Line(M, E),
                        length=0.26, color=ACCENT, stroke_width=5)

        # ---- side labels: given on chosen side, ? on the other two ----
        short_pt = Line(A, M).get_center()
        long_pt = Line(M, E).get_center()
        hyp_pt = Line(A, E).get_center()

        role_color = {"short": LEG, "long": LONG, "hyp": HYP}
        given = MathTex(self.GIVEN, font_size=self.SIDE_SIZE,
                        color=role_color[self.GIVEN_SIDE])
        q_short = MathTex("?", font_size=self.SIDE_SIZE, color=LEG)
        q_long = MathTex("?", font_size=self.SIDE_SIZE, color=LONG)
        q_hyp = MathTex("?", font_size=self.SIDE_SIZE, color=HYP)

        if self.GIVEN_SIDE == "short":
            short_lbl, long_lbl, hyp_lbl = given, q_long, q_hyp
        elif self.GIVEN_SIDE == "long":
            short_lbl, long_lbl, hyp_lbl = q_short, given, q_hyp
        else:  # "hyp"
            short_lbl, long_lbl, hyp_lbl = q_short, q_long, given

        short_lbl.next_to(short_pt, DOWN, buff=0.3)
        long_lbl.next_to(long_pt, RIGHT, buff=0.3)
        hyp_lbl.move_to(hyp_pt +
                        normalize(UP * 0.5 + LEFT * np.sqrt(3) / 2) * 0.55)

        # interior angles: 60 at A, 30 at E
        arc_A = Angle(Line(A, M), Line(A, E), radius=0.45,
                      color=INK, stroke_width=4)
        lbl_60 = MathTex("60^\\circ", font_size=self.ANGLE_SIZE)
        lbl_60.move_to(A + normalize(RIGHT * 1.9 + UP * 1.1) * 0.95)

        arc_E = Angle(Line(E, A), Line(E, M), radius=0.55,
                      color=INK, stroke_width=4, other_angle=False)
        lbl_30 = MathTex("30^\\circ", font_size=self.ANGLE_SIZE)
        lbl_30.move_to(E + DOWN * 1.0 + LEFT * 0.28)

        self.add(tri, ra, short_lbl, long_lbl, hyp_lbl,
                 arc_A, lbl_60, arc_E, lbl_30)

        # standing reference: color-coded banked ratio
        bank = MathTex("x", ":", "x\\sqrt{3}", ":", "2x", font_size=60)
        bank[0].set_color(LEG)
        bank[2].set_color(LONG)
        bank[4].set_color(HYP)
        bank.to_corner(UL, buff=0.6)
        self.add(bank, SurroundingRectangle(bank, color=INK, buff=0.25,
                                            corner_radius=0.1,
                                            stroke_width=3))
        self.wait()


class ThirtySixty_Ex1(ThirtySixtyExampleBase):
    GIVEN = "2"
    GIVEN_SIDE = "short"
    S = 1.9


class ThirtySixty_Ex2(ThirtySixtyExampleBase):
    GIVEN = "20"
    GIVEN_SIDE = "hyp"
    S = 1.9


class ThirtySixty_ExX(ThirtySixtyExampleBase):
    GIVEN = "4\\sqrt{3}"
    GIVEN_SIDE = "long"
    S = 1.9

class ThirtySixty_Ratio(Scene):
    """Scene 11: the hub diagram. Short leg (30°) is the hub;
    30<->90 is x/÷2, 30<->60 is x/÷sqrt(3). Optional dashed chord
    shows the derived direct 60<->90 rate. Key top-left. STILL."""

    SHOW_CHORD = True        # the derived 60<->90 shortcut

    # ---- tweak knobs ----
    NODE_SIZE = 84           # angle-node font size
    OP_SIZE = 48             # operation-label font size
    CHORD_OP_SIZE = 40       # chord-label font size (subordinate)
    N30 = DOWN * 2.0                     # node positions
    N60 = UP * 1.4 + LEFT * 3.4
    N90 = UP * 1.4 + RIGHT * 3.4

    def spoke(self, a, b, op_ab, op_ba, side=LEFT, lbl_off=0.55):
        """Double curved arrows between two nodes with op labels.
        side = which side of the spoke the labels sit on.
        lbl_off = how far the op labels sit off the arrows."""
        d = normalize(b.get_center() - a.get_center())
        n = rotate_vector(d, PI / 2)     # normal for offsetting

        fwd = CurvedArrow(
            a.get_center() + d * 0.85 + n * 0.18,
            b.get_center() - d * 0.85 + n * 0.18,
            angle=-TAU / 12, color=INK, stroke_width=5, tip_length=0.22)
        bwd = CurvedArrow(
            b.get_center() - d * 0.85 - n * 0.18,
            a.get_center() + d * 0.85 - n * 0.18,
            angle=-TAU / 12, color=INK, stroke_width=5, tip_length=0.22)

        lbl_fwd = MathTex(op_ab, font_size=self.OP_SIZE)
        lbl_fwd.move_to(fwd.get_center() + n * lbl_off)
        lbl_bwd = MathTex(op_ba, font_size=self.OP_SIZE)
        lbl_bwd.move_to(bwd.get_center() - n * lbl_off)

        return VGroup(fwd, bwd, lbl_fwd, lbl_bwd)

    def construct(self):
        # ---- key, usual corner ----
        bank = MathTex("x", ":", "x\\sqrt{3}", ":", "2x", font_size=60)
        bank[0].set_color(LEG)
        bank[2].set_color(LONG)
        bank[4].set_color(HYP)
        bank.to_corner(UL, buff=0.55)
        self.add(bank, SurroundingRectangle(bank, color=INK, buff=0.25,
                                            corner_radius=0.1,
                                            stroke_width=3))

        # ---- nodes: 30 at the bottom = the hub ----
        n30 = MathTex("30^\\circ", font_size=self.NODE_SIZE, color=LEG)
        n30.move_to(self.N30)
        n60 = MathTex("60^\\circ", font_size=self.NODE_SIZE, color=LONG)
        n60.move_to(self.N60)
        n90 = MathTex("90^\\circ", font_size=self.NODE_SIZE, color=HYP)
        n90.move_to(self.N90)

        # hub emphasis: a ring around the 30
        hub_ring = Circle(radius=0.85, color=LEG, stroke_width=4)
        hub_ring.move_to(n30)

        self.add(n30, n60, n90, hub_ring)

        # ---- spokes ----
        self.add(self.spoke(n30, n90, "\\times 2", "\\div 2"))
        self.add(self.spoke(n30, n60, "\\times \\sqrt{3}", "\\div \\sqrt{3}",
                            lbl_off=0.72))    # tweak: clear the arrows

        # ---- optional derived chord: 60 <-> 90 direct ----
        if self.SHOW_CHORD:
            chord = DashedLine(
                n60.get_right() + RIGHT * 0.25,
                n90.get_left() + LEFT * 0.25,
                color=GHOST, stroke_width=4)
            self.add(chord)

        # # ---- heuristic caption ----
        # heur = Text("bigger angle → longer side → multiply   ·   "
        #             "smaller angle → shorter side → divide",
        #             font_size=30, slant=ITALIC)
        # heur.to_edge(DOWN, buff=0.45)
        # self.add(heur)
        # self.wait()

class SAT3060Base(Scene):
    """Scene 13: capstone 30-60-90 problem. O is the circle's center,
    AC = 20, 30° at C, right angle at B. Find the shaded area
    (circle minus triangle).
    Setup frame gives only what the problem gives.
    Identified frame reveals the strategy + the diameter insight.
    STILL x2."""

    SHOW_IDENTIFICATION = False

    # ---- tweak knobs ----
    X = 1.8                    # short leg (BA) on screen; R = X
    SHIFT = LEFT * 4.4 + DOWN * 1.5   # position of B (the right angle)
    LBL_SIZE = 48              # vertex letters
    SIDE_SIZE = 54
    ANGLE_SIZE = 40
    Q_SIZE = 42

    def construct(self):
        x = self.X
        # right angle at B; short leg up to A, long leg right to C
        B = self.SHIFT
        A = B + UP * x                       # opposite the 30° -> short leg
        C = B + RIGHT * x * np.sqrt(3)       # opposite the 60° -> long leg
        O = (A + C) / 2                      # hypotenuse midpoint = center
        R = x                                # circumradius = half of 2x

        circle = Circle(radius=R, color=INK, stroke_width=5).move_to(O)
        tri = Polygon(A, B, C, color=INK, stroke_width=6)

        # shaded region: circle minus triangle
        shade = Difference(
            Circle(radius=R).move_to(O),
            Polygon(A, B, C),
        ).set_fill(BANK, opacity=0.15).set_stroke(width=0)
        self.add(shade, circle, tri)

        ra = RightAngle(Line(B, A), Line(B, C),
                        length=0.28, color=ACCENT, stroke_width=5)

        # the given 30° at C
        arc_C = Angle(Line(C, A), Line(C, B), radius=0.55,
                      color=INK, stroke_width=4)
        lbl_30 = MathTex("30^\\circ", font_size=self.ANGLE_SIZE)
        lbl_30.move_to(C + normalize(UP * 0.23 + LEFT * np.sqrt(3) / 2) * 1.15)

        # vertex letters + center dot
        lbl_A = MathTex("A", font_size=self.LBL_SIZE)
        lbl_A.next_to(A, UP + LEFT * 0.3, buff=0.15)
        lbl_B = MathTex("B", font_size=self.LBL_SIZE)
        lbl_B.next_to(B, DOWN + LEFT * 0.3, buff=0.15)
        lbl_C = MathTex("C", font_size=self.LBL_SIZE)
        lbl_C.next_to(C, DOWN + RIGHT * 0.3, buff=0.15)

        O_dot = Dot(O, radius=0.06, color=INK)
        lbl_O = MathTex("O", font_size=self.LBL_SIZE)
        lbl_O.next_to(O_dot, UP + RIGHT * 0.4, buff=0.12)

        # the given: AC = 20, placed off O's corner of the hypotenuse
        hyp_lbl = MathTex("20", font_size=self.SIDE_SIZE, color=HYP)
        hyp_pos = A + (C - A) * 0.28         # tweak: slide along AC
        hyp_lbl.move_to(hyp_pos +
                        normalize(UP * np.sqrt(3) / 2 + RIGHT * 0.5) * 0.5)

        self.add(ra, arc_C, lbl_30, lbl_A, lbl_B, lbl_C,
                 O_dot, lbl_O)

        # problem statement, top
        q = VGroup(
            Text("O is the center of the circle. AC = 20", font_size=self.Q_SIZE),
            # Text("AC = 20.", font_size=self.Q_SIZE),
            Text("What is the area of the shaded region?", font_size=self.Q_SIZE,
                 weight=BOLD),
            # Text("shaded region?", font_size=self.Q_SIZE, weight=BOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42)
        q.to_corner(UP, buff=0.3)
        self.add(q)

        if self.SHOW_IDENTIFICATION:
            # insight 1: AC passes through O -> it's the diameter
            diam = Line(A, C, color=HYP, stroke_width=7)
            self.add(diam, O_dot, lbl_O, hyp_lbl, ra)  # re-stack on top

            # insight 2: the missing angle at A is 60°
            arc_A = Angle(Line(A, B), Line(A, C), radius=0.45,
                          color=INK, stroke_width=4)
            lbl_60 = MathTex("60^\\circ", font_size=self.ANGLE_SIZE,
                             color=LONG)
            lbl_60.move_to(A + normalize(DOWN * 1.2 + RIGHT * 0.75) * 0.95)
            self.add(arc_A, lbl_60)

            # the strategy + the two identifications
            insight = VGroup(
                MathTex("A_{\\text{shaded}} = A_{\\text{circle}} "
                        "- A_{\\text{triangle}}", font_size=48),
                Text("AC passes through O ⇒ diameter",
                     font_size=34, color=HYP),
                MathTex("180^\\circ - 90^\\circ - 30^\\circ = 60^\\circ"
                        "\\;\\Rightarrow\\; 30\\text{-}60\\text{-}90",
                        font_size=40),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
            insight.to_edge(RIGHT, buff=0.8).shift(DOWN * 1.7)
            self.add(insight)

        self.wait()


class SAT_3060_Setup(SAT3060Base):
    SHOW_IDENTIFICATION = False


class SAT_3060_Identified(SAT3060Base):
    SHOW_IDENTIFICATION = True

class SpecialRecap(Scene):
    """Recap scene: static top band (the six solved examples, boxed by
    family, keys beneath) + looping animation below (fixed angles ->
    scaling preserves proportion; new angle -> new fixed proportion).
    VIDEO loops in PowerPoint. Start/end states match."""

    # ---- tweak knobs ----
    MINI_LBL = 24            # mini side-label font size
    KEY_SIZE = 34            # key font size in the boxes
    MINI_45 = 0.62           # mini 45 leg length
    MINI_3060 = 0.52         # mini 3060 short-leg length
    BAND_Y = 2.55            # vertical center of the top band
    ANCHOR = LEFT * 3.6 + DOWN * 3.3   # animated triangle's 60ish corner
    BASE = 3.0               # animated triangle base at s = 1
    THETA1 = 45 * DEGREES    # beat-1 fixed angle
    THETA2 = 30 * DEGREES    # beat-2 fixed angle
    S_SMALL = 0.62           # loop start/end scale

    # ---------- static minis ----------
    def mini45(self, b, l, h):
        s = self.MINI_45
        bl, br, tr = ORIGIN, RIGHT * s, RIGHT * s + UP * s
        tri = Polygon(bl, br, tr, color=INK, stroke_width=4)
        ra = RightAngle(Line(br, bl), Line(br, tr), length=0.14,
                        color=ACCENT, stroke_width=3)
        g = VGroup(tri, ra)
        g.add(MathTex(b, font_size=self.MINI_LBL, color=LEG)
              .next_to(Line(bl, br).get_center(), DOWN, buff=0.12))
        g.add(MathTex(l, font_size=self.MINI_LBL, color=LEG)
              .next_to(Line(br, tr).get_center(), RIGHT, buff=0.12))
        g.add(MathTex(h, font_size=self.MINI_LBL, color=HYP)
              .move_to(Line(bl, tr).get_center() +
                       normalize(UP + LEFT) * 0.3))
        return g

    def mini3060(self, sh, lo, h):
        x = self.MINI_3060
        A, M, E = ORIGIN, RIGHT * x, RIGHT * x + UP * x * np.sqrt(3)
        tri = Polygon(A, M, E, color=INK, stroke_width=4)
        ra = RightAngle(Line(M, A), Line(M, E), length=0.14,
                        color=ACCENT, stroke_width=3)
        g = VGroup(tri, ra)
        g.add(MathTex(sh, font_size=self.MINI_LBL, color=LEG)
              .next_to(Line(A, M).get_center(), DOWN, buff=0.12))
        g.add(MathTex(lo, font_size=self.MINI_LBL, color=LONG)
              .next_to(Line(M, E).get_center(), RIGHT, buff=0.12))
        g.add(MathTex(h, font_size=self.MINI_LBL, color=HYP)
              .move_to(Line(A, E).get_center() +
                       normalize(UP * 0.5 + LEFT * np.sqrt(3) / 2) * 0.34))
        return g

    def boxed_family(self, minis, key_parts, key_colors):
        row = VGroup(*minis).arrange(RIGHT, buff=0.75, aligned_edge=DOWN)
        key = MathTex(*key_parts, font_size=self.KEY_SIZE)
        for i, c in key_colors.items():
            key[i].set_color(c)
        key.next_to(row, DOWN, buff=0.32)
        content = VGroup(row, key)
        box = SurroundingRectangle(content, color=INK, buff=0.3,
                                   corner_radius=0.12, stroke_width=3)
        return VGroup(content, box)

    def construct(self):
        # ================= static top band =================
        fam45 = self.boxed_family(
            [self.mini45("1", "1", "\\sqrt{2}"),
             self.mini45("2", "2", "2\\sqrt{2}"),
             self.mini45("x", "x", "x\\sqrt{2}")],
            ["x", ":", "x", ":", "x\\sqrt{2}"],
            {0: LEG, 2: LEG, 4: HYP})

        fam3060 = self.boxed_family(
            [self.mini3060("2", "2\\sqrt{3}", "4"),
             self.mini3060("10", "10\\sqrt{3}", "20"),
             self.mini3060("4", "4\\sqrt{3}", "8")],
            ["x", ":", "x\\sqrt{3}", ":", "2x"],
            {0: LEG, 2: LONG, 4: HYP})

        band = VGroup(fam45, fam3060).arrange(RIGHT, buff=0.7)
        band.move_to(UP * self.BAND_Y)
        self.add(band)

        # ================= animated middle =================
        theta = ValueTracker(self.THETA1)
        s = ValueTracker(self.S_SMALL)

        def verts():
            b = self.BASE * s.get_value()
            A = self.ANCHOR                       # base angle theta here
            R = A + RIGHT * b                     # right angle
            T = R + UP * b * np.tan(theta.get_value())
            return A, R, T

        tri = always_redraw(lambda: Polygon(*verts(), color=INK,
                                            stroke_width=6))
        ra = always_redraw(lambda: RightAngle(
            Line(verts()[1], verts()[0]), Line(verts()[1], verts()[2]),
            length=0.24, color=INK, stroke_width=4))
        arc = always_redraw(lambda: Angle(
            Line(verts()[0], verts()[1]), Line(verts()[0], verts()[2]),
            radius=0.55, color=ACCENT, stroke_width=5))

        # live proportion readout: opposite / hypotenuse
        ratio_label = MathTex(
            "\\frac{\\text{opposite}}{\\text{hypotenuse}} =",
            font_size=44)
        ratio_label.move_to(RIGHT * 2.7 + DOWN * 1.7)
        ratio_num = always_redraw(lambda: DecimalNumber(
            np.sin(theta.get_value()), num_decimal_places=3,
            font_size=48, color=ACCENT).next_to(ratio_label, RIGHT,
                                                buff=0.25))

        self.add(tri, ra, arc, ratio_label, ratio_num)
        self.wait(0.4)

        # ---- beat 1: scale changes, proportion frozen ----
        self.play(s.animate.set_value(1.15), run_time=1.7, rate_func=smooth)
        self.play(s.animate.set_value(0.80), run_time=1.4, rate_func=smooth)
        self.wait(0.5)

        # ---- beat 2: new fixed angle, then scale again ----
        self.play(theta.animate.set_value(self.THETA2), run_time=1.3,
                  rate_func=smooth)
        self.play(s.animate.set_value(1.2), run_time=1.6, rate_func=smooth)
        self.play(s.animate.set_value(self.S_SMALL), run_time=1.4,
                  rate_func=smooth)
        self.wait(0.4)

        # ---- return to start state for a seamless loop ----
        self.play(theta.animate.set_value(self.THETA1), run_time=1.0,
                  rate_func=smooth)
        self.wait(0.5)