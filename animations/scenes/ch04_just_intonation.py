# -*- coding: utf-8 -*-
"""Ch4 纯律：×3/2（五度）与 ×5/4（大三度）张开二维格；
五度链上的 E（81/64）与直接取的 E（5/4）相差一个普通音差 81:80 = 21.51c。"""
import numpy as np
from manim import *
from common import (T, project_common, C_TITLE, C_PYTH, C_JUST,
                    C_GRID, C_SUB, C_DRIFT)

proj = project_common()
rtc = proj.ratio_to_cents
PX, PY = 1.45, 1.3   # 格距


class JustIntonation(Scene):
    def construct(self):
        title = T("纯律：五度与三度张开二维格", font_size=40, color=C_TITLE)
        title.to_edge(UP, buff=0.35)
        self.play(FadeIn(title))

        O = np.array([-3.6, 1.7, 0.0])

        def pt(a, b):
            return O + np.array([a * PX, -b * PY, 0.0])

        # 坐标轴
        hx = Line(O + np.array([-0.5, 0.3, 0]), O + np.array([6.4, 0.3, 0]),
                  color=C_GRID, stroke_width=3)
        vx = Line(O + np.array([-0.5, 0.3, 0]), O + np.array([-0.5, -3.2, 0]),
                  color=C_GRID, stroke_width=3)
        self.play(Create(hx), Create(vx))
        self.add(T("×3/2（纯五度）", font_size=24, color=C_SUB).next_to(hx, DOWN, buff=0.06))
        self.add(T("×5/4（大三度）", font_size=24, color=C_SUB).next_to(vx, LEFT, buff=0.06))

        grid = VGroup(*[Dot(pt(a, b), radius=0.04, color="#39424f")
                        for a in range(5) for b in range(3)])
        self.play(FadeIn(grid))

        self.play(FadeIn(Dot(pt(0, 0), radius=0.13, color=C_TITLE)))
        for a in range(1, 5):
            self.play(FadeIn(Dot(pt(a, 0), radius=0.11, color=C_PYTH)), run_time=0.3)
        self.play(FadeIn(Dot(pt(0, 1), radius=0.11, color=C_JUST)))

        def lab(s, p, c):
            return T(s, font_size=22, color=c).next_to(p, UP, buff=0.08)
        self.add(lab("C  1/1", pt(0, 0), C_TITLE))
        self.add(lab("G  3/2", pt(1, 0), C_PYTH))
        self.add(lab("D  9/8", pt(2, 0), C_PYTH))
        self.add(lab("A  27/16", pt(3, 0), C_PYTH))
        self.add(lab(f"E  81/64 = {rtc(81/64):.2f}c", pt(4, 0), C_PYTH))
        self.add(lab(f"E  5/4 = {rtc(5/4):.2f}c", pt(0, 1), C_JUST))
        self.wait(0.6)

        # 底部：同音名 E 的两个值
        e1 = Dot(np.array([-2.6, -3.3, 0]), radius=0.12, color=C_PYTH)
        e2 = Dot(np.array([0.2, -3.3, 0]), radius=0.12, color=C_JUST)
        self.play(FadeIn(e1), FadeIn(e2))
        self.add(T(f"E（相生）{rtc(81/64):.2f}c", font_size=24, color=C_PYTH)
                 .next_to(e1, UP, buff=0.1))
        self.add(T(f"E（纯律）{rtc(5/4):.2f}c", font_size=24, color=C_JUST)
                 .next_to(e2, UP, buff=0.1))
        br = Brace(Line(e1.get_center(), e2.get_center()), DOWN, buff=0.15)
        self.play(FadeIn(br))
        self.add(T(f"普通音差 81:80 = {rtc(81/80):.2f}c", font_size=26, color=C_DRIFT)
                 .next_to(br, DOWN, buff=0.1))
        self.wait(1.3)
