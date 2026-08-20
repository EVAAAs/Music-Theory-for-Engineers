# -*- coding: utf-8 -*-
"""Ch8 音程 = 频率比：转位 = 互补比 r ↔ 2/r；
纯五度 701.96c + 纯四度 498.04c 恰好补成一个八度。"""
import numpy as np
from manim import *
from common import T, project_common, C_TITLE, C_PYTH, C_JUST, C_HL, C_GRID, C_SUB

proj = project_common()
rtc = proj.ratio_to_cents


class IntervalsInversion(Scene):
    def construct(self):
        title = T("音程 = 频率比；转位 = 互补比 r ↔ 2/r", font_size=40, color=C_TITLE)
        title.to_edge(UP, buff=0.35)
        self.play(FadeIn(title))

        ctr = np.array([0.0, 0.4, 0.0])
        R = 2.4
        circ = Circle(radius=R, color=C_GRID, stroke_width=3).move_to(ctr)
        self.play(Create(circ))

        f = rtc(3 / 2)   # 纯五度 701.96
        p = rtc(4 / 3)   # 纯四度 498.04

        def pt_on(c):
            a = np.pi / 2 - 2 * np.pi * c / 1200
            return ctr + R * np.array([np.cos(a), np.sin(a), 0])

        a0 = np.pi / 2
        arc_f = Arc(radius=R, start_angle=a0, angle=-2 * np.pi * f / 1200,
                    color=C_PYTH, stroke_width=7).move_to(ctr)
        self.play(Create(arc_f))
        a1 = np.pi / 2 - 2 * np.pi * f / 1200
        arc_p = Arc(radius=R, start_angle=a1, angle=-2 * np.pi * p / 1200,
                    color=C_JUST, stroke_width=7).move_to(ctr)
        self.play(Create(arc_p))

        dotC = Dot(pt_on(0), radius=0.09, color=C_TITLE)
        dotG = Dot(pt_on(f), radius=0.09, color=C_PYTH)
        self.play(FadeIn(dotC), FadeIn(dotG))
        self.add(T("C", font_size=26, color=C_TITLE).next_to(pt_on(0), UP, buff=0.12))
        self.add(T("G", font_size=26, color=C_PYTH).next_to(pt_on(f), UR, buff=0.05))

        def mid_pt(c0, dc):
            a = np.pi / 2 - 2 * np.pi * c0 / 1200 - np.pi * dc / 1200
            return ctr + R * 1.42 * np.array([np.cos(a), np.sin(a), 0])

        lf = T(f"纯五度 3:2 = {f:.2f}c", font_size=24, color=C_PYTH).move_to(mid_pt(0, f))
        lp = T(f"纯四度 4:3 = {p:.2f}c", font_size=24, color=C_JUST).move_to(mid_pt(f, p))
        self.play(FadeIn(lf), FadeIn(lp))

        bottom = T("转位：五度 ↔ 四度，三度 ↔ 六度；两段之和 = 1200c = 八度",
                   font_size=28, color=C_HL).to_edge(DOWN, buff=0.6)
        self.play(FadeIn(bottom))
        self.wait(1.3)
