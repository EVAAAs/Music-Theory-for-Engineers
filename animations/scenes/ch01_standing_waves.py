# -*- coding: utf-8 -*-
"""Ch1 驻波：两端固定的弦，本征模 n = 1..4，f_n = n·f_1。"""
import numpy as np
from manim import *
from common import T, C_TITLE, C_HL, C_SUB, C_NOTE, C_GRID


class StandingWaves(Scene):
    def construct(self):
        title = T("两端固定的弦：驻波本征模", font_size=40, color=C_TITLE)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title, shift=DOWN * 0.2))
        self.wait(0.4)

        L = 4.2
        x0 = 0.0
        string = Line(LEFT * L / 2, RIGHT * L / 2, color=C_GRID, stroke_width=6)
        pins = VGroup(
            Dot(string.get_start(), radius=0.09, color=C_TITLE),
            Dot(string.get_end(), radius=0.09, color=C_TITLE),
        )
        self.play(Create(string), FadeIn(pins))
        self.wait(0.3)

        f1 = 110.0
        for n in (1, 2, 3, 4):
            self.show_mode(n, f1, L, x0)
        self.wait(0.6)

    def show_mode(self, n, f1, L, x0):
        phase = ValueTracker(0.0)
        A = 0.95

        def y_of(x, ph):
            return A * np.sin(n * np.pi * (x - x0 + L / 2) / L) * np.cos(ph)

        wave = always_redraw(lambda: ParametricFunction(
            lambda x: np.array([x, y_of(x, phase.get_value()), 0]),
            t_range=[x0 - L / 2, x0 + L / 2],
            color=C_NOTE, stroke_width=5,
        ))
        self.play(FadeIn(wave))
        self.play(phase.animate.set_value(2 * np.pi * 2), run_time=2.4, rate_func=linear)

        nodes = VGroup(*[
            Dot(np.array([x0 - L / 2 + k * L / n, 0, 0]), radius=0.07, color=C_HL)
            for k in range(n + 1)
        ])
        self.play(FadeIn(nodes))
        lab = T(f"n = {n}    f = {n}×{f1:.0f} Hz = {n*f1:.0f} Hz",
                font_size=28, color=C_HL)
        lab.next_to(np.array([x0, 0, 0]), DOWN, buff=0.8)
        self.play(FadeIn(lab, shift=UP * 0.2))
        self.wait(0.4)

        if n == 4:
            note = T("n 越大，节点越多、频率越高", font_size=28, color=C_SUB)
            note.next_to(lab, DOWN, buff=0.35)
            self.play(FadeIn(note))
            self.wait(0.8)
            self.play(FadeOut(note))
        self.play(FadeOut(wave), FadeOut(nodes), FadeOut(lab))
