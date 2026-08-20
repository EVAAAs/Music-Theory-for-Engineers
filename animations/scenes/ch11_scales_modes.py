# -*- coding: utf-8 -*-
"""Ch11 音阶与调式：八度内的一组离散频率；
大调步型 [2,2,1,2,2,2,1]，换主音 = 转调式（同音列）；五声 [2,2,3,2,3]。"""
import numpy as np
from manim import *
from common import T, C_TITLE, C_HL, C_NOTE, C_GRID, C_SUB

MAJOR = [2, 2, 1, 2, 2, 2, 1]
PENTA = [2, 2, 3, 2, 3]


class ScalesAndModes(Scene):
    def construct(self):
        title = T("音阶 = 八度内的一组离散频率；调式 = 换主音", font_size=38, color=C_TITLE)
        title.to_edge(UP, buff=0.3)
        self.play(FadeIn(title))

        x0, w = -4.6, 9.2

        def xpos(c):
            return x0 + c / 1200 * w

        def axis(yrow):
            return Line(np.array([x0, yrow, 0]), np.array([x0 + w, yrow, 0]),
                        color=C_GRID, stroke_width=3)

        def note_row(intervals, names, yrow):
            """画一行音阶，返回 (dots_group, cents)。"""
            ax = axis(yrow)
            self.play(Create(ax))
            cents = [0]
            for s in intervals:
                cents.append(cents[-1] + s * 100)
            grp = VGroup(ax)
            dots = []
            for i, c in enumerate(cents[:-1]):  # 末点是八度主音，不重复画
                p = np.array([xpos(c), yrow, 0])
                d = Dot(p, radius=0.11, color=C_NOTE)
                dots.append(d)
                self.play(FadeIn(d), run_time=0.15)
                t = T(names[i], font_size=24, color=C_TITLE).next_to(p, UP, buff=0.12)
                self.add(t)
                grp.add(t, d)
            for i, s in enumerate(intervals):
                mid = np.array([xpos((cents[i] + cents[i + 1]) / 2), yrow, 0])
                t = T(str(s), font_size=26, color=C_SUB).next_to(mid, DOWN, buff=0.12)
                self.add(t)
                grp.add(t)
            return grp, dots, cents

        # ---- 大调 ----
        y1 = 1.7
        major_grp, dots1, cents1 = note_row(MAJOR, ["C", "D", "E", "F", "G", "A", "B"], y1)
        cap1 = T("自然大调 [2,2,1,2,2,2,1]", font_size=26, color=C_HL)
        cap1.next_to(np.array([x0 + w / 2, y1, 0]), DOWN, buff=0.5)
        self.add(cap1)
        major_grp.add(cap1)
        self.wait(0.5)

        # ---- 调式旋转：换主音 ----
        modes = VGroup()
        tri = Triangle(color=C_HL, fill_opacity=0.9, fill_color=C_HL).scale(0.16)
        tri.next_to(np.array([xpos(cents1[0]), y1, 0]), UP, buff=0.02)
        self.play(FadeIn(tri))
        modes.add(tri)
        for target, name in [(200, "D 多利亚（第 2 级起）"),
                             (900, "A 爱奥利亚（自然小调）")]:
            self.play(tri.animate.next_to(np.array([xpos(target), y1, 0]), UP, buff=0.02),
                      run_time=1.2)
            cap = T(name, font_size=26, color=C_HL)
            cap.next_to(np.array([x0 + w / 2, y1, 0]), DOWN, buff=0.5)
            self.add(cap)
            modes.add(cap)
            self.wait(0.5)

        # ---- 五声 ----
        y2 = -2.1
        self.play(FadeOut(major_grp), FadeOut(modes))
        penta_grp, dots2, cents2 = note_row(PENTA, ["宫", "商", "角", "徵", "羽"], y2)
        cap2 = T("五声音阶 [2,2,3,2,3]", font_size=26, color=C_HL)
        cap2.next_to(np.array([x0 + w / 2, y2, 0]), DOWN, buff=0.5)
        self.add(cap2)
        self.wait(1.2)
