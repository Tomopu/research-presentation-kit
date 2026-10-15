#!/usr/bin/env python3
"""論文ゼミ（2026-10-14）: Trinh & Combes (2021) Randomized Selfish KL-UCB の発表資料。

    python build_1014.py fig ../論文ゼミ_泉1014.pptx

本体は parts/ の 6 つのファイル（共通部分と各部）。図の一部は本人の過去資料
（論文ゼミ_泉0421.pptx、泉知成_修論中間発表スライド.pptx）から Slide.paste() で複製する。
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
for part in ("p0_head", "p1_intro", "p2_algo", "p3_exp", "p4_comp", "p5_why"):
    with open(os.path.join(HERE, "parts", part + ".py"), encoding="utf-8") as f:
        exec(compile(f.read(), part + ".py", "exec"))
