"""作例：UCB と KL-UCB の説明動画（約 5 分 8 秒）。

    PY=~/.claude/skills/explainer-video/.venv/bin/python
    $PY ucb_sim.py                     # 比較のシミュレーション（build/ucb_sim.pkl、1〜2 分）
    $PY ucb_explainer.py preview       # 配置の確認
    $PY ucb_explainer.py               # ucb_klucb_explainer.mp4 を作る

出典（原典で確認済み）
- UCB1：Auer, Cesa-Bianchi & Fischer (2002), Machine Learning 47, 定理 1（index は平均 + sqrt(2 ln n / n_j)）
- KL-UCB：Garivier & Cappé (COLT 2011)。定理は f(t) = log t + 3 log log t、実用では c = 0 を推奨。系 3：Bernoulli で漸近最適
- 下界：Lai & Robbins (1985)
"""
import math
import os
import pickle
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "scripts"))
sys.path.insert(0, HERE)
from video import *  # noqa: F401,F403
from video import Video, frame_base, which, prog, box, panel, side_panel, clean, fade  # noqa: F401
from ucb_sim import kl_vec

ARM_C = ["#0D114A", "#D14B46", "#196723"]
ARM2_C = ["#0D114A", "#E69F00"]
PL_C = ["#3B5BA9", "#196723"]


def panel(fig, rows, x=0.67, y0=0.17, y1=0.66):
    """右の説明欄（上の数式の箱の下に収める）。"""
    import video
    video.panel(fig, rows, x=x, y0=y0, y1=y1)

SCENES = [
    dict(title=None, lines=[
        ("バンディット問題の基本の方策である UCB と、その改良の KL-UCB を説明します。"
         "最後に、マルチプレイヤーの Selfish KL-UCB と R-SKL とのつながりを見ます。",
         "バンディット問題の基本の方策である、ユーシービーと、その改良の、ケーエル・ユーシービーを説明します。"
         "最後に、マルチプレイヤーの、セルフィッシュ・ケーエル・ユーシービーと、アール・エス・ケー・エルとの、つながりを見ます。"),
    ]),
    dict(title="1. バンディット問題と、探索と活用", lines=[
        ("バンディット問題では、平均の分からない複数の腕から、毎回 1 本を選んで報酬を得ます。",
         "バンディット問題では、平均の分からない複数の腕から、毎回1本を選んで、報酬を得ます。"),
        ("目標は、最良の腕をずっと引いた場合との差、つまり後悔を小さくすることです。",
         "目標は、最良の腕をずっと引いた場合との差、つまり、後悔を小さくすることです。"),
        ("これまでの平均が最も高い腕だけを引くと、運悪く低く見えた良い腕を、二度と試せません。",
         "これまでの平均が最も高い腕だけを引くと、運悪く低く見えた良い腕を、二度と試せません。"),
        ("そこで、まだよく分からない腕を試す探索と、良さそうな腕を引く活用の、釣り合いが必要です。",
         "そこで、まだよく分からない腕を試す、探索と、良さそうな腕を引く、活用の、釣り合いが必要です。"),
    ]),
    dict(title="2. UCB：分からないものは楽観的に見積もる", lines=[
        ("UCB の考え方は、不確かなものは楽観的に見積もる、というものです。",
         "ユーシービーの考え方は、不確かなものは、楽観的に見積もる、というものです。"),
        ("各腕について、これまでの平均に不確かさの分を上乗せした、上側信頼限界を計算します。",
         "各腕について、これまでの平均に、不確かさの分を上乗せした、上側信頼限界を計算します。"),
        ("UCB1 では、上乗せは √(2 log t ／ 引いた回数) です。",
         "ユーシービー・ワンでは、上乗せは、ルート、2ログ t、割る、引いた回数、です。"),
        ("毎回、この上限が最も高い腕を引きます。",
         "毎回、この上限が、最も高い腕を引きます。"),
        ("引いた回数が増えると上乗せは小さくなり、上限は本当の平均に近づきます。",
         "引いた回数が増えると、上乗せは小さくなり、上限は、本当の平均に近づきます。"),
    ]),
    dict(title="なぜうまくいくのか", lines=[
        ("悪い腕も、引かれない間は log t が少しずつ増えるので、上限がゆっくり上がり、ときどき試されます。",
         "悪い腕も、引かれない間は、ログ t が少しずつ増えるので、上限がゆっくり上がり、ときどき試されます。"),
        ("試されて低い報酬が出ると、上限はまた下がります。",
         "試されて、低い報酬が出ると、上限は、また下がります。"),
        ("良い腕は平均そのものが高いので、上乗せが小さくなっても選ばれ続けます。",
         "良い腕は、平均そのものが高いので、上乗せが小さくなっても、選ばれ続けます。"),
        ("Auer らは 2002 年に、悪い腕を引く回数が 8 log T ／ Δ² 程度で抑えられ、後悔が log T のオーダーになることを示しました。",
         "アウアーらは、2002年に、悪い腕を引く回数が、8ログ T、割る、デルタの2乗、程度で抑えられ、後悔が、ログ T のオーダーになることを示しました。"),
    ]),
    dict(title="3. どこまで良くできるか：Lai–Robbins の下界", lines=[
        ("1985 年に Lai と Robbins は、どんな良い方策でも、悪い腕をおよそ log T ／ KL ダイバージェンス回は引く必要があることを示しました。",
         "1985年に、ライとロビンズは、どんな良い方策でも、悪い腕を、およそ、ログ T、割る、ケーエル・ダイバージェンス回は、引く必要があることを示しました。"),
        ("KL ダイバージェンスは、2 つの分布の見分けやすさです。差が同じでも、平均が 0 や 1 に近いほど見分けやすくなります。",
         "ケーエル・ダイバージェンスは、2つの分布の、見分けやすさです。差が同じでも、平均が、0や1に近いほど、見分けやすくなります。"),
        ("UCB1 の上乗せは、平均の位置を考えず、引いた回数だけで決まります。",
         "ユーシービー・ワンの上乗せは、平均の位置を考えず、引いた回数だけで決まります。"),
        ("そのため、平均が 0 や 1 に近いとき、必要以上に探索してしまいます。",
         "そのため、平均が、0や1に近いとき、必要以上に、探索してしまいます。"),
    ]),
    dict(title="4. KL-UCB：KL ダイバージェンスで上限を決める", lines=[
        ("KL-UCB は、上乗せを足す代わりに、KL ダイバージェンスで上限を決めます。",
         "ケーエル・ユーシービーは、上乗せを足す代わりに、ケーエル・ダイバージェンスで、上限を決めます。"),
        ("引いた回数 × 平均から q までの KL が log t 以下になる、最大の q を上限にします。",
         "引いた回数、かける、平均から q までのケーエルが、ログ t 以下になる、最大の q を、上限にします。"),
        ("実線の曲線が KL、横線が log t で、その交点が KL-UCB の上限です。破線は KL を 2(q − 平均)² で置き換えた、UCB 型の場合です。",
         "実線の曲線がケーエル、横線がログ t で、その交点が、ケーエル・ユーシービーの上限です。破線は、ケーエルを、2かける、差の2乗で置き換えた、ユーシービー型の場合です。"),
        ("引いた回数が増えると曲線が急になり、上限は平均に近づきます。",
         "引いた回数が増えると、曲線が急になり、上限は、平均に近づきます。"),
        ("KL-UCB の上限は必ず 1 以下で、UCB 型より常に低く、平均が 0 や 1 に近いほど差が大きくなります。",
         "ケーエル・ユーシービーの上限は、必ず1以下で、ユーシービー型より、常に低く、平均が、0や1に近いほど、差が大きくなります。"),
        ("Garivier と Cappé は 2011 年に、KL-UCB が Bernoulli 報酬で漸近最適であることを示しました。",
         "ガリビエと、カッペは、2011年に、ケーエル・ユーシービーが、ベルヌーイ報酬で、漸近最適であることを示しました。"),
    ]),
    dict(title="5. 比べると", lines=[
        ("3 本の腕で、1 万ステップを 100 回試しました。左は平均が 0 に近い場合、右は平均が中ほどの場合です。",
         "3本の腕で、1万ステップを、100回試しました。左は、平均が0に近い場合、右は、平均が中ほどの場合です。"),
        ("平均が 0 に近いと、UCB1 の後悔は約 180、KL-UCB は約 28 で、6 分の 1 ほどになります。",
         "平均が0に近いと、ユーシービー・ワンの後悔は、約180、ケーエル・ユーシービーは、約28で、6分の1ほどになります。"),
        ("平均が中ほどでは、約 150 と約 49 で、差は 3 分の 1 ほどに縮みます。",
         "平均が中ほどでは、約150と、約49で、差は、3分の1ほどに縮みます。"),
        ("Thompson Sampling も、どちらの場合も KL-UCB と同じくらい小さくなります。",
         "トンプソン・サンプリングも、どちらの場合も、ケーエル・ユーシービーと同じくらい、小さくなります。"),
        ("なお、定理では log t に 3 log log t を足しますが、Garivier と Cappé は実用では足さないこと、c = 0 を勧めています。",
         "なお、定理では、ログ t に、3ログ・ログ t を足しますが、ガリビエとカッペは、実用では足さないこと、つまり、c イコール 0 を勧めています。"),
    ]),
    dict(title="6. マルチプレイヤーとのつながり", lines=[
        ("Selfish KL-UCB は、各プレイヤーが自分の観測だけで、この KL-UCB の index を使う方策です。",
         "セルフィッシュ・ケーエル・ユーシービーは、各プレイヤーが、自分の観測だけで、このケーエル・ユーシービーのインデックスを使う方策です。"),
        ("index が決定的なので、2 人の記録がそろうと、同じ腕を選び続けることがあります。",
         "インデックスが決定的なので、2人の記録がそろうと、同じ腕を選び続けることがあります。"),
        ("R-SKL は、この index に、標準正規分布の乱数 Z を t で割ったゆらぎを足して、対称性を崩します。",
         "アール・エス・ケー・エルは、このインデックスに、標準正規分布の乱数 Z を、t で割ったゆらぎを足して、対称性を崩します。"),
        ("ゆらぎは t で割られているのですぐ小さくなり、1 人で使う KL-UCB の良さはほぼそのまま残ります。",
         "ゆらぎは、t で割られているので、すぐ小さくなり、1人で使うケーエル・ユーシービーの良さは、ほぼ、そのまま残ります。"),
    ]),
    dict(title="まとめ", lines=[
        ("UCB は、平均に不確かさの分を上乗せした上限で腕を選ぶ方策で、後悔は log T のオーダーです。",
         "ユーシービーは、平均に、不確かさの分を上乗せした上限で、腕を選ぶ方策で、後悔は、ログ T のオーダーです。"),
        ("ただし上乗せが平均の位置を考えないため、定数は最適ではありません。",
         "ただし、上乗せが、平均の位置を考えないため、定数は、最適ではありません。"),
        ("KL-UCB は KL ダイバージェンスで上限を決め、Bernoulli 報酬で Lai–Robbins の下界に一致します。",
         "ケーエル・ユーシービーは、ケーエル・ダイバージェンスで上限を決め、ベルヌーイ報酬で、ライ・ロビンズの下界に一致します。"),
        ("この KL-UCB を各プレイヤーが使うのが Selfish KL-UCB、そこに Z/t のゆらぎを足したのが R-SKL です。",
         "このケーエル・ユーシービーを、各プレイヤーが使うのが、セルフィッシュ・ケーエル・ユーシービー、そこに、Z 割る t のゆらぎを足したのが、アール・エス・ケー・エルです。"),
    ]),
]


def kl1(p, q):
    return float(kl_vec(np.array([p]), np.array([q]))[0])


def klucb1(mean, n, f):
    lo, hi = mean, 1.0
    for _ in range(40):
        mid = (lo + hi) / 2
        if n * kl1(mean, mid) <= f:
            lo = mid
        else:
            hi = mid
    return lo


# ------------------------------------------------------------------ 場面 0：表紙
def draw0(fig, t, cues, data):
    frame_base(fig, None, SCENES[0]["lines"][which(cues, t)][0])
    fig.text(0.5, 0.70, "UCB と KL-UCB", fontsize=44, weight="bold", color=NAVY, ha="center")
    qs = ["UCB：分からないものは楽観的に見積もる", "KL-UCB：KL ダイバージェンスで上限を決める", "Selfish KL-UCB・R-SKL とのつながり"]
    for i, q in enumerate(qs):
        a = float(np.clip((t - 0.6 - 1.5 * i) / 0.5, 0, 1))
        y = 0.52 - 0.09 * i
        box(fig, 0.22, y - 0.034, 0.56, 0.068, LIGHT)
        fig.text(0.24, y, f"{i + 1}", fontsize=22, weight="bold", color=NAVY, va="center", alpha=a)
        fig.text(0.28, y, q, fontsize=20, color=INK, va="center", alpha=a)


# ------------------------------------------------------------------ 場面 1：問題
def slot(fig, x, y, k, top, bottom, hi=False):
    box(fig, x - 0.09, y - 0.11, 0.18, 0.22, YEL if hi else "#F4F5FA", ec=ARM_C[k], lw=2.5)
    fig.text(x, y + 0.06, f"腕 {k + 1}", fontsize=20, weight="bold", color=ARM_C[k], ha="center", va="center")
    fig.text(x, y, top, fontsize=16, color=INK, ha="center", va="center")
    fig.text(x, y - 0.055, bottom, fontsize=14, color=GRAY, ha="center", va="center")


def draw1(fig, t, cues, data):
    i = which(cues, t)
    frame_base(fig, SCENES[1]["title"], SCENES[1]["lines"][i][0])
    xs = [0.25, 0.5, 0.75]
    if i <= 1:
        for k in range(3):
            slot(fig, xs[k], 0.62, k, "平均 = ?", "")
        if i == 1:
            box(fig, 0.12, 0.22, 0.76, 0.2, YEL)
            fig.text(0.5, 0.36, r"後悔 $R_T = T\mu^* - \mathbb{E}[\,$得た報酬の合計$\,]$", fontsize=24, color=NAVY,
                     ha="center", va="center")
            fig.text(0.5, 0.27, "μ* は最良の腕の平均。最良の腕をずっと引けば 0", fontsize=16, color=INK, ha="center", va="center")
    else:
        true = ["本当は 0.7", "本当は 0.5", "本当は 0.3"]
        first = ["1 回目：報酬 0", "1 回目：報酬 1", "1 回目：報酬 0"]
        for k in range(3):
            slot(fig, xs[k], 0.62, k, first[k], true[k], hi=(k == 1 and i == 2))
        if i == 2:
            fig.text(0.5, 0.40, "平均だけで選ぶと、腕 2 を引き続ける（腕 1 は「0」のまま二度と試されない）", fontsize=17,
                     weight="bold", color=RED, ha="center", va="center")
        else:
            box(fig, 0.10, 0.22, 0.38, 0.2, LIGHT)
            box(fig, 0.52, 0.22, 0.38, 0.2, LIGHT)
            fig.text(0.29, 0.37, "探索", fontsize=22, weight="bold", color=NAVY, ha="center", va="center")
            fig.text(0.29, 0.29, "まだよく分からない腕を試す", fontsize=16, color=INK, ha="center", va="center")
            fig.text(0.71, 0.37, "活用", fontsize=22, weight="bold", color=NAVY, ha="center", va="center")
            fig.text(0.71, 0.29, "良さそうな腕を引く", fontsize=16, color=INK, ha="center", va="center")
            fig.text(0.5, 0.32, "⇄", fontsize=30, color=GRAY, ha="center", va="center")


# ------------------------------------------------------------------ 場面 2・3：1 人の UCB1
MU = np.array([0.7, 0.5, 0.3])


def ucb_run(seed=3, T=1000):
    rng = np.random.default_rng(seed)
    N, S = np.zeros(3), np.zeros(3)
    hist = []
    for t in range(1, T + 1):
        if t <= 3:
            idx = np.full(3, np.nan)
            idx[N == 0] = np.inf
            k = t - 1
        else:
            idx = S / N + np.sqrt(2 * np.log(t - 1) / N)
            k = int(np.argmax(idx))
        r = int(rng.random() < MU[k])
        hist.append(dict(t=t, N=N.copy(), S=S.copy(), idx=idx.copy(), k=k, r=r))
        N[k] += 1
        S[k] += r
    hist.append(dict(t=T + 1, N=N.copy(), S=S.copy(), idx=S / N + np.sqrt(2 * np.log(T) / N), k=None, r=None))
    return hist


def draw_bars(ax, h, chosen=None, show_bonus=True, ymax=None):
    N, S = h["N"], h["S"]
    mean = np.where(N > 0, S / np.maximum(N, 1), np.nan)
    tt = max(h["t"] - 1, 1)
    ucb = np.where(N > 0, mean + np.sqrt(2 * np.log(max(tt, 2)) / np.maximum(N, 1)), np.nan)
    top = np.nanmax(ucb) if np.any(N > 0) else 1
    ymax = ymax or max(1.1, top * 1.08)
    for k in range(3):
        x = k
        ax.plot([x - 0.3, x + 0.3], [MU[k]] * 2, color=ARM_C[k], ls=":", lw=2)
        if N[k] == 0:
            continue
        if show_bonus:
            ax.add_patch(plt.Rectangle((x - 0.12, mean[k]), 0.24, ucb[k] - mean[k], fc=ARM_C[k], alpha=0.18,
                                       ec=ARM_C[k], lw=1.5))
            ax.plot([x - 0.18, x + 0.18], [ucb[k]] * 2, color=ARM_C[k], lw=4 if chosen == k else 2.5)
            if chosen == k:
                ax.plot([x], [ucb[k]], marker="v", ms=16, color=YEL, mec=ARM_C[k], mew=2, zorder=6)
        ax.plot([x], [mean[k]], "o", ms=12, color=ARM_C[k], mec="white", mew=1.5, zorder=5)
    ax.axhline(1.0, color=GRAY, lw=0.8, ls="--")
    ax.set_xlim(-0.6, 2.6), ax.set_ylim(0, ymax)
    ax.set_xticks([0, 1, 2], [f"腕 {k + 1}" for k in range(3)], fontsize=15)
    for k, tl in enumerate(ax.get_xticklabels()):
        tl.set_color(ARM_C[k]), tl.set_weight("bold")
    ax.set_ylabel("報酬の平均の見積もり", fontsize=14)
    clean(ax)
    return mean, ucb


def draw2(fig, t, cues, data):
    hist = data["hist"]
    i = which(cues, t)
    frame_base(fig, SCENES[2]["title"], SCENES[2]["lines"][i][0])
    ax = fig.add_axes([0.08, 0.20, 0.56, 0.62])
    NS = 8      # 文 3（毎回、上限が最も高い腕）で 1 ステップずつ
    if i <= 2:
        step = 3
        chosen = None
    elif i == 3:
        p = prog(cues, 3, t)
        step = 3 + min(int(p * NS), NS - 1)
        chosen = hist[step]["k"]
    else:
        p = prog(cues, 4, t)
        step = int(round((3 + NS) * (1000 / (3 + NS)) ** min(p / 0.85, 1)))
        chosen = None
    h = hist[step]
    mean, ucb = draw_bars(ax, h, chosen=chosen, show_bonus=(i >= 1))
    if i >= 1:
        k = 2
        ax.annotate("上乗せ\n（不確かさ）", xy=(2.14, (mean[k] + ucb[k]) / 2), xytext=(2.3, (mean[k] + ucb[k]) / 2),
                    fontsize=13, color=GRAY, va="center")
    rows = [(f"時刻 t = {h['t']}", dict(fontsize=20, weight="bold", color=NAVY, dy=0.07))]
    if i >= 2:
        rows.append((r"$\hat\mu_k + \sqrt{2\ln t \,/\, N_k}$", dict(fontsize=22, color=INK, dy=0.09)))
    for k in range(3):
        n = int(h["N"][k])
        rows.append((f"腕 {k + 1}：引いた回数 {n}", dict(fontsize=15, color=ARM_C[k], weight="bold", dy=0.045)))
        if n:
            rows.append((f"   平均 {mean[k]:.2f}　上限 {ucb[k]:.2f}", dict(fontsize=13, color=INK, dy=0.055)))
    if chosen is not None:
        rows.append((f"→ 上限が最も高い腕 {chosen + 1} を引く", dict(fontsize=15, weight="bold", color=ARM_C[chosen], dy=0.05)))
    side_panel(fig, None, rows, x=0.67, y0=0.17)
    fig.text(0.08, 0.84, "●：これまでの平均　━：上限（UCB）　┈：本当の平均（見えない）", fontsize=12, color=GRAY)


def draw3(fig, t, cues, data):
    hist = data["hist"]
    i = which(cues, t)
    frame_base(fig, SCENES[3]["title"], SCENES[3]["lines"][i][0])
    T = 600
    ax = fig.add_axes([0.08, 0.37 if i == 3 else 0.22, 0.88, 0.45 if i == 3 else 0.58])
    upto = int(4 + (T - 4) * prog(cues, 0, t, 1)) if i <= 1 else T
    ts = np.arange(4, upto + 1)
    idx = np.array([hist[s - 1]["idx"] for s in ts])
    ks = np.array([hist[s - 1]["k"] for s in ts])
    for k in range(3):
        lw = 2.6 if (i <= 1 and k == 2) or (i == 2 and k == 0) or i == 3 else 1.6
        al = 1.0 if (i <= 1 and k == 2) or (i == 2 and k == 0) or i == 3 else 0.35
        ax.plot(ts, idx[:, k], color=ARM_C[k], lw=lw, alpha=al, label=f"腕 {k + 1} の上限")
        ax.axhline(MU[k], color=ARM_C[k], ls=":", lw=1.2, alpha=al)
        sel = ks == k
        if k == 2:
            ax.plot(ts[sel], idx[sel, k], "o", ms=6, color=ARM_C[k], alpha=al)
    ax.set_xlim(0, T), ax.set_ylim(0.2, 1.6)
    ax.set_xlabel("時刻 t", fontsize=14), ax.set_ylabel("上限（UCB）", fontsize=14)
    ax.legend(fontsize=12, loc="upper right", frameon=False)
    clean(ax)
    if i <= 1:
        ax.text(T * 0.35, 1.45, "● 腕 3 が引かれた時刻（上限が下がる）", fontsize=14, color=ARM_C[2], weight="bold")
    if i == 3:
        box(fig, 0.08, 0.16, 0.88, 0.14, YEL)
        fig.text(0.10, 0.255, "Auer, Cesa-Bianchi & Fischer (2002)", fontsize=15, weight="bold", color=NAVY, va="center")
        fig.text(0.10, 0.195, r"悪い腕 $k$ を引く回数の期待値 $\leq \dfrac{8\ln T}{\Delta_k^2} + 1 + \dfrac{\pi^2}{3}$" +
                 r"　→　後悔は $O(\log T)$", fontsize=16, color=INK, va="center")


# ------------------------------------------------------------------ 場面 4：下界
def draw4(fig, t, cues, data):
    i = which(cues, t)
    frame_base(fig, SCENES[4]["title"], SCENES[4]["lines"][i][0])
    box(fig, 0.06, 0.70, 0.88, 0.12, YEL)
    fig.text(0.5, 0.76, r"悪い腕 $k$ を引く回数 $\gtrsim \dfrac{\ln T}{\mathrm{KL}(\mu_k,\ \mu^*)}$　（Lai & Robbins, 1985）",
             fontsize=21, color=NAVY, ha="center", va="center")
    if i == 0:
        return
    ax = fig.add_axes([0.10, 0.22, 0.52, 0.42])
    d = 0.1
    mu = np.linspace(0.005, 0.895, 300)
    need = 1 / kl_vec(mu, mu + d)
    ax.plot(mu, need, color=NAVY, lw=3, label="下界：1 / KL(μ, μ + 0.1)")
    if i >= 2:
        ax.axhline(1 / (2 * d * d), color=RED, lw=2.5, ls="--", label="UCB 型（Hoeffding）：1 / (2 × 0.1²) = 50")
    ax.set_xlim(0, 0.9), ax.set_ylim(0, 60)
    ax.set_xlabel("悪い腕の平均 μ（最良の腕は μ + 0.1）", fontsize=13)
    ax.set_ylabel("log T あたりの必要な試行回数", fontsize=13)
    ax.legend(fontsize=12, loc="lower center", frameon=False)
    clean(ax)
    rows = [("差 Δ = 0.1 のとき", dict(fontsize=17, weight="bold", color=NAVY, dy=0.07))]
    for m in (0.01, 0.45, 0.85):
        rows.append((f"μ = {m:.2f}：{1 / kl1(m, m + d):.0f} 回", dict(fontsize=16, color=INK, dy=0.055)))
    if i >= 2:
        rows.append(("", dict(fontsize=8, dy=0.02)))
        rows.append(("UCB 型は位置によらず 50", dict(fontsize=15, color=RED, weight="bold", dy=0.055)))
    if i >= 3:
        rows.append(("→ 0 や 1 の近くで", dict(fontsize=15, color=RED, weight="bold", dy=0.045)))
        rows.append(("   探索しすぎる", dict(fontsize=15, color=RED, weight="bold", dy=0.055)))
    panel(fig, rows)
    fig.text(0.10, 0.655, "大きいほど見分けにくい", fontsize=12, color=GRAY)


# ------------------------------------------------------------------ 場面 5：KL-UCB の作図
def draw5(fig, t, cues, data):
    i = which(cues, t)
    frame_base(fig, SCENES[5]["title"], SCENES[5]["lines"][i][0])
    box(fig, 0.06, 0.71, 0.88, 0.11, YEL)
    fig.text(0.5, 0.765, r"$U_k(t) = \max\{\, q \in [0,1] : N_k \cdot \mathrm{KL}(\hat\mu_k,\ q) \leq \ln t \,\}$",
             fontsize=23, color=NAVY, ha="center", va="center")
    if i == 0:
        return
    mean, lt = 0.1, math.log(1000)
    if i <= 2:
        n = 10
    elif i == 3:
        n = int(round(10 * 30 ** prog(cues, 3, t)))
    else:
        n = 30
    q = np.linspace(mean, 0.999, 500)
    ax = fig.add_axes([0.08, 0.22, 0.56, 0.42])
    if i >= 2:
        ax.plot(q, n * kl_vec(np.full_like(q, mean), q), color=NAVY, lw=3, label=r"$N_k\cdot\mathrm{KL}(\hat\mu_k, q)$")
        ax.plot(q, n * 2 * (q - mean) ** 2, color=RED, lw=2.2, ls="--", label=r"$N_k\cdot 2(q-\hat\mu_k)^2$（UCB 型）")
        ax.axhline(lt, color=GREEN, lw=2, label=r"$\ln t$（t = 1000）")
        u_kl = klucb1(mean, n, lt)
        u_h = mean + math.sqrt(lt / (2 * n))
        ax.plot([u_kl], [lt], "o", ms=13, color=NAVY, mec=YEL, mew=3, zorder=6)
        ax.axvline(u_kl, color=NAVY, lw=1, ls=":")
        if u_h <= 1:
            ax.plot([u_h], [lt], "o", ms=11, color=RED, mec="white", mew=2, zorder=6)
            ax.axvline(u_h, color=RED, lw=1, ls=":")
    ax.axvline(mean, color=GRAY, lw=1)
    ax.text(mean + 0.01, 5.0, r"$\hat\mu_k = 0.1$", fontsize=13, color=GRAY)
    ax.set_xlim(0, 1), ax.set_ylim(0, 15)
    ax.set_xlabel("候補の平均 q", fontsize=14)
    ax.legend(fontsize=12, loc="upper left", frameon=False)
    clean(ax)
    rows = [(f"平均 0.1、引いた回数 N = {n}", dict(fontsize=16, weight="bold", color=NAVY, dy=0.07))]
    if i >= 2:
        u_kl = klucb1(mean, n, lt)
        u_h = mean + math.sqrt(lt / (2 * n))
        u_1 = mean + math.sqrt(2 * lt / n)
        rows += [("上限", dict(fontsize=15, weight="bold", color=INK, dy=0.05)),
                 (f"KL-UCB：{u_kl:.2f}", dict(fontsize=17, weight="bold", color=NAVY, dy=0.05)),
                 (f"UCB 型（破線）：{u_h:.2f}", dict(fontsize=15, color=RED, dy=0.05)),
                 (f"UCB1：{u_1:.2f}", dict(fontsize=15, color=GRAY, dy=0.07))]
    if i >= 4:
        rows += [("KL-UCB は 1 を超えない", dict(fontsize=14, weight="bold", color=GREEN, dy=0.045)),
                 ("UCB 型より常に低い", dict(fontsize=14, weight="bold", color=GREEN, dy=0.065))]
    if i >= 5:
        rows += [("Garivier & Cappé (2011)", dict(fontsize=14, weight="bold", color=NAVY, dy=0.045)),
                 ("Bernoulli 報酬で漸近最適", dict(fontsize=14, weight="bold", color=NAVY, dy=0.05))]
    panel(fig, rows)


# ------------------------------------------------------------------ 場面 6：比較
LAB = {"ucb1": ("UCB1", RED), "klucb": ("KL-UCB", NAVY), "ts": ("Thompson Sampling", GREEN)}


def draw6(fig, t, cues, data):
    res = data["sim"]
    i = which(cues, t)
    frame_base(fig, SCENES[6]["title"], SCENES[6]["lines"][i][0])
    p = prog(cues, 0, t)
    for j, (name, title) in enumerate((("low", "平均 (0.10, 0.05, 0.02)：0 に近い"), ("mid", "平均 (0.6, 0.5, 0.4)：中ほど"))):
        ax = fig.add_axes([0.07 + 0.47 * j, 0.22, 0.40, 0.55])
        hl = (i == 1 and j == 0) or (i == 2 and j == 1) or i >= 3
        for pol in ("ucb1", "klucb", "ts"):
            if pol == "ts" and i < 3:
                continue
            d = res[name][pol]
            m = d["times"] <= 10 ** (4 * p) if i == 0 else np.ones(len(d["times"]), bool)
            lab, c = LAB[pol]
            ax.plot(d["times"][m], d["curve"][m], color=c, lw=2.6, label=lab)
            if i >= 1 and m.all():
                ax.text(10500, d["curve"][-1], f"{d['curve'][-1]:.0f}", fontsize=14, color=c, weight="bold", va="center")
        ax.set_xscale("log"), ax.set_xlim(1, 10000), ax.set_ylim(0, 200)
        ax.set_title(title, fontsize=16, weight="bold", color=NAVY if hl else GRAY)
        ax.set_xlabel("時刻 t（対数）", fontsize=13)
        if j == 0:
            ax.set_ylabel("平均の累積後悔（100 回）", fontsize=13)
        ax.legend(fontsize=12, loc="upper left", frameon=False)
        clean(ax)
    if i == 4:
        box(fig, 0.12, 0.45, 0.76, 0.09, YEL, z=2)
        fig.text(0.5, 0.495, r"定理：$f(t) = \ln t + 3\ln\ln t$　／　実用の推奨：$f(t) = \ln t$（c = 0、この比較もこちら）",
                 fontsize=16, color=NAVY, ha="center", va="center")


# ------------------------------------------------------------------ 場面 7：マルチプレイヤー
def draw7(fig, t, cues, data):
    i = which(cues, t)
    frame_base(fig, SCENES[7]["title"], SCENES[7]["lines"][i][0])
    # 2 人の index（同じ記録 → 同じ index）を棒で描き、R-SKL では小さなゆらぎを足す
    base = np.array([0.60, 0.57])
    tt = 20
    for seed in range(100):
        z = np.random.default_rng(seed).normal(size=(2, 2))
        if np.argmax(base + z[0] / tt) != np.argmax(base + z[1] / tt):
            break
    for m in range(2):
        x0 = 0.08 + 0.30 * m
        box(fig, x0, 0.20, 0.27, 0.55, "#F4F5FA")
        fig.text(x0 + 0.135, 0.71, f"プレイヤー {m + 1} の index", fontsize=16, weight="bold", color=PL_C[m], ha="center")
        ax = fig.add_axes([x0 + 0.04, 0.27, 0.20, 0.38])
        v = base + (z[m] / tt if i >= 2 else 0)
        ax.bar([0, 1], v, color=ARM2_C, width=0.6)
        ax.set_ylim(0.4, 0.7), ax.set_xticks([0, 1], ["腕 1", "腕 2"], fontsize=13)
        ax.tick_params(axis="y", labelsize=10)
        clean(ax)
        k = int(np.argmax(v))
        ax.plot([k], [v[k] + 0.015], marker="v", ms=14, color=YEL, mec=NAVY, mew=1.5)
    rows = []
    if i == 0:
        rows = [("Selfish KL-UCB", dict(fontsize=19, weight="bold", color=NAVY, dy=0.065)),
                ("各プレイヤーが", dict(fontsize=15, color=INK, dy=0.045)),
                ("自分の観測だけで", dict(fontsize=15, color=INK, dy=0.045)),
                ("KL-UCB の index を計算", dict(fontsize=15, color=INK, dy=0.045))]
    elif i == 1:
        rows = [("記録がそろうと", dict(fontsize=17, weight="bold", color=RED, dy=0.055)),
                ("index も同じ", dict(fontsize=17, weight="bold", color=RED, dy=0.055)),
                ("→ 同じ腕を選んで衝突", dict(fontsize=17, weight="bold", color=RED, dy=0.055))]
    else:
        rows = [("R-SKL", dict(fontsize=19, weight="bold", color=NAVY, dy=0.065)),
                (r"$U_{m,k}(t) + Z_{m,k} / t$", dict(fontsize=20, color=INK, dy=0.07)),
                ("Z：標準正規分布の乱数", dict(fontsize=14, color=INK, dy=0.06)),
                (f"（図は t = {tt}）", dict(fontsize=13, color=GRAY, dy=0.06))]
        if i >= 3:
            rows += [("t が大きいほど", dict(fontsize=15, weight="bold", color=GREEN, dy=0.045)),
                     ("ゆらぎは小さい", dict(fontsize=15, weight="bold", color=GREEN, dy=0.045)),
                     ("→ KL-UCB の良さが残る", dict(fontsize=15, weight="bold", color=GREEN, dy=0.05))]
    side_panel(fig, None, rows, x=0.69, y0=0.20)


# ------------------------------------------------------------------ 場面 8：まとめ
def draw8(fig, t, cues, data):
    i = which(cues, t)
    frame_base(fig, SCENES[8]["title"], SCENES[8]["lines"][i][0])
    items = [("UCB（UCB1）", "平均 + √(2 ln t / N) の上限で選ぶ。後悔は O(log T)（Auer et al. 2002）"),
             ("UCB の弱点", "上乗せが平均の位置を考えない → 0 や 1 の近くで探索しすぎる"),
             ("KL-UCB", "KL で上限を決める。Bernoulli で漸近最適（Garivier & Cappé 2011）"),
             ("つながり", "各プレイヤーが KL-UCB → Selfish KL-UCB、+ Z/t → R-SKL")]
    for j, (h, b) in enumerate(items):
        al = float(np.clip((t - cues[j][0]) / 0.5, 0, 1))
        y = 0.76 - 0.15 * j
        box(fig, 0.05, y - 0.055, 0.90, 0.11, YEL if j == 2 else LIGHT)
        fig.text(0.07, y, h, fontsize=17, weight="bold", color=NAVY, va="center", alpha=al)
        fig.text(0.25, y, b, fontsize=15, color=INK, va="center", alpha=al)


DRAW = [draw0, draw1, draw2, draw3, draw4, draw5, draw6, draw7, draw8]


def build_data():
    return dict(hist=ucb_run(), sim=pickle.load(open(os.path.join(HERE, "build", "ucb_sim.pkl"), "rb")))



if __name__ == "__main__":
    Video(SCENES, DRAW, build_data, out=os.path.join(HERE, "ucb_klucb_explainer.mp4")).main(sys.argv[1:])
