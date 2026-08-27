"""
    manim -qh -s lineq/demo3.py CandleWordProblem
    manim -qh -s lineq/demo3.py GymWordProblem
    manim -qh -s lineq/demo3.py WaterTankWordProblem
"""

from manim import *

config.background_color = WHITE

INK    = BLACK
ACCENT = RED_D    # pieces just pulled out of the word problem
GHOST  = GREY_B   # de-emphasized / scratch text (unused here, kept for parity)
BANK   = BLUE_D   # banked / final result

Mobject.set_default(color=INK)
Text.set_default(color=INK)
MathTex.set_default(color=INK)


# helpers, mostly unused
def component_row(phrase, symbol_tex, phrase_font=26, symbol_font=34):
    """One row: a quoted phrase from the problem -> the symbol it becomes."""
    phrase_text = Text(f'"{phrase}"', font_size=phrase_font, slant=ITALIC)
    arrow = MathTex(r"\Rightarrow", font_size=symbol_font)
    symbol = MathTex(symbol_tex, font_size=symbol_font, color=ACCENT)
    return VGroup(phrase_text, arrow, symbol).arrange(RIGHT, buff=0.3)


def boxed_answer(target, label_text):
    box = SurroundingRectangle(target, color=ACCENT, buff=0.2, stroke_width=5)
    label = Text(label_text, font_size=36, color=BANK, weight=BOLD)
    label.next_to(box, DOWN, buff=0.3)
    return VGroup(box, label)

class CandleWordProblem(Scene):
    def construct(self):
        PROBLEM_FONT = 30
        ROW_BUFF     = 0.3
        COL_GAP      = 1.3

        # title = Text("The Candle", font_size=40, weight=BOLD)
        # title.to_edge(UP, buff=0.4)

        problem = Text(
            "A candle is 20 cm tall when it's lit. It burns down at a\n"
            "constant rate of 2 cm per hour. After how many hours will\n"
            "it be 8 cm tall?",
            font_size=PROBLEM_FONT,
            line_spacing=1.2,
        )
        # problem.next_to(title, DOWN, buff=0.45)

        self.play(Write(problem))

        # # ---- pull the components out of the words ----
        # rows = VGroup(
        #     component_row("20 cm tall when it's lit", "b = 20"),
        #     component_row("burns... 2 cm per hour", "m = -2"),
        #     component_row("8 cm tall", "y = 8"),
        #     component_row("how many hours?", "x = \\,?"),
        # ).arrange(DOWN, aligned_edge=LEFT, buff=ROW_BUFF)
        # rows.next_to(problem, DOWN, buff=0.6).to_edge(LEFT, buff=1.0)

        # self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.3))

        # # ---- build the equation and solve for x ----
        # general = MathTex("y = mx + b", font_size=44)
        # sub     = MathTex("8 = -2x + 20", font_size=44)
        # step1   = MathTex("-12 = -2x", font_size=44)
        # step2   = MathTex("x = 6", font_size=44, color=BANK)

        # solve = VGroup(general, sub, step1, step2).arrange(DOWN, buff=0.4)
        # solve.next_to(rows, RIGHT, buff=COL_GAP).align_to(rows, UP)

        # self.play(Write(general))
        # self.play(TransformMatchingTex(general.copy(), sub))
        # self.play(TransformMatchingTex(sub.copy(), step1))
        # self.play(TransformMatchingTex(step1.copy(), step2))

        # answer = boxed_answer(step2, "6 hours")
        # self.play(Create(answer[0]), FadeIn(answer[1]))
        self.wait()

class GymWordProblem(Scene):
    def construct(self):
        PROBLEM_FONT = 30
        ROW_BUFF     = 0.3
        COL_GAP      = 1.3

        title = Text("gym membership", font_size=40, weight=BOLD)
        title.to_edge(UP, buff=0.4)

        problem = Text(
            "A gym charges a $45 sign-up fee, then $15 per month after\n"
            "that. What is the total cost after 8 months?",
            font_size=PROBLEM_FONT,
            line_spacing=1.2,
        )
        problem.next_to(title, DOWN, buff=0.45)

        # self.play(Write(title), FadeIn(problem))
        self.play(FadeIn(problem))

        rows = VGroup(
            component_row("$45 sign-up fee", "b = 45"),
            component_row("$15 per month", "m = 15"),
            component_row("after 8 months", "x = 8"),
            component_row("total cost?", "y = \\,?"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=ROW_BUFF)
        rows.next_to(problem, DOWN, buff=0.6).to_edge(LEFT, buff=1.0)

        # self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.3))

        # general = MathTex("y = mx + b", font_size=44)
        # sub     = MathTex("y = 15(8) + 45", font_size=44)
        # step1   = MathTex("y = 120 + 45", font_size=44)
        # step2   = MathTex("y = 165", font_size=44, color=BANK)

        # solve = VGroup(general, sub, step1, step2).arrange(DOWN, buff=0.4)
        # solve.next_to(rows, RIGHT, buff=COL_GAP).align_to(rows, UP)

        # self.play(Write(general))
        # self.play(TransformMatchingTex(general.copy(), sub))
        # self.play(TransformMatchingTex(sub.copy(), step1))
        # self.play(TransformMatchingTex(step1.copy(), step2))

        # answer = boxed_answer(step2, "$165 total")
        # self.play(Create(answer[0]), FadeIn(answer[1]))
        self.wait()

class WaterTankWordProblem(Scene):
    def construct(self):
        PROBLEM_FONT = 28
        ROW_BUFF     = 0.28
        COL_GAP      = 1.1

        title = Text("Water Tank", font_size=40, weight=BOLD)
        title.to_edge(UP, buff=0.4)

        problem = Text(
            "A tank starts with 12 gallons. After 5 minutes it has\n"
            "42 gallons, filling at a constant rate. How many minutes\n"
            "until the tank has 90 gallons?",
            font_size=PROBLEM_FONT,
            line_spacing=1.2,
        )
        problem.next_to(title, DOWN, buff=0.4)

        self.play(FadeIn(problem))

        rows = VGroup(
            component_row("starts with 12 gallons", "(0,\\,12)"),
            component_row("after 5 min, 42 gallons", "(5,\\,42)"),
            component_row("has 90 gallons", "y = 90"),
            component_row("how many minutes?", "x = \\,?"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=ROW_BUFF)
        rows.next_to(problem, DOWN, buff=0.55).to_edge(LEFT, buff=0.9)

        # self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.3))

        slope_formula = MathTex(r"m = \frac{y_2-y_1}{x_2-x_1}", font_size=38)
        slope_sub     = MathTex(r"m = \frac{42-12}{5-0}", font_size=38)
        slope_val     = MathTex("m = 6", font_size=38, color=ACCENT)

        slope_work = VGroup(slope_formula, slope_sub, slope_val).arrange(DOWN, buff=0.28)
        slope_work.next_to(rows, RIGHT, buff=COL_GAP).align_to(rows, UP)

        # self.play(Write(slope_formula))
        # self.play(TransformMatchingTex(slope_formula.copy(), slope_sub))
        # self.play(TransformMatchingTex(slope_sub.copy(), slope_val))

        general = MathTex("y = mx + b", font_size=38)
        sub     = MathTex("90 = 6x + 12", font_size=38)
        step1   = MathTex("78 = 6x", font_size=38)
        step2   = MathTex("x = 13", font_size=38, color=BANK)

        # solve = VGroup(general, sub, step1, step2).arrange(DOWN, buff=0.28)
        # solve.next_to(slope_work, DOWN, buff=0.45).align_to(slope_work, LEFT)

        # self.play(Write(general))
        # self.play(TransformMatchingTex(general.copy(), sub))
        # self.play(TransformMatchingTex(sub.copy(), step1))
        # self.play(TransformMatchingTex(step1.copy(), step2))

        # answer = boxed_answer(step2, "13 minutes")
        # self.play(Create(answer[0]), FadeIn(answer[1]))
        self.wait()