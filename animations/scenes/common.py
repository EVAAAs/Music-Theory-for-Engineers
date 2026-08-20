# -*- coding: utf-8 -*-
"""动画共享配置：CJK 字体、调色板、常量（与全书 common.py 单一数据源对齐）。"""
import importlib.util
import os
import numpy as np
from manim import Text, config

config.background_color = "#17181c"

# 项目根 common.py 与本模块同名，用 importlib 别名加载，避免遮蔽。
_PROJ_COMMON = None


def project_common():
    """加载项目根目录 common.py（单一数据源：TEMP/cents/音名常量）。"""
    global _PROJ_COMMON
    if _PROJ_COMMON is None:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "..", "..", "common.py")
        spec = importlib.util.spec_from_file_location("proj_common", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _PROJ_COMMON = mod
    return _PROJ_COMMON


def T(s, **kw):
    """中文/数学文本：统一 Noto Sans SC；下标等由 Pango 回退到 DejaVu Sans。"""
    kw.setdefault("font", "Noto Sans SC")
    kw.setdefault("font_size", 32)
    kw.setdefault("color", "#e8e8e8")
    return Text(s, **kw)


# ---- 调色板（与全书图配色一致） ----
C_BG    = "#17181c"
C_TITLE = "#e8e8e8"
C_ET    = "#58a6ff"   # 平均律 · 蓝
C_PYTH  = "#f0883e"   # 五度相生律 · 橙
C_JUST  = "#3fb950"   # 纯律 · 绿
C_HL    = "#e3b341"   # 强调 · 黄
C_DRIFT = "#f85149"   # 误差 · 红
C_GRID  = "#6e7681"
C_SUB   = "#9da7b3"
C_NOTE  = "#39c5cf"   # 音符 · 青

# ---- 频率常量（与 common.py 一致） ----
A4 = 440.0
C4 = 261.6256
