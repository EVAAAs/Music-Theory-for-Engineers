# -*- coding: utf-8 -*-
"""Ch12 五度圈：Z12 群里 +7（纯五度）生成元走遍 12 调；
关系大小调 = 同一组音、主音不同（C 大调 ↔ A 小调）。"""
import numpy as np
from manim import *
from common import T, C_TITLE, C_ET, C_HL, C_SUB, C_GRID

# 位置 k（pitch class）→ 音名，与 demo_12 的 KEY_LABEL 一致
NAME = {0: "C", 7: "G", 2: "D", 9: "A", 4: "E", 11: "B",
        6: "F#", 1: "Db", 8: "Ab", 3: "Eb", 10: "Bb", 5: "F"}


class CircleOfFifths(Scene):
    def construct(self):
        title = T("五度圈：每次 +7 个半音（纯五度），走 12 步回到 C",
                  font_size=36, color=C_TITLE)
        title.to_edge(UP, buff=0.3)
        self.play(FadeIn(title))

        ctr = np.array([0.0, 0.4, 0.0])
        R = 2.5
        circ = Circle(radius=R, color=C_GRID, stroke_width=3).move_to(ctr)
        self.play(Create(circ))

        def pos(pc):
            a = np.pi / 2 - 2 * np.pi * pc / 12
            return ctr + R * np.array([np.cos(a), np.sin(a), 0])

        def out(p):
            return (p - ctr) / np.linalg.norm(p - ctr)

        for pc in range(12):
            p = pos(pc)
            self.add(Dot(p, radius=0.035, color="#39424f"))
            self.add(T(NAME[pc], font_size=22, color=C_SUB)
                     .next_to(p, out(p), buff=0.32))

        # 五度步进：0 → 7 → 2 → … → 5 → 0
        self.play(FadeIn(Dot(pos(0), radius=0.15, color=C_HL)))
        pc = 0
        for _ in range(11):
            nxt = (pc + 7) % 12
            self.play(Create(Line(pos(pc), pos(nxt), color=C_ET, stroke_width=4)),
                      FadeIn(Dot(pos(nxt), radius=0.15, color=C_HL)),
                      run_time=0.35)
            pc = nxt
        self.play(Create(Line(pos(5), pos(0), color=C_ET, stroke_width=4)),
                  run_time=0.5)
        self.wait(0.5)

        # 关系大小调：同音列，主音 C → A
        title2 = T("关系大小调：同一组音，主音不同（C 大调 = A 小调）",
                   font_size=32, color=C_HL)
        title2.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(title2))
        tri = Triangle(color=C_HL, fill_opacity=0.9, fill_color=C_HL).scale(0.16)
        tri.move_to(pos(0) + out(pos(0)) * 0.4)
        self.play(FadeIn(tri))
        self.wait(0.6)
        self.play(tri.animate.move_to(pos(9) + out(pos(9)) * 0.4), run_time=1.2)
        self.wait(1.0)
