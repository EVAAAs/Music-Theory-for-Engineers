# -*- coding: utf-8 -*-
"""Ch15 旋律：F0(t) 时频折线；谐波梳随 F0 一起升降（频谱图直觉）；
导音（1100c）扑向主音（1200c）——吸引子。"""
import numpy as np
from manim import *
from common import T, C_TITLE, C_HL, C_NOTE, C_GRID, C_SUB, C_DRIFT

# 小星星 F0（音分，相对 C），末段回到主音 C
SEQ = [(0, 0), (1, 0), (2, 700), (3, 700), (4, 900), (5, 900), (6, 700), (7, 1200)]


class MelodyF0(Scene):
    def construct(self):
        title = T("旋律 = 音高 F0(t) 随时间画出的折线", font_size=38, color=C_TITLE)
        title.to_edge(UP, buff=0.3)
        self.play(FadeIn(title))

        # 旋律坐标系
        ax = Axes(
            x_range=[0, 7, 1], y_range=[0, 3200, 400],
            x_length=8.0, y_length=3.4,
            x_axis_config={"include_numbers": False, "include_tip": False,
                           "stroke_color": C_GRID},
            y_axis_config={"include_numbers": False, "include_tip": False,
                           "stroke_color": C_GRID},
        ).shift(DOWN * 0.3)
        self.play(Create(ax))
        self.add(T("时间 t", font_size=20, color=C_SUB).next_to(ax, DOWN, buff=0.08))
        self.add(T("音高（相对 C 的音分）", font_size=20, color=C_SUB)
                 .next_to(ax, LEFT, buff=0.12))

        segs = VGroup()
        for (t0, c0), (t1, c1) in zip(SEQ, SEQ[1:]):
            segs.add(Line(ax.c2p(t0, c0), ax.c2p(t1, c1), color=C_NOTE, stroke_width=4))
        for seg in segs:
            self.play(Create(seg), run_time=0.25)

        # 频谱图直觉：F0 与它的谐波一起移动
        note3 = T("频谱图：f0 与 2f0、3f0 的谐波梳一起升降", font_size=26, color=C_SUB)
        note3.to_edge(UP, buff=0.6)
        self.play(FadeIn(note3))
        playhead = ValueTracker(0)

        def f0at(t):
            i = min(int(np.clip(t, 0, 6.9)), 6)
            return SEQ[i][1]

        ph = always_redraw(lambda: DashedLine(
            ax.c2p(playhead.get_value(), 0), ax.c2p(playhead.get_value(), 3200),
            color=C_SUB, stroke_width=2))
        stack = always_redraw(lambda: VGroup(*[
            Dot(ax.c2p(playhead.get_value(), f0at(playhead.get_value()) + o),
                radius=0.06, color=c)
            for o, c in [(0, C_NOTE), (1200, C_HL), (1902, C_DRIFT)]]))
        self.play(FadeIn(ph), FadeIn(stack))
        self.play(playhead.animate.set_value(7), run_time=3.2, rate_func=linear)
        self.play(FadeOut(ph), FadeOut(stack), FadeOut(note3))

        # 导音解决（换景）
        self.play(FadeOut(ax), FadeOut(segs))
        cap = T("导音：1100c 处的 B 像被磁铁吸住一样扑向主音 C（1200c）",
                font_size=26, color=C_HL).to_edge(DOWN, buff=0.3)
        self.play(FadeIn(cap))
        d1 = Dot(np.array([-1.8, 0.2, 0]), radius=0.12, color=C_HL)
        d2 = Dot(np.array([1.4, 0.2, 0]), radius=0.12, color=C_TITLE)
        self.play(FadeIn(d1), FadeIn(d2))
        self.add(T("导音 B（1100c）", font_size=24, color=C_HL).next_to(d1, UP, buff=0.12))
        self.add(T("主音 C（1200c）", font_size=24, color=C_TITLE).next_to(d2, UP, buff=0.12))
        arr = Arrow(d1.get_center(), d2.get_center(), color=C_HL, buff=0.25)
        self.play(Create(arr))
        self.wait(1.3)
