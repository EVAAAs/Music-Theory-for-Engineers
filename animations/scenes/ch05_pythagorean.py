# -*- coding: utf-8 -*-
"""Ch5 五度相生律：螺旋 12 步接近闭合，缺口 = 毕氏音差 23.46c。"""
import numpy as np
from manim import *
from common import T, C_TITLE, C_PYTH, C_DRIFT, C_GRID, C_SUB

FIFTH = 701.955  # 纯五度 3:2 = 1200·log2(3/2) ≈ 701.96c（单一数据源见 demo_07）


class PythagoreanComma(Scene):
    def construct(self):
        title = T("12 个纯五度 ≈ 7 个八度，多出 23.46 音分（毕氏音差）",
                  font_size=36, color=C_TITLE)
        title.to_edge(UP, buff=0.35)
        self.play(FadeIn(title))

        x0, y0 = -4.0, 2.9
        w, v = 3.1, 0.55   # 每八度的宽、高

        def xy(n):
            p = FIFTH * n
            octv = int(p // 1200)
            return np.array([x0 + (p - 1200 * octv) / 1200 * w, y0 - octv * v, 0.0])

        ticks = VGroup(*[
            Line(np.array([x0 - 0.14, y0 - o * v, 0]),
                 np.array([x0 + 0.14, y0 - o * v, 0]),
                 color=C_GRID, stroke_width=3)
            for o in range(8)])
        self.play(Create(ticks))
        self.add(T("竖线 = 每个八度的 C", font_size=22, color=C_SUB)
                 .next_to(ticks, DOWN, buff=0.3))

        dots = [Dot(xy(n), radius=0.09, color=C_PYTH) for n in range(13)]
        self.play(FadeIn(dots[0], scale=2))
        for n in range(1, 13):
            self.play(Create(Line(xy(n - 1), xy(n), color=C_PYTH, stroke_width=3)),
                      FadeIn(dots[n]), run_time=0.25)

        # 缺口：第 12 步回到“C”时，高出第 7 个八度的刻度 23.46c
        gap = Line(xy(12), np.array([x0, y0 - 7 * v, 0]),
                   color=C_DRIFT, stroke_width=6)
        self.play(Create(gap))
        lab = T("毕氏音差\n23.46c", font_size=24, color=C_DRIFT)
        lab.next_to(xy(12), RIGHT, buff=0.12)
        self.play(FadeIn(lab))
        note = T("五度相生律转不过头：12 步到不了原 C", font_size=26, color=C_SUB)
        note.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(note))
        self.wait(1.2)
