# -*- coding: utf-8 -*-
"""Ch3 对数频率轴：同样的音程，只有对数轴才等距；八度 = ×2。"""
import numpy as np
from manim import *
from common import T, C_TITLE, C_HL, C_SUB, C_NOTE, C_GRID


class LogFrequency(Scene):
    def construct(self):
        title = T("同样的音程，对数轴才等距", font_size=40, color=C_TITLE)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title))
        self.wait(0.3)

        notes = [("A2", 110), ("A3", 220), ("A4", 440), ("A5", 880)]

        # 线性轴
        lin = Line(LEFT * 3.6, RIGHT * 3.6, color=C_GRID, stroke_width=4)
        lin.shift(UP * 0.6)
        lin_lab = T("线性轴：每 Hz 等长", font_size=26, color=C_SUB)
        lin_lab.next_to(lin, LEFT, buff=0.8)
        self.play(Create(lin), FadeIn(lin_lab))
        fmin, fmax = 0.0, 1000.0

        def xlin(f):
            return lin.get_center()[0] + (f - fmin) / (fmax - fmin) * 3.6

        for name, f in notes:
            p = np.array([xlin(f), lin.get_center()[1], 0])
            self.play(FadeIn(Dot(p, radius=0.07, color=C_NOTE)))
            lab = T(f"{name}  {f} Hz", font_size=22, color=C_SUB).next_to(p, UP, buff=0.12)
            self.add(lab)
        self.wait(0.4)
        # 线性轴上 A3–A4 与 A4–A5 的"臂"不等长
        b1 = Brace(Line(np.array([xlin(220), lin.get_center()[1], 0]),
                        np.array([xlin(440), lin.get_center()[1], 0])),
                   DOWN, buff=0.1)
        b2 = Brace(Line(np.array([xlin(440), lin.get_center()[1], 0]),
                        np.array([xlin(880), lin.get_center()[1], 0])),
                   DOWN, buff=0.1)
        self.play(FadeIn(b1), FadeIn(b2))
        self.wait(0.5)

        # 对数轴
        log_ = Line(LEFT * 3.6, RIGHT * 3.6, color=C_NOTE, stroke_width=4)
        log_.shift(DOWN * 1.6)
        log_lab = T("对数轴：每八度等长", font_size=26, color=C_SUB)
        log_lab.next_to(log_, LEFT, buff=0.8)
        self.play(ReplacementTransform(lin.copy(), log_),
                  ReplacementTransform(lin_lab.copy(), log_lab))
        f0, f1 = 110.0, 880.0

        def xlog(f):
            return log_.get_center()[0] + np.log(f / f0) / np.log(f1 / f0) * 3.6

        for name, f in notes:
            p = np.array([xlog(f), log_.get_center()[1], 0])
            self.play(FadeIn(Dot(p, radius=0.07, color=C_HL)))
            lab = T(f"{name}  {f} Hz", font_size=22, color=C_SUB).next_to(p, UP, buff=0.12)
            self.add(lab)
        self.wait(0.4)
        c1 = Brace(Line(np.array([xlog(220), log_.get_center()[1], 0]),
                        np.array([xlog(440), log_.get_center()[1], 0])),
                   DOWN, buff=0.1)
        c2 = Brace(Line(np.array([xlog(440), log_.get_center()[1], 0]),
                        np.array([xlog(880), log_.get_center()[1], 0])),
                   DOWN, buff=0.1)
        self.play(FadeIn(c1), FadeIn(c2))
        self.wait(0.6)

        # 公式（Text + Unicode，无需 LaTeX）
        eq = T("c = 1200 × log₂ (f₂ / f₁)", font_size=38)
        eq2 = T("八度：f₂ = 2·f₁  ⟹  1200 × log₂ 2 = 1200 音分",
                font_size=30, color=C_HL)
        box = VGroup(eq, eq2).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.7)
        self.play(FadeIn(box))
        self.wait(1.5)
