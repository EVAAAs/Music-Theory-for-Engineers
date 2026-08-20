# -*- coding: utf-8 -*-
"""Ch9 Plomp–Levelt 粗糙度曲线：第二音从 0 滑到 1200c；
小二度峰、五度/八度低谷、三全音局部峰。"""
import numpy as np
from manim import *
from common import T, project_common, C_TITLE, C_HL, C_DRIFT, C_GRID, C_SUB, C_NOTE

proj = project_common()
CENTS, ROUGH = proj.roughness_curve()

# 关键读数（与 demo_09 --print-tables 同源）
MARKS = [(111.73, "小二度"), (600.0, "三全音"),
         (701.96, "纯五度"), (1200.0, "纯八度")]


class RoughnessCurve(Scene):
    def construct(self):
        title = T("协和 = 低粗糙度：两音越近越糙，完全重合又光滑", font_size=36, color=C_TITLE)
        title.to_edge(UP, buff=0.3)
        self.play(FadeIn(title))

        # 上部：粗糙度曲线
        ax = Axes(
            x_range=[0, 1200, 200], y_range=[0, 1.5, 0.25],
            x_length=9.4, y_length=2.5,
            x_axis_config={"include_numbers": False, "include_tip": False,
                           "stroke_color": C_GRID},
            y_axis_config={"include_numbers": False, "include_tip": False,
                           "stroke_color": C_GRID},
        ).shift(UP * 0.7)
        self.play(Create(ax))
        self.add(T("两音间隔（音分）", font_size=20, color=C_SUB)
                 .next_to(ax, DOWN, buff=0.05).shift(RIGHT * 2.4))
        self.add(T("粗糙度", font_size=20, color=C_SUB)
                 .next_to(ax, LEFT, buff=0.15))

        curve = ax.plot(lambda c: np.interp(c, CENTS, ROUGH), color=C_NOTE, stroke_width=3)
        self.play(Create(curve, run_time=1.5))

        # 底部：滑动双音
        y_bot = -2.5
        base = Line(np.array([-4.5, y_bot, 0]), np.array([4.5, y_bot, 0]),
                    color=C_GRID, stroke_width=4)
        self.play(Create(base))
        self.add(T("0c", font_size=20, color=C_SUB).next_to(np.array([-4.5, y_bot, 0]), DOWN, buff=0.1))
        self.add(T("1200c", font_size=20, color=C_SUB).next_to(np.array([4.5, y_bot, 0]), DOWN, buff=0.1))

        c_fix = Dot(np.array([-4.5, y_bot, 0]), radius=0.1, color=C_TITLE)
        slider = ValueTracker(0)

        def slid_pos():
            return np.array([-4.5 + slider.get_value() / 1200 * 9.0, y_bot, 0])

        slid_dot = always_redraw(lambda: Dot(slid_pos(), radius=0.1, color=C_DRIFT))
        cursor = always_redraw(lambda: Dot(
            ax.c2p(slider.get_value(), np.interp(slider.get_value(), CENTS, ROUGH)),
            radius=0.09, color=C_HL))
        vline = always_redraw(lambda: DashedLine(
            cursor.get_center(), slid_pos(), color=C_SUB, stroke_width=2))

        self.play(FadeIn(c_fix), FadeIn(slid_dot), FadeIn(cursor), FadeIn(vline))
        self.add(T("220 Hz", font_size=22, color=C_TITLE)
                 .next_to(np.array([-4.5, y_bot, 0]), UP, buff=0.15))

        # 依次滑到关键点并标注
        for c_target, name in MARKS:
            self.play(slider.animate.set_value(c_target), run_time=2.0)
            v = np.interp(c_target, CENTS, ROUGH)
            lab = T(f"{name}  {v:.2f}", font_size=24, color=C_HL)
            lab.move_to(ax.c2p(c_target, v)).shift(UP * 0.6)
            self.play(FadeIn(lab))
            self.wait(0.5)
        self.wait(0.8)
