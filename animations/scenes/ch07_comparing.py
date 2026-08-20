# -*- coding: utf-8 -*-
"""Ch7 三律对比：以平均律为 0 基准，画 12 个音的偏差；
五度（G、D）近乎公共，三度/六度（E、A）分歧最大。"""
import numpy as np
from manim import *
from common import (T, project_common, C_TITLE, C_PYTH, C_JUST,
                    C_HL, C_GRID, C_SUB)

proj = project_common()
TEMP = proj.TEMP
NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


class ComparingTemperaments(Scene):
    def construct(self):
        title = T("三种音律：以平均律为基准，看 12 个音的偏差", font_size=38, color=C_TITLE)
        title.to_edge(UP, buff=0.35)
        self.play(FadeIn(title))

        x0, xw = -4.6, 8.4
        y0 = 0.35
        def xpos(pc): return x0 + pc / 12 * xw
        def ydev(dev): return y0 + dev / 25.0 * 1.2

        base = Line(np.array([x0, y0, 0]), np.array([x0 + xw, y0, 0]),
                    color=C_GRID, stroke_width=4)
        self.play(Create(base))
        self.add(T("平均律 = 0 基准", font_size=22, color=C_SUB)
                 .next_to(base, RIGHT, buff=0.12))

        et = [TEMP["equal"][p] for p in range(12)]
        pyth = [TEMP["pyth"][p] for p in range(12)]
        just = [TEMP["just"][p] for p in range(12)]

        for pc in range(12):
            xp = xpos(pc)
            self.add(Line(np.array([xp, y0 - 0.07, 0]), np.array([xp, y0 + 0.07, 0]),
                          color="#39424f", stroke_width=3))
            self.add(T(NAMES[pc], font_size=18, color=C_SUB)
                     .next_to(np.array([xp, y0 - 0.07, 0]), DOWN, buff=0.1))

        def seg(pc, dev, color):
            return Line(np.array([xpos(pc), y0, 0]),
                        np.array([xpos(pc), ydev(dev), 0]),
                        color=color, stroke_width=4)

        pyth_segs = VGroup(*[seg(pc, pyth[pc] - et[pc], C_PYTH) for pc in range(12)])
        just_segs = VGroup(*[seg(pc, just[pc] - et[pc], C_JUST) for pc in range(12)])
        self.play(FadeIn(pyth_segs, lag_ratio=0.1))
        self.wait(0.2)
        self.play(FadeIn(just_segs, lag_ratio=0.1))
        self.wait(0.3)

        # 图例
        leg = VGroup(
            T("五度相生律", font_size=24, color=C_PYTH),
            T("纯律", font_size=24, color=C_JUST),
        ).arrange(RIGHT, buff=0.8).to_corner(DR, buff=0.8)
        self.play(FadeIn(leg))

        # 高亮：E（分歧最大）与 G（公共）
        for pc, dx in [(4, -0.7), (7, 0.2)]:
            p = np.array([xpos(pc) + dx, y0, 0])
            self.add(T(NAMES[pc], font_size=26, color=C_HL).next_to(p, DOWN, buff=0.45))
        e_note = T("E：+7.82c / −13.69c（分歧最大）", font_size=26, color=C_HL)
        e_note.next_to(np.array([xpos(4), y0, 0]), UP, buff=0.5)
        self.play(FadeIn(e_note))
        g_note = T("G：五度几乎公共（+1.96 / +1.96）", font_size=26, color=C_HL)
        g_note.next_to(np.array([xpos(7), y0, 0]), UP, buff=1.0)
        self.play(FadeIn(g_note))
        self.wait(1.4)
