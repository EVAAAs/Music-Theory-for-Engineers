# -*- coding: utf-8 -*-
"""Ch6 十二平均律：对数轴上 12 个等距点；
为什么是 12：log₂(3/2) 连分数收敛子 7/12 首次把纯五度误差压到 2c 内。"""
import numpy as np
from manim import *
from common import T, C_TITLE, C_ET, C_HL, C_SUB, C_GRID

NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

# log₂(3/2) 收敛子（单一数据源：demo_06 --print-tables）
CONV = [("1", "2", "101.96"), ("3", "5", "18.04"),
        ("7", "12", "1.96"), ("24", "41", "0.48"), ("31", "53", "0.07")]


class EqualTemperament(Scene):
    def construct(self):
        title = T("十二平均律：对数轴上 12 个等距点，每格 100 音分",
                  font_size=38, color=C_TITLE)
        title.to_edge(UP, buff=0.35)
        self.play(FadeIn(title))

        # Part A：等距点
        axis = Line(LEFT * 4.7, RIGHT * 4.7, color=C_GRID, stroke_width=4)
        axis.shift(UP * 1.5)
        self.play(Create(axis))
        width = 9.4
        pts = [np.array([axis.get_center()[0] + (i / 12 - 0.5) * width,
                         axis.get_center()[1], 0]) for i in range(12)]
        ticks = VGroup(*[Line(p + DOWN * 0.06, p + UP * 0.06,
                              color="#39424f", stroke_width=3) for p in pts])
        self.play(FadeIn(ticks))
        for i, p in enumerate(pts):
            self.play(FadeIn(Dot(p, radius=0.07, color=C_ET)), run_time=0.12)
            self.add(T(NAMES[i], font_size=20, color=C_SUB).next_to(p, DOWN, buff=0.14))
        self.wait(0.5)

        # Part B：为什么 12 —— 连分数收敛子
        title2 = T("为什么恰好 12 个？log₂(3/2) 的最佳有理逼近", font_size=32, color=C_HL)
        title2.to_edge(DOWN, buff=0.15)
        self.play(FadeIn(title2))

        table = VGroup()
        for p, q, err in CONV:
            frac = T(f"{p} 步 / {q} 格", font_size=27)
            errl = T(f"误差 {err}c", font_size=27)
            table.add(VGroup(frac, errl).arrange(RIGHT, buff=0.9))
        table.arrange(DOWN, buff=0.4).shift(DOWN * 1.6)
        self.play(FadeIn(table, shift=UP * 0.3))

        hl_row = table[2]
        self.play(hl_row.animate.set_color(C_HL).scale(1.15))
        note = T("12 是第一个把纯五度误差压进 2c 的选择",
                 font_size=26, color=C_HL).next_to(hl_row, RIGHT, buff=0.8)
        self.play(FadeIn(note))
        self.wait(1.3)
