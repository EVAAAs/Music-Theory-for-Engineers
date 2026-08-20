# 随书动画（Manim）

每章一个 3b1b 风格 Manim 场景，把「频率的语言」画出来：

| 场景文件 | 场景类 | 内容 |
|---|---|---|
| `scenes/ch01_standing_waves.py` | `StandingWaves` | 两端固定弦的本征模 n=1..4，fₙ = n·f₁ |
| `scenes/ch02_fourier_timbre.py` | `FourierTimbre` | 方波 = 奇次谐波 1,3,5,7… 的叠加；音色 = 频谱 |
| `scenes/ch03_log_frequency.py` | `LogFrequency` | 同样的音程，线性轴不等距、对数轴等距 |
| `scenes/ch04_just_intonation.py` | `JustIntonation` | ×3/2 与 ×5/4 二维格；同一个 E 差一个普通音差 |
| `scenes/ch05_pythagorean.py` | `PythagoreanComma` | 12 个纯五度 ≈ 7 个八度，缺口 23.46c |
| `scenes/ch06_equal_temperament.py` | `EqualTemperament` | 12 等距点；为什么是 12（收敛子 7/12） |
| `scenes/ch07_comparing.py` | `ComparingTemperaments` | 三律 12 音偏差：五度公共、三度分歧 |
| `scenes/ch08_intervals.py` | `IntervalsInversion` | 转位 = 互补比；五度 + 四度 = 八度 |
| `scenes/ch09_roughness.py` | `RoughnessCurve` | Plomp–Levelt 粗糙度曲线随双音滑动 |
| `scenes/ch10_chords.py` | `ChordsHarmonics` | 谐波梳重合；属七的三音是 16:9 而非 7:4 |
| `scenes/ch11_scales_modes.py` | `ScalesAndModes` | 大调/五声步型；换主音 = 转调式 |
| `scenes/ch12_circle_of_fifths.py` | `CircleOfFifths` | Z12 五度圈 +7 生成元；关系大小调 |
| `scenes/ch13_transposition.py` | `Transposition` | 平均律移调必落格；纯律格不封闭（21.51c） |
| `scenes/ch14_rhythm.py` | `RhythmMeter` | 时间格、切分、三连音、BPM 时间轴缩放 |
| `scenes/ch15_melody_f0.py` | `MelodyF0` | 旋律 = F0(t)；谐波梳升降；导音解决 |

## 运行环境

动画不依赖项目 `.venv`，用独立的 micromamba 环境（内含 manim + ffmpeg）：

```bash
micromamba create -p ~/.manim-envs/musicKnowledge -c conda-forge manim -y
# 若环境里没有 Noto Sans SC，把它放到 ~/.local/share/fonts/ 后刷新字体缓存
```

## 渲染

```bash
# 渲染单个场景（720p/30fps，产物在 animations/media/）
micromamba run -p ~/.manim-envs/musicKnowledge manim render -qm \
    --media_dir animations/media animations/scenes/ch01_standing_waves.py StandingWaves

# 渲染全部 15 个
for f in animations/scenes/ch*.py; do
  scene=$(grep -oP '^class \K[A-Za-z]+' "$f" | head -1)
  micromamba run -p ~/.manim-envs/musicKnowledge manim render -qm \
      --media_dir animations/media "$f" "$scene"
done
```

## 约定

- 全部文字用 `Text`（Pango），字体统一 Noto Sans SC；数学公式用 Unicode 符号
  （×、→、≈、f₁ 等，下标由 Pango 回退到 DejaVu Sans），**不用 LaTeX**（环境未装 texlive）。
- 调色板、频率常量与数值（三律 cents、粗糙度曲线、漂移量）取自 `scenes/common.py`，
  其中 `project_common()` 直接加载项目根 `common.py`（单一数据源），与正文/演示一致。
- `media/` 是运行时输出，可加入 `.gitignore`。
