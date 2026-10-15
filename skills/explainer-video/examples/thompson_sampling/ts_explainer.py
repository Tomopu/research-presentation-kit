"""作例：Thompson Sampling と Selfish Thompson Sampling の説明動画（約 5 分 16 秒）。

    PY=~/.claude/skills/explainer-video/.venv/bin/python
    $PY ts_explainer.py preview        # 各文の終わりのコマを PNG に（ts_explainer_build/preview/）
    $PY ts_explainer.py                # 全場面を作って ts_explainer.mp4 にする
    $PY ts_explainer.py 3 5            # 場面 3 と 5 だけ作り直す

2 人の軌跡（場面 5・6）は toy.py の小さな再現。500 試行の数値（場面 7）は data/fig1_K2_M2_T1e4.csv
（mpmab-simu の outputs/exp_20261015_ts_equal/fig1_K2_M2_T1e4/summary.csv の写し）。
出典は原典で確かめた（Besson & Kaufmann 2018 の 4.1・4.2・6.3 節、Bonnefoi et al. 2017、Trinh & Combes 2021）。
"""
import math
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "scripts"))
sys.path.insert(0, HERE)
from video import *  # noqa: F401,F403  色・部品・Video
from video import Video, frame_base, which, prog, box, side_panel, wrap_ja  # noqa: F401
from toy import run as toy_run

FIG1 = os.path.join(HERE, "data", "fig1_K2_M2_T1e4.csv")
ARM_C = ["#0D114A", "#D14B46", "#196723"]          # 腕 1・2・3（場面 1・2）
ARM2_C = ["#0D114A", "#E69F00"]                    # 腕 1・2（場面 4〜6）
PL_C = ["#3B5BA9", "#196723"]                      # プレイヤー 1・2

# ------------------------------------------------------------------ 台本
# (字幕, 読み上げ)。読み上げは Kyoko が読みやすい表記にする
SCENES = [
    dict(title=None, lines=[
        ("Thompson Sampling とは何か、Selfish Thompson Sampling の論文はあるのか、"
         "そして複数のプレイヤーが並列に使うと何が起きるのかを、順に説明します。",
         "トンプソン・サンプリングとは何か、セルフィッシュ・トンプソン・サンプリングの論文はあるのか、"
         "そして、複数のプレイヤーが並列に使うと何が起きるのかを、順に説明します。"),
    ]),
    dict(title="1. Thompson Sampling の仕組み", lines=[
        ("Thompson Sampling は、1933 年に Thompson が提案した、最も古いバンディットアルゴリズムです。",
         "トンプソン・サンプリングは、1933年にトンプソンが提案した、最も古いバンディット・アルゴリズムです。"),
        ("報酬が 0 か 1 のとき、各腕の平均の見込みを Beta 分布で表します。",
         "報酬が、0か1のとき、各腕の平均の見込みを、ベータ分布で表します。"),
        ("最初は Beta(1, 1)、つまり一様分布から始めます。",
         "最初は、ベータ・いち・いち、つまり、一様分布から始めます。"),
        ("各時刻に、腕ごとに分布から乱数を 1 つ引き、最も大きい値が出た腕を引きます。",
         "各時刻に、腕ごとに、分布から乱数を1つ引き、最も大きい値が出た腕を引きます。"),
        ("報酬が 1 なら左のパラメータ α を、0 なら右のパラメータ β を 1 増やします。",
         "報酬が1なら、左のパラメータ、アルファを、0なら、右のパラメータ、ベータを、1増やします。"),
        ("これを繰り返すと、分布はしだいに細くなり、本当の平均の近くに集まっていきます。",
         "これを繰り返すと、分布はしだいに細くなり、本当の平均の近くに集まっていきます。"),
    ]),
    dict(title="なぜうまくいくのか：探索と活用", lines=[
        ("試した回数が少ない腕は分布が広いので、ときどき大きな値が出て選ばれます。これが探索です。",
         "試した回数が少ない腕は、分布が広いので、ときどき大きな値が出て、選ばれます。これが、探索です。"),
        ("多く試した良い腕は、分布が細く高い位置にあるので、ほとんどの時刻で選ばれます。これが活用です。",
         "多く試した良い腕は、分布が細く、高い位置にあるので、ほとんどの時刻で選ばれます。これが、活用です。"),
        ("2012 年に Agrawal と Goyal が後悔が対数で抑えられることを示し、同じ年に Kaufmann らが、"
         "Bernoulli 報酬では Lai と Robbins の下界に一致する、つまり漸近最適であることを示しました。",
         "2012年に、アグラワルとゴヤルが、後悔が対数で抑えられることを示し、同じ年に、カウフマンらが、"
         "ベルヌーイ報酬では、ライとロビンズの下界に一致する、つまり、漸近最適であることを示しました。"),
    ]),
    dict(title="2. Selfish Thompson Sampling の論文はあるか", lines=[
        ("では、Selfish Thompson Sampling を主題にした論文はあるのでしょうか。",
         "では、セルフィッシュ・トンプソン・サンプリングを主題にした論文は、あるのでしょうか。"),
        ("調べた範囲では、この方策の後悔を解析した論文は見つかりませんでした。",
         "調べた範囲では、この方策の後悔を解析した論文は、見つかりませんでした。"),
        ("最も近いのは、2017 年の Bonnefoi らの論文です。",
         "最も近いのは、2017年の、ボヌフォワらの論文です。"),
        ("IoT の端末が、送信が届いたことを知らせる ACK だけを見て、Thompson Sampling でチャネルを選びます。"
         "衝突すると ACK が返らないので、失敗として数えます。",
         "アイオーティーの端末が、送信が届いたことを知らせる、アックだけを見て、トンプソン・サンプリングでチャネルを選びます。"
         "衝突すると、アックが返らないので、失敗として数えます。"),
        ("中身は Selfish Thompson Sampling ですが、実験だけで、後悔の解析はありません。",
         "中身は、セルフィッシュ・トンプソン・サンプリングですが、実験だけで、後悔の解析はありません。"),
        ("次に、2018 年の Besson と Kaufmann が、この考え方を Selfish と名付けました。",
         "次に、2018年の、ベッソンとカウフマンが、この考え方を、セルフィッシュと名付けました。"),
        ("どの index 方策とも組み合わせられると書いていますが、解析と実験は UCB1 と KL-UCB だけです。",
         "どのインデックス方策とも組み合わせられると書いていますが、解析と実験は、ユーシービー・ワンと、ケーエル・ユーシービーだけです。"),
        ("そして、Selfish KL-UCB は小さな確率で衝突し続け、後悔が線形に増えると予想しました。",
         "そして、セルフィッシュ・ケーエル・ユーシービーは、小さな確率で衝突し続け、後悔が線形に増えると予想しました。"),
        ("2021 年の Trinh と Combes は、KL-UCB の index に乱数を足してこれを避けました。それが R-SKL です。"
         "Thompson Sampling 版の理論は、まだありません。",
         "2021年の、トリンとコンブは、ケーエル・ユーシービーのインデックスに乱数を足して、これを避けました。それが、アール・エス・ケー・エルです。"
         "トンプソン・サンプリング版の理論は、まだありません。"),
    ]),
    dict(title="3. 並列にすると：2 人・2 本の腕", lines=[
        ("次に、2 人のプレイヤーが、それぞれ自分の観測だけでこの方策を使うとどうなるかを見ます。",
         "次に、2人のプレイヤーが、それぞれ自分の観測だけで、この方策を使うと、どうなるかを見ます。"),
        ("腕は 2 本で、平均は 0.9 と 0.1 です。",
         "腕は2本で、平均は、0.9と、0.1です。"),
        ("2 人が同じ腕を選ぶと衝突し、2 人とも報酬は 0 になります。",
         "2人が同じ腕を選ぶと、衝突し、2人とも、報酬は0になります。"),
        ("衝突したかどうかは分からないので、衝突による 0 も、腕の失敗として数えます。",
         "衝突したかどうかは分からないので、衝突による0も、腕の失敗として数えます。"),
        ("理想は、1 人が腕 1、もう 1 人が腕 2 に分かれることです。",
         "理想は、1人が腕1、もう1人が腕2に、分かれることです。"),
    ]),
    dict(title="Selfish KL-UCB：衝突が止まらない例", lines=[
        ("まず Selfish KL-UCB です。index は観測だけで決まり、乱数を含みません。",
         "まず、セルフィッシュ・ケーエル・ユーシービーです。インデックスは、観測だけで決まり、乱数を含みません。"),
        ("この例では、2 ステップ目で、2 人の観測がたまたま同じになりました。",
         "この例では、2ステップ目で、2人の観測が、たまたま同じになりました。"),
        ("すると、その後は 2 人が毎回同じ腕を選び、そろって衝突し、そろって評価を下げ、そろって隣の腕に移ります。",
         "すると、その後は、2人が毎回、同じ腕を選び、そろって衝突し、そろって評価を下げ、そろって隣の腕に移ります。"),
        ("衝突はほぼ毎回起き、報酬はほとんど得られません。",
         "衝突は、ほぼ毎回起き、報酬は、ほとんど得られません。"),
    ]),
    dict(title="Selfish Thompson Sampling：乱数で分かれる", lines=[
        ("次に Selfish Thompson Sampling です。2 人は毎回、別々に乱数を引きます。",
         "次に、セルフィッシュ・トンプソン・サンプリングです。2人は毎回、別々に乱数を引きます。"),
        ("同じ腕に集まっても、どちらかが先に別の腕を選ぶので、2 人の観測に差が生まれます。",
         "同じ腕に集まっても、どちらかが先に別の腕を選ぶので、2人の観測に、差が生まれます。"),
        ("差が広がると、1 人は腕 1、もう 1 人は腕 2 に落ち着き、衝突は止まります。",
         "差が広がると、1人は腕1、もう1人は腕2に落ち着き、衝突は止まります。"),
        ("R-SKL が index に乱数を足したのと同じ働きを、Thompson Sampling は最初から持っています。",
         "アール・エス・ケー・エルが、インデックスに乱数を足したのと同じ働きを、トンプソン・サンプリングは、最初から持っています。"),
    ]),
    dict(title="500 回の試行で比べると", lines=[
        ("同じ設定で、1 万ステップを 500 回試しました。",
         "同じ設定で、1万ステップを、500回試しました。"),
        ("後悔が 1000 を超えた試行は、Selfish KL-UCB が 144 回、R-SKL が 0 回、Selfish TS が 1 回でした。",
         "後悔が1000を超えた試行は、セルフィッシュ・ケーエル・ユーシービーが144回、アール・エス・ケー・エルが0回、"
         "セルフィッシュ・トンプソン・サンプリングが1回でした。"),
        ("平均の後悔は、それぞれ約 1960、160、180 です。",
         "平均の後悔は、それぞれ、約1960、160、180です。"),
        ("乱数だけで R-SKL に近い効果が出ています。ただし、1 つの設定での実験で、理論の保証はありません。",
         "乱数だけで、アール・エス・ケー・エルに近い効果が出ています。ただし、1つの設定での実験で、理論の保証はありません。"),
    ]),
    dict(title="まとめ", lines=[
        ("Thompson Sampling は、事後分布から乱数を引いて最大の腕を選ぶ方策で、1 人なら漸近最適です。",
         "トンプソン・サンプリングは、事後分布から乱数を引いて、最大の腕を選ぶ方策で、1人なら、漸近最適です。"),
        ("Selfish Thompson Sampling は IoT の実験で使われていますが、後悔の理論はまだありません。",
         "セルフィッシュ・トンプソン・サンプリングは、アイオーティーの実験で使われていますが、後悔の理論は、まだありません。"),
        ("並列にすると、毎回の乱数が 2 人の対称性を崩し、Selfish KL-UCB のような衝突の連続を避けやすくなります。",
         "並列にすると、毎回の乱数が2人の対称性を崩し、セルフィッシュ・ケーエル・ユーシービーのような、衝突の連続を、避けやすくなります。"),
        ("すべての腕の平均が等しい設定と、腕の数を増やした比較は、いま計算中です。",
         "すべての腕の平均が等しい設定と、腕の数を増やした比較は、いま計算中です。"),
    ]),
]


def beta_pdf(x, a, b):
    lb = math.lgamma(a) + math.lgamma(b) - math.lgamma(a + b)
    return np.exp((a - 1) * np.log(x) + (b - 1) * np.log1p(-x) - lb)


XG = np.linspace(0.001, 0.999, 500)


# ------------------------------------------------------------------ 場面 0：表紙
def draw0(fig, t, cues, data):
    frame_base(fig, None, SCENES[0]["lines"][which(cues, t)][0])
    fig.text(0.5, 0.74, "Thompson Sampling と", fontsize=40, weight="bold", color=NAVY, ha="center")
    fig.text(0.5, 0.64, "Selfish Thompson Sampling", fontsize=40, weight="bold", color=NAVY, ha="center")
    qs = ["Thompson Sampling とは何か", "Selfish Thompson Sampling の論文はあるか", "複数のプレイヤーが並列に使うと何が起きるか"]
    for i, q in enumerate(qs):
        a = float(np.clip((t - 0.6 - 1.2 * i) / 0.5, 0, 1))
        y = 0.47 - 0.085 * i
        box(fig, 0.25, y - 0.032, 0.5, 0.064, LIGHT)
        fig.text(0.27, y, f"{i + 1}", fontsize=22, weight="bold", color=NAVY, va="center", alpha=a)
        fig.text(0.31, y, q, fontsize=20, color=INK, va="center", alpha=a)


# ------------------------------------------------------------------ 場面 1・2：1 人の Thompson Sampling
MU1 = np.array([0.7, 0.5, 0.3])


def single_ts(seed=7, T=1000):
    rng = np.random.default_rng(seed)
    a, b = np.ones(3), np.ones(3)
    hist = []
    for _ in range(T):
        s = rng.beta(a, b)
        k = int(np.argmax(s))
        r = int(rng.random() < MU1[k])
        hist.append(dict(a=a.copy(), b=b.copy(), s=s, k=k, r=r))
        a[k] += r
        b[k] += 1 - r
    hist.append(dict(a=a.copy(), b=b.copy(), s=None, k=None, r=None))
    return hist


def draw_post(ax, a, b, ymax=None, sample=None, chosen=None, true=True, fade=None):
    peak = 0
    for k in range(3):
        y = beta_pdf(XG, a[k], b[k])
        peak = max(peak, y.max())
        al = 1.0 if fade is None else fade[k]
        ax.plot(XG, y, color=ARM_C[k], lw=3 if chosen == k else 2, alpha=al)
        ax.fill_between(XG, y, color=ARM_C[k], alpha=0.10 * al)
        if true:
            ax.axvline(MU1[k], color=ARM_C[k], ls=":", lw=1.4, alpha=0.8 * al)
    ymax = ymax or max(2.0, peak * 1.12)
    ax.set_xlim(0, 1), ax.set_ylim(0, ymax)
    ax.set_xlabel("腕の平均 μ の値", fontsize=14)
    ax.set_ylabel("見込み（確率密度）", fontsize=14)
    ax.tick_params(labelsize=12)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    if sample is not None:
        for k in range(3):
            yk = beta_pdf(np.array([sample[k]]), a[k], b[k])[0]
            ax.plot([sample[k]], [yk], "o", ms=15 if k == chosen else 11, color=ARM_C[k],
                    mec=YEL if k == chosen else "white", mew=3 if k == chosen else 1.5, zorder=5)
    return ymax


def draw1(fig, t, cues, data):
    hist = data["hist"]
    i = which(cues, t)
    frame_base(fig, SCENES[1]["title"], SCENES[1]["lines"][i][0])
    ax = fig.add_axes([0.08, 0.25, 0.58, 0.57])
    # 文 0〜2：一様分布のまま。文 3〜4：1 ステップずつ（8 ステップ）。文 5：早送りで t = 1000 まで
    NSLOW = 8
    if i <= 2:
        step, phase = 0, None
    elif i <= 4:
        p = prog(cues, 3, t, 4) * NSLOW
        step = min(int(p), NSLOW - 1)
        phase = p - step if p < NSLOW else 1.0
    else:
        p = prog(cues, 5, t)
        step = int(round(NSLOW * (1000 / NSLOW) ** min(p / 0.85, 1)))
        phase = None
    h = hist[step]
    if phase is None:
        draw_post(ax, h["a"], h["b"], true=(i >= 1))
        shown = h
    elif phase < 0.6:
        draw_post(ax, h["a"], h["b"], sample=h["s"], chosen=h["k"] if phase > 0.25 else None)
        shown = h
    else:
        h2 = hist[step + 1]
        draw_post(ax, h2["a"], h2["b"], chosen=h["k"])
        shown = h2
    for k in range(3):
        ax.text(MU1[k], ax.get_ylim()[1] * 0.98, f"腕 {k + 1}", color=ARM_C[k], fontsize=13, ha="center", va="top",
                weight="bold")
    if i >= 1:
        ax.text(0.01, ax.get_ylim()[1] * 0.98, "点線：本当の平均\n（学習者には見えない）", fontsize=11, color=GRAY, va="top")
    # 右の欄
    tt = step if phase is None or phase < 0.6 else step + 1
    rows = [(f"時刻 t = {tt}", dict(fontsize=20, weight="bold", color=NAVY, dy=0.07))]
    for k in range(3):
        a_, b_ = shown["a"][k], shown["b"][k]
        rows.append((f"腕 {k + 1}：Beta({int(a_)}, {int(b_)})", dict(fontsize=16, color=ARM_C[k], weight="bold", dy=0.05)))
        rows.append((f"   引いた回数 {int(a_ + b_ - 2)}", dict(fontsize=13, color=INK, dy=0.055)))
    if phase is not None:
        k = h["k"]
        rows.append(("", dict(fontsize=8, dy=0.01)))
        rows.append(("引いた乱数：", dict(fontsize=14, color=INK, dy=0.045)))
        rows.append(("  " + "  ".join(f"{v:.2f}" for v in h["s"]), dict(fontsize=14, color=INK, dy=0.05)))
        if phase > 0.25:
            rows.append((f"→ 腕 {k + 1} を引く", dict(fontsize=16, weight="bold", color=ARM_C[k], dy=0.05)))
        if phase >= 0.6:
            rows.append((f"報酬 {h['r']} → " + ("α" if h["r"] else "β") + " を +1",
                         dict(fontsize=16, weight="bold", color=RED if h["r"] == 0 else GREEN, dy=0.05)))
    side_panel(fig, None, rows)


def draw2(fig, t, cues, data):
    hist = data["hist"]
    i = which(cues, t)
    frame_base(fig, SCENES[2]["title"], SCENES[2]["lines"][i][0])
    snap = data["snap"]
    h = hist[snap]
    ax = fig.add_axes([0.08, 0.25 if i < 2 else 0.50, 0.58, 0.57 if i < 2 else 0.32])
    fade = [1, 0.25, 1] if i == 0 else ([1, 0.25, 0.25] if i == 1 else None)
    draw_post(ax, h["a"], h["b"], fade=fade)
    ym = ax.get_ylim()[1]
    if i == 0:
        k = 2
        ax.annotate("試した回数が少ない → 広い\nときどき大きな値が出る（探索）", xy=(0.62, beta_pdf(np.array([0.62]), h["a"][k], h["b"][k])[0]),
                    xytext=(0.03, ym * 0.42), fontsize=14, color=ARM_C[k], weight="bold",
                    arrowprops=dict(arrowstyle="->", color=ARM_C[k], lw=2))
        ax.plot([0.62], [beta_pdf(np.array([0.62]), h["a"][k], h["b"][k])[0]], "o", ms=12, color=ARM_C[k], mec=YEL, mew=3)
    if i == 1:
        k = 0
        pk = XG[np.argmax(beta_pdf(XG, h["a"][k], h["b"][k]))]
        ax.annotate("多く試した良い腕 → 細く高い\nほとんどの時刻で選ばれる（活用）", xy=(pk + 0.02, ym * 0.7),
                    xytext=(0.05, ym * 0.70), fontsize=14, color=ARM_C[k], weight="bold",
                    arrowprops=dict(arrowstyle="->", color=ARM_C[k], lw=2))
    rows = [(f"時刻 t = {snap} の様子", dict(fontsize=18, weight="bold", color=NAVY, dy=0.07))]
    for k in range(3):
        rows.append((f"腕 {k + 1}：引いた回数 {int(h['a'][k] + h['b'][k] - 2)}", dict(fontsize=15, color=ARM_C[k], weight="bold", dy=0.055)))
    side_panel(fig, None, rows, y0=0.17 if i < 2 else 0.45)
    if i >= 2:
        box(fig, 0.06, 0.16, 0.91, 0.24, YEL)
        refs = [("Agrawal & Goyal (COLT 2012)", "後悔が O(log T) で抑えられることを示す"),
                ("Kaufmann, Korda & Munos (ALT 2012)", "Bernoulli 報酬で漸近最適（Lai–Robbins の下界に一致）"),
                ("Thompson (1933)", "2 つの治療法を比べる問題として提案")]
        for j, (a_, b_) in enumerate(refs):
            al = float(np.clip((t - cues[2][0]) / 0.6 - j * 0.8, 0, 1))
            fig.text(0.08, 0.34 - 0.06 * j, a_, fontsize=15, weight="bold", color=NAVY, va="center", alpha=al)
            fig.text(0.45, 0.34 - 0.06 * j, b_, fontsize=14, color=INK, va="center", alpha=al)


# ------------------------------------------------------------------ 場面 3：文献
def card(fig, x, y, w, h, year, head, body, alpha, fc="#F4F5FA", ec=NAVY):
    if alpha <= 0:
        return
    fig.add_artist(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.012", fc=fc, ec=ec, lw=1.8,
                                  transform=fig.transFigure, alpha=alpha))
    fig.text(x + 0.015, y + h - 0.035, year, fontsize=15, weight="bold", color=RED, va="center", alpha=alpha)
    fig.text(x + 0.015, y + h - 0.085, head, fontsize=15, weight="bold", color=NAVY, va="center", alpha=alpha)
    fig.text(x + 0.015, y + h - 0.125, body, fontsize=13, color=INK, va="top", linespacing=1.5, alpha=alpha)


def draw3(fig, t, cues, data):
    i = which(cues, t)
    frame_base(fig, SCENES[3]["title"], SCENES[3]["lines"][i][0])
    fa = lambda j: float(np.clip((t - cues[j][0]) / 0.5, 0, 1))
    # 問いの箱
    box(fig, 0.06, 0.73, 0.88, 0.1, PRED if i >= 1 else LIGHT)
    fig.text(0.08, 0.78, "Selfish Thompson Sampling の後悔を解析した論文は？", fontsize=19, weight="bold", color=NAVY, va="center")
    if i >= 1:
        fig.text(0.92, 0.78, "→ 見つからなかった", fontsize=19, weight="bold", color=RED, va="center", ha="right", alpha=fa(1))
    cw, ch_ = 0.28, 0.48
    card(fig, 0.06, 0.18, cw, ch_, "2017（CROWNCOM）", "Bonnefoi et al.",
         "IoT 端末が自分の ACK だけで\nチャネルを選ぶ\n\n・UCB1 と Thompson Sampling\n・衝突 = ACK なし = 失敗\n\n中身は Selfish TS\n実験だけ・後悔の解析なし",
         fa(2) if i >= 2 else 0)
    card(fig, 0.36, 0.18, cw, ch_, "2018（ALT）", "Besson & Kaufmann",
         "この考え方を「Selfish」と命名\n\n・どの index 方策とも組める\n・解析と実験は UCB1・KL-UCB\n\nSelfish KL-UCB は小さな確率で\n衝突し続ける（線形の後悔）と予想",
         fa(5) if i >= 5 else 0)
    card(fig, 0.66, 0.18, cw, ch_, "2021（arXiv）", "Trinh & Combes",
         "KL-UCB の index に乱数 Z/t を\n足して対称性を崩す（R-SKL）\n\nThompson Sampling は扱わない\n\nTS 版の理論は未解決",
         fa(8) if i >= 8 else 0, fc=YEL)
    if i >= 6 and i < 8:
        fig.text(0.50, 0.205, "Selfish TS の理論は扱われていない", fontsize=13, color=RED, ha="center", weight="bold")
    if i >= 3:
        fig.add_artist(FancyArrowPatch((0.34, 0.42), (0.36, 0.42), arrowstyle="-|>", mutation_scale=18, color=GRAY,
                                       transform=fig.transFigure, alpha=fa(5) if i >= 5 else 0))
        fig.add_artist(FancyArrowPatch((0.64, 0.42), (0.66, 0.42), arrowstyle="-|>", mutation_scale=18, color=GRAY,
                                       transform=fig.transFigure, alpha=fa(8) if i >= 8 else 0))


# ------------------------------------------------------------------ 場面 4：2 人・2 本の腕
def player(fig, x, y, k, alpha=1):
    fig.add_artist(Ellipse((x, y), 0.07 * H / W, 0.07, transform=fig.transFigure, fc=PL_C[k], ec="white", lw=2, alpha=alpha))
    fig.text(x, y, f"P{k + 1}", fontsize=17, weight="bold", color="white", ha="center", va="center", alpha=alpha)


def arm_box(fig, x, y, k, label):
    box(fig, x - 0.11, y - 0.07, 0.22, 0.14, "#F4F5FA", ec=ARM2_C[k], lw=2.5)
    fig.text(x, y + 0.025, f"腕 {k + 1}", fontsize=20, weight="bold", color=ARM2_C[k], ha="center", va="center")
    fig.text(x, y - 0.03, label, fontsize=16, color=INK, ha="center", va="center")


def arrow(fig, p, q, color, lw=2.5, alpha=1):
    fig.add_artist(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=22, color=color, lw=lw,
                                   transform=fig.transFigure, alpha=alpha))


def draw4(fig, t, cues, data):
    i = which(cues, t)
    frame_base(fig, SCENES[4]["title"], SCENES[4]["lines"][i][0])
    ax_, bx_ = 0.33, 0.67
    if i >= 1:
        arm_box(fig, ax_, 0.33, 0, "平均 0.9")
        arm_box(fig, bx_, 0.33, 1, "平均 0.1")
    player(fig, 0.40, 0.70, 0)
    player(fig, 0.60, 0.70, 1)
    fig.text(0.40, 0.775, "自分の報酬だけ", fontsize=12, color=GRAY, ha="center")
    fig.text(0.60, 0.775, "自分の報酬だけ", fontsize=12, color=GRAY, ha="center")
    if i in (2, 3):
        arrow(fig, (0.395, 0.66), (0.35, 0.41), RED)
        arrow(fig, (0.595, 0.66), (0.37, 0.41), RED)
        fig.text(0.15, 0.50, "衝突！\n2 人とも報酬 0", fontsize=18, weight="bold", color=RED, ha="center", va="center")
    if i == 3:
        for k, x in enumerate((0.80, 0.80)):
            pass
        box(fig, 0.73, 0.52, 0.24, 0.24, YEL)
        fig.text(0.75, 0.73, "それぞれの記録", fontsize=15, weight="bold", color=NAVY, va="top")
        fig.text(0.75, 0.67, "腕 1：失敗 +1", fontsize=15, color=INK, va="top")
        fig.text(0.75, 0.62, "（衝突か、腕の 0 かは", fontsize=13, color=GRAY, va="top")
        fig.text(0.75, 0.585, "区別できない）", fontsize=13, color=GRAY, va="top")
    if i == 4:
        arrow(fig, (0.395, 0.66), (0.34, 0.41), PL_C[0])
        arrow(fig, (0.605, 0.66), (0.66, 0.41), PL_C[1])
        fig.text(0.5, 0.20, "理想：別々の腕に分かれる（衝突なし）", fontsize=19, weight="bold", color=GREEN, ha="center")


# ------------------------------------------------------------------ 場面 5・6：2 人の軌跡
def klucb_index(N, S, t):
    from toy import klucb
    f = math.log(max(t, 1))
    return np.array([klucb(S[k] / N[k] if N[k] else 0.0, N[k], f) for k in range(2)])


def timeline(fig, ch, co, upto, T, y0=0.53):
    ax = fig.add_axes([0.10, y0, 0.84, 0.27])
    img = np.ones((3, T, 3))
    cols = [matplotlib.colors.to_rgb(c) for c in ARM2_C]
    for s in range(upto):
        img[0, s] = cols[ch[s, 0]]
        img[1, s] = cols[ch[s, 1]]
        img[2, s] = matplotlib.colors.to_rgb(RED) if co[s] else (0.93, 0.93, 0.93)
    ax.imshow(img, aspect="auto", interpolation="nearest", extent=(0.5, T + 0.5, 2.5, -0.5))
    ax.set_yticks([0, 1, 2], ["P1 の選択", "P2 の選択", "衝突"], fontsize=14)
    ax.set_xlabel("ステップ", fontsize=13)
    ax.tick_params(axis="x", labelsize=11)
    if upto < T:
        ax.axvline(upto + 0.5, color=INK, lw=1)
    for s in ax.spines.values():
        s.set_visible(False)
    # 凡例
    fig.text(0.10, 0.82, "■", color=ARM2_C[0], fontsize=16, va="center")
    fig.text(0.125, 0.82, "腕 1（0.9）", fontsize=13, va="center")
    fig.text(0.22, 0.82, "■", color=ARM2_C[1], fontsize=16, va="center")
    fig.text(0.245, 0.82, "腕 2（0.1）", fontsize=13, va="center")
    fig.text(0.34, 0.82, "■", color=RED, fontsize=16, va="center")
    fig.text(0.365, 0.82, "衝突", fontsize=13, va="center")
    n = int(co[:upto].sum())
    fig.text(0.94, 0.82, f"ステップ {upto}　衝突 {n} 回", fontsize=16, weight="bold", color=NAVY, ha="right", va="center")
    return ax


def draw5(fig, t, cues, data):
    ch, co, post = data["kl"]
    T = data["kl_T"]
    i = which(cues, t)
    frame_base(fig, SCENES[5]["title"], SCENES[5]["lines"][i][0])
    if i == 0:
        upto = 0
    elif i == 1:
        upto = 2
    else:
        upto = max(2, int(2 + (T - 2) * prog(cues, 2, t, 3) ** 1.6))
    timeline(fig, ch, co, upto, T)
    # 下：各プレイヤーの index（KL-UCB）と記録
    for m in range(2):
        x0 = 0.10 + 0.43 * m
        box(fig, x0, 0.16, 0.41, 0.31, "#F4F5FA")
        fig.text(x0 + 0.015, 0.445, f"P{m + 1} の index", fontsize=15, weight="bold", color=PL_C[m], va="top")
        if upto == 0:
            continue
        N, S = post[upto - 1]
        idx = klucb_index(N[m], S[m], upto + 1)
        ax = fig.add_axes([x0 + 0.03, 0.19, 0.17, 0.2])
        ax.bar([0, 1], idx, color=ARM2_C, width=0.6)
        ax.set_ylim(0, 1.05), ax.set_xticks([0, 1], ["腕 1", "腕 2"], fontsize=12)
        ax.tick_params(axis="y", labelsize=10)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        fig.text(x0 + 0.23, 0.38, f"腕 1：{int(S[m, 0])} / {int(N[m, 0])}", fontsize=14, color=ARM2_C[0], weight="bold")
        fig.text(x0 + 0.23, 0.33, f"腕 2：{int(S[m, 1])} / {int(N[m, 1])}", fontsize=14, color=ARM2_C[1], weight="bold")
        fig.text(x0 + 0.23, 0.28, "（成功 / 回数）", fontsize=11, color=GRAY)
    if i == 1:
        box(fig, 0.30, 0.60, 0.40, 0.08, PRED, z=2)
        fig.text(0.50, 0.64, "2 人の記録が同じ → index も同じ", fontsize=17, weight="bold", color=RED, ha="center", va="center")


def draw6(fig, t, cues, data):
    ch, co, post = data["ts"]
    T = data["ts_T"]
    i = which(cues, t)
    frame_base(fig, SCENES[6]["title"], SCENES[6]["lines"][i][0])
    upto = int(T * prog(cues, 0, t, 2) ** 1.3)
    timeline(fig, ch, co, upto, T)
    for m in range(2):
        x0 = 0.10 + 0.43 * m
        box(fig, x0, 0.16, 0.41, 0.31, "#F4F5FA")
        fig.text(x0 + 0.015, 0.445, f"P{m + 1} の Beta 分布", fontsize=15, weight="bold", color=PL_C[m], va="top")
        N, S = post[upto - 1] if upto > 0 else (np.zeros((2, 2)), np.zeros((2, 2)))
        ax = fig.add_axes([x0 + 0.03, 0.19, 0.22, 0.2])
        for k in range(2):
            y = beta_pdf(XG, 1 + S[m, k], 1 + N[m, k] - S[m, k])
            ax.plot(XG, y, color=ARM2_C[k], lw=2)
            ax.fill_between(XG, y, color=ARM2_C[k], alpha=0.12)
        ax.set_xlim(0, 1), ax.set_yticks([])
        ax.tick_params(axis="x", labelsize=10)
        for s in ("top", "right", "left"):
            ax.spines[s].set_visible(False)
        fig.text(x0 + 0.27, 0.38, f"腕 1：{int(S[m, 0])} / {int(N[m, 0])}", fontsize=14, color=ARM2_C[0], weight="bold")
        fig.text(x0 + 0.27, 0.33, f"腕 2：{int(S[m, 1])} / {int(N[m, 1])}", fontsize=14, color=ARM2_C[1], weight="bold")
        fig.text(x0 + 0.27, 0.28, "（成功 / 回数）", fontsize=11, color=GRAY)


# ------------------------------------------------------------------ 場面 7：500 試行
def draw7(fig, t, cues, data):
    d = data["fig1"]
    i = which(cues, t)
    frame_base(fig, SCENES[7]["title"], SCENES[7]["lines"][i][0])
    fig.text(0.06, 0.82, "M = K = 2，μ = (0.9, 0.1)，T = 10⁴，500 試行（mpmab-simu）", fontsize=15, color=GRAY, va="center")
    algs = [("selfish_klucb", "Selfish KL-UCB", ORANGE), ("trinh2021_rskl", "R-SKL", RED), ("selfish_ts", "Selfish TS", GREEN)]
    bins = np.linspace(0, 10000, 41)
    for j, (a, name, c) in enumerate(algs):
        ax = fig.add_axes([0.07 + 0.31 * j, 0.25, 0.27, 0.47])
        v = d[d.algorithm == a].cumulative_regret.values
        ax.hist(v, bins=bins, color=c, alpha=0.85)
        ax.set_yscale("log"), ax.set_ylim(0.7, 600), ax.set_xlim(0, 10000)
        ax.set_title(name, fontsize=17, weight="bold", color=c)
        ax.set_xlabel("1 万ステップ後の後悔", fontsize=12)
        if j == 0:
            ax.set_ylabel("試行の数（対数）", fontsize=12)
        ax.tick_params(labelsize=10)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        if i >= 1:
            ax.axvline(1000, color=INK, ls="--", lw=1.2)
            ax.axvspan(1000, 10000, color=PRED, alpha=0.35, zorder=0)
            ax.text(5500, 250, f"1000 超え：{int((v > 1000).sum())} 回", fontsize=16, weight="bold", color=INK, ha="center")
        if i >= 2:
            ax.text(5500, 90, f"平均 {v.mean():,.0f}", fontsize=15, color=INK, ha="center")
            ax.text(5500, 35, f"中央値 {np.median(v):,.0f}", fontsize=13, color=GRAY, ha="center")


# ------------------------------------------------------------------ 場面 8：まとめ
def draw8(fig, t, cues, data):
    i = which(cues, t)
    frame_base(fig, SCENES[8]["title"], SCENES[8]["lines"][i][0])
    items = [("Thompson Sampling", "Beta 事後分布から乱数を引き、最大の腕を選ぶ。1 人なら漸近最適（2012）"),
             ("Selfish TS の論文", "IoT の実験（Bonnefoi et al. 2017）はあるが、後悔の理論はない"),
             ("並列にすると", "毎回の乱数が対称性を崩し、衝突の連続を避けやすい（500 試行で 1000 超えは 1 回）"),
             ("計算中", "全平均が等しい設定・腕の数を増やした比較（Huang・Izumi・R-SKL と比べる）")]
    for j, (h, b) in enumerate(items):
        al = float(np.clip((t - cues[j][0]) / 0.5, 0, 1)) if j < len(cues) else 0
        y = 0.76 - 0.15 * j
        box(fig, 0.05, y - 0.055, 0.90, 0.11, YEL if j == 2 else (LIGHT if j < 3 else "#F4F5FA"))
        fig.text(0.07, y, h, fontsize=17, weight="bold", color=NAVY, va="center", alpha=al)
        fig.text(0.31, y, b, fontsize=15, color=INK, va="center", alpha=al)


DRAW = [draw0, draw1, draw2, draw3, draw4, draw5, draw6, draw7, draw8]


def build_data():
    hist = single_ts()
    # 場面 2 の静止画：腕 3 がまだ広く、腕 1 が細い時刻
    snap = 300
    kl = toy_run("klucb", 2, T=400)
    ts = toy_run("ts", 2, T=700)
    return dict(hist=hist, snap=snap, kl=kl, kl_T=400, ts=ts, ts_T=700, fig1=pd.read_csv(FIG1))



if __name__ == "__main__":
    Video(SCENES, DRAW, build_data, out=os.path.join(HERE, "ts_explainer.mp4")).main(sys.argv[1:])
