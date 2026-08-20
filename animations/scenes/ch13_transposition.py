# -*- coding: utf-8 -*-
"""Ch13 移调：T_λ 是频率轴上的精确平移。
平均律下平移必落格（格子封闭）；纯律下格子不封闭，平移出现漂移（最多 21.51c）。"""
import numpy as np
from manim import *
from common import T, project_common, C_TITLE, C_ET, C_JUST, C_HL, C_DRIFT, C_GRID, C_SUB

proj = project_common()
TEMP = proj.TEMP


def melody_cents(temperament):
    # 小星星 C C G G A A G（同 demo_13）
    return [TEMP[temperament][p] for p in (0, 0, 7, 7, 9, 9, 7)]


class Transposition(Scene):
    def construct(self):
        title = T("移调 = 把整段旋律在频率轴上平移", font_size=40, color=C_TITLE)
        title.to_edge(UP, buff=0.3)
        self.play(FadeIn(title))

        x0, w = -4.6, 8.8
        y_m = -0.6

        def xpos(c):
            return x0 + c / 2400 * w

        def grid_ticks(pts, y):
            return VGroup(*[Line(np.array([xpos(c), y - 0.08, 0]),
                                 np.array([xpos(c), y + 0.08, 0]),
                                 color="#39424f", stroke_width=2)
                            for c in pts])

        def draw_melody(cents, color):
            dots = []
            for c in cents:
                p = np.array([xpos(c), y_m, 0])
                dots.append(Dot(p, radius=0.11, color=color))
            for d in dots:
                self.play(FadeIn(d), run_time=0.2)
            for a, b in zip(dots, dots[1:]):
                self.play(Create(Line(a.get_center(), b.get_center(),
                                      color=color, stroke_width=3)), run_time=0.2)
            return dots

        # ---------- 平均律：平移必落格 ----------
        ET = [100 * p for p in range(12)]
        GRID_ET = ET + [e + 1200 for e in ET]
        self.play(FadeIn(grid_ticks(GRID_ET, y_m)))
        cap_et = T("平均律格（每格 100c）", font_size=24, color=C_SUB)
        cap_et.next_to(np.array([xpos(0), y_m, 0]), UP, buff=0.35)
        self.add(cap_et)

        melody_et = melody_cents("equal")
        dots_et = draw_melody(melody_et, C_ET)
        self.wait(0.4)

        shifted_et = [c + 200 for c in melody_et]
        self.play(Transform(VGroup(*dots_et),
                            VGroup(*[d.copy().move_to(np.array([xpos(c2), y_m, 0]))
                                     for d, c2 in zip(dots_et, shifted_et)])),
                  run_time=1.0)
        hl = VGroup(*[Line(np.array([xpos(c), y_m - 0.35, 0]),
                           np.array([xpos(c), y_m + 0.35, 0]),
                           color=C_HL, stroke_width=5) for c in shifted_et])
        self.play(FadeIn(hl))
        lab_ok = T("平移 +200c：每个音都精确落在格上", font_size=28, color=C_HL)
        lab_ok.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(lab_ok))
        self.wait(0.9)
        self.play(FadeOut(VGroup(*dots_et)), FadeOut(hl),
                  FadeOut(lab_ok), FadeOut(cap_et))

        # ---------- 纯律：格子平移不自洽 ----------
        JUST = [TEMP["just"][p] for p in range(12)]
        GRID_J = JUST + [g + 1200 for g in JUST]

        def nearest(g):
            return min(GRID_J, key=lambda x: abs(x - g))

        self.play(FadeIn(grid_ticks(GRID_J, y_m)))
        cap_j = T("纯律 12 音格（5-limit）", font_size=24, color=C_SUB)
        cap_j.next_to(np.array([xpos(0), y_m, 0]), UP, buff=0.35)
        self.add(cap_j)

        # 平移 ×9/8（+203.91c）：整格平移后，有的音落不回原格
        shift = JUST[2]
        shifted_j = [c + shift for c in JUST]
        moved = VGroup(*[Dot(np.array([xpos(c2), y_m, 0]), radius=0.09, color=C_TITLE)
                          for c2 in shifted_j])
        self.play(FadeIn(moved))

        offs = [abs(c2 - nearest(c2)) for c2 in shifted_j]
        drifts = VGroup()
        for c2, off in zip(shifted_j, offs):
            if off > 2.0:
                a = np.array([xpos(c2), y_m - 0.32, 0])
                b = np.array([xpos(nearest(c2)), y_m - 0.32, 0])
                drifts.add(Line(a, b, color=C_DRIFT, stroke_width=5))
        self.play(FadeIn(drifts))
        lab_drift = T(f"平移 +{shift:.2f}c：格子不封闭，漂移最多 {max(offs):.2f}c",
                      font_size=28, color=C_DRIFT)
        lab_drift.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(lab_drift))
        self.wait(1.2)
