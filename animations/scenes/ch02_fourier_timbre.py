# -*- coding: utf-8 -*-
"""Ch2 傅里叶：方波 = 奇次谐波 1,3,5,7… 的叠加；音色 = 频谱。"""
import numpy as np
from manim import *
from common import T, C_TITLE, C_ET, C_HL, C_SUB, C_GRID


class FourierTimbre(Scene):
    def construct(self):
        title = T("音色 = 频谱：方波由奇次谐波堆叠而成", font_size=38, color=C_TITLE)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title))
        self.wait(0.3)

        f0 = 220.0
        t_span = 2.0 / f0  # 两个周期

        x_axes = Axes(
            x_range=[0, t_span, t_span / 8],
            y_range=[-1.4, 1.4, 0.5],
            x_length=5.6, y_length=3.4,
            x_axis_config={"include_numbers": False, "include_tip": False,
                           "stroke_color": C_GRID},
            y_axis_config={"include_numbers": False, "include_tip": False,
                           "stroke_color": C_GRID},
        ).to_corner(UL, buff=0.7)
        self.add(x_axes)
        xlab = T("时间 t", font_size=24, color=C_SUB).next_to(x_axes, DOWN, buff=0.25)
        self.add(xlab)

        n_harm = ValueTracker(0)

        def sq(t):
            total = 0.0
            for k in (1, 3, 5, 7):
                if k <= 2 * int(n_harm.get_value()) - 1:
                    total += (1.0 / k) * np.sin(2 * np.pi * k * f0 * t)
            return total

        curve = always_redraw(lambda: x_axes.plot(sq, color="#e8e8e8", stroke_width=3))
        self.play(FadeIn(curve))
        self.wait(0.4)

        # 频谱轴：横轴 = 谐波序号，纵轴 = 幅度
        s_axes = Axes(
            x_range=[0, 8.5, 1], y_range=[0, 1.15, 0.25],
            x_length=5.6, y_length=3.4,
            x_axis_config={"include_numbers": False, "include_tip": False,
                           "stroke_color": C_GRID},
            y_axis_config={"include_numbers": False, "include_tip": False,
                           "stroke_color": C_GRID},
        ).to_corner(UR, buff=0.7)
        s_axes.shift(DOWN * 0.0)
        self.play(FadeIn(s_axes))
        slab = T("谐波序号 k", font_size=24, color=C_SUB).next_to(s_axes, DOWN, buff=0.25)
        self.add(slab)

        width = 0.4 * (s_axes.c2p(1, 0)[0] - s_axes.c2p(0, 0)[0])

        def add_bar(k, amp):
            bot = s_axes.c2p(k, 0)
            top = s_axes.c2p(k, amp)
            r = Rectangle(width=width, height=top[1] - bot[1],
                          stroke_width=0, fill_opacity=0.9, fill_color=C_ET)
            r.move_to(np.array([(bot[0] + top[0]) / 2, (bot[1] + top[1]) / 2, 0]))
            self.play(GrowFromCenter(r), run_time=0.4)
            return r

        for k, amp in [(1, 1.0), (3, 1 / 3), (5, 1 / 5), (7, 1 / 7)]:
            self.play(n_harm.animate.set_value((k + 1) // 2), run_time=1.0,
                      rate_func=linear)
            self.wait(0.3)
            add_bar(k, amp)

        note = T("只取奇次谐波（1,3,5,7…），波形逐渐变方",
                 font_size=28, color=C_HL).to_edge(DOWN, buff=0.6)
        self.play(FadeIn(note))
        self.wait(1.2)
