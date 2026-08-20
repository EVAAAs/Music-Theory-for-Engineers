# -*- coding: utf-8 -*-
"""Ch14 节奏与速度：时间格；切分 = 离格；三连音 = 一拍三等分；BPM = 时间轴缩放。"""
import numpy as np
from manim import *
from common import T, C_TITLE, C_HL, C_NOTE, C_GRID, C_SUB, C_DRIFT


class RhythmMeter(Scene):
    def construct(self):
        title = T("节奏 = 时间格上的位置", font_size=40, color=C_TITLE)
        title.to_edge(UP, buff=0.3)
        self.play(FadeIn(title))

        y_axis = -0.4
        beat = 1.3
        x_left = -2.6

        axis = Line(LEFT * 3.0, RIGHT * 3.0, color=C_GRID, stroke_width=4)
        axis.shift(DOWN * 0.4)
        self.play(Create(axis))
        grid = VGroup()
        for i in range(5):
            x = x_left + i * beat
            grid.add(Line(np.array([x, y_axis - 0.15, 0]), np.array([x, y_axis + 0.15, 0]),
                          color=C_GRID, stroke_width=3))
        self.play(FadeIn(grid))
        for i in range(1, 5):
            self.add(T(str(i), font_size=22, color=C_SUB)
                     .next_to(np.array([x_left + i * beat, y_axis, 0]), DOWN, buff=0.1))

        # 正拍音符
        notes = []
        for i in range(4):
            x = x_left + (i + 1) * beat
            r = Rectangle(width=0.42, height=0.8, stroke_width=0,
                          fill_opacity=0.95, fill_color=C_NOTE)
            r.move_to(np.array([x, y_axis + 0.4, 0]))
            notes.append(r)
            self.play(FadeIn(r, scale=0.5), run_time=0.25)
        self.wait(0.3)

        # 切分
        cap = T("切分：把第 2 个音挪到两拍之间", font_size=28, color=C_HL).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(cap))
        self.play(notes[1].animate.shift(LEFT * beat / 2), run_time=0.8)
        self.play(notes[1].animate.set_color(C_DRIFT))
        self.wait(0.7)
        self.play(notes[1].animate.shift(RIGHT * beat / 2).set_color(C_NOTE),
                  FadeOut(cap))

        # 三连音
        cap2 = T("三连音：一拍三等分（非 2 的幂）", font_size=28, color=C_HL).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(cap2))
        x3 = x_left + 3 * beat
        br = Brace(Line(np.array([x3, y_axis, 0]),
                        np.array([x3 + beat, y_axis, 0])), UP, buff=0.1)
        self.play(FadeIn(br))
        trip = VGroup(br)
        for k in range(3):
            xx = x3 + k * beat / 3
            r = Rectangle(width=0.22, height=0.8, stroke_width=0,
                          fill_opacity=0.9, fill_color=C_HL)
            r.move_to(np.array([xx, y_axis + 0.4, 0]))
            trip.add(r)
            self.play(FadeIn(r), run_time=0.2)
        t3 = T("3", font_size=26, color=C_HL).next_to(br, UP, buff=0.05)
        self.add(t3)
        trip.add(t3)
        self.wait(0.7)
        self.play(FadeOut(cap2), FadeOut(trip))

        # 速度：时间轴压缩
        cap3 = T("BPM 翻倍 = 时间轴压缩一半", font_size=28, color=C_HL).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(cap3))
        grp = VGroup(axis, grid, *notes)
        self.play(grp.animate.scale(0.5, about_point=np.array([x_left, y_axis, 0])),
                  run_time=1.2)
        self.wait(1.0)
