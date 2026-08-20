# -*- coding: utf-8 -*-
"""Ch10 和弦 = 谐波梳：大三和弦 1:5/4:3/2 的谐波在低频段重合；
属七和弦 C–E–G–B♭ 的三音是 16:9，不是第 7 谐波 7:4，相差七音逗号 27.26c。"""
import numpy as np
from manim import *
from common import (T, project_common, C_TITLE, C_ET, C_JUST, C_PYTH,
                    C_HL, C_DRIFT, C_GRID, C_SUB)

proj = project_common()
rtc = proj.ratio_to_cents


class ChordsHarmonics(Scene):
    def construct(self):
        title = T("和弦 = 几组谐波梳在频率轴上的重合", font_size=40, color=C_TITLE)
        title.to_edge(UP, buff=0.3)
        self.play(FadeIn(title))

        x0, y_axis = -4.8, -0.2
        w_oct = 2.3

        def xpos(r):
            return x0 + np.log2(r) * w_oct

        ax_line = Line(np.array([xpos(1), y_axis, 0]), np.array([xpos(4), y_axis, 0]),
                       color=C_GRID, stroke_width=4)
        self.play(Create(ax_line))
        self.add(T("C（基频 = 1）", font_size=20, color=C_SUB)
                 .next_to(np.array([xpos(1), y_axis, 0]), DOWN, buff=0.1))
        self.add(T("×4（两八度）", font_size=20, color=C_SUB)
                 .next_to(np.array([xpos(4), y_axis, 0]), DOWN, buff=0.1))

        def add_comb(r, color, up=True):
            ticks = VGroup()
            k = 1
            while r * k <= 4.001:
                yy = y_axis + (0.55 if up else -0.55)
                xx = xpos(r * k)
                ticks.add(Line(np.array([xx, y_axis, 0]), np.array([xx, yy, 0]),
                               color=color, stroke_width=3))
                k += 1
            self.play(FadeIn(ticks, lag_ratio=0.08))
            return ticks

        combs = VGroup(add_comb(1.0, C_ET), add_comb(5 / 4, C_JUST),
                       add_comb(3 / 2, C_PYTH))

        p3 = np.array([xpos(3.0), y_axis, 0])
        self.play(FadeIn(Dot(p3, radius=0.1, color=C_HL)))
        lab = T("C 的第 3 谐波 = G 的第 2 谐波（重合）", font_size=24, color=C_HL)
        lab.next_to(p3, UP, buff=0.85)
        self.play(FadeIn(lab))
        self.wait(0.6)
        self.play(FadeOut(lab))
        self.play(FadeOut(combs))

        # 属七：16:9 与 7:4
        title2 = T("属七和弦 C–E–G–B♭：三音是 16:9，不是第 7 谐波 7:4",
                   font_size=32, color=C_HL)
        title2.to_edge(DOWN, buff=0.35)
        self.play(FadeIn(title2))

        for r, name, c in [(1, "C", C_ET), (5 / 4, "E", C_JUST),
                           (3 / 2, "G", C_PYTH), (16 / 9, "B♭", C_DRIFT)]:
            pp = np.array([xpos(r), y_axis, 0])
            self.play(FadeIn(Dot(pp, radius=0.09, color=c)))
            self.add(T(name, font_size=22, color=c).next_to(pp, UP, buff=0.15))

        p_a = np.array([xpos(16 / 9), y_axis + 1.0, 0])
        p_b = np.array([xpos(7 / 4), y_axis + 1.0, 0])
        self.play(FadeIn(Dot(p_a, radius=0.07, color=C_DRIFT)),
                  FadeIn(Dot(p_b, radius=0.07, color=C_SUB)))
        br = Brace(Line(p_b, p_a), UP, buff=0.1)
        self.play(FadeIn(br))
        self.add(T(f"七音逗号 64:63 = {rtc(64 / 63):.2f}c", font_size=24, color=C_DRIFT)
                 .next_to(br, UP, buff=0.1))
        self.wait(1.3)
