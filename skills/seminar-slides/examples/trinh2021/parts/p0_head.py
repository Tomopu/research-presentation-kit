# 共通部分：読み込み・図の部品・本人の過去資料のパス
import math
import os
import sys

sys.path.insert(0, os.path.expanduser("~/.claude/skills/seminar-slides/scripts"))
from deck import Deck, C  # noqa: E402

FIG = sys.argv[1] if len(sys.argv) > 1 else "fig"
OUT = sys.argv[2] if len(sys.argv) > 2 else "out.pptx"

# 本人の過去資料（図はここから複製する）
R0421 = "paper0421"   # assets/reference/論文ゼミ_泉0421.pptx（deck.REF）
RTH = "thesis"        # assets/reference/泉知成_修論中間発表スライド_完成.pptx（番号は完成版で xdump.py を使って確かめ直す）

BOTTOM = 6.70   # 本文の下端（これより下に置かない。6.86 から下は余白）


def F(name):
    return os.path.join(FIG, name)


d = Deck()

TOC = ["Introduction", "KL-UCB and Selfish KL-UCB", "Randomized Selfish KL-UCB",
       "Numerical Experiments", "Comparison with Izumi et al. (2026)", "Conclusion"]


def figlabel(s, x, y, w, markup, size=18):
    """図の上の見出し（塗りつぶさない。太字の文字だけ）。"""
    s.text(x, y, w, "**%s**" % markup, size, "ink", align="ctr")
    return y + 0.42


def arms(s, x0, y, K, gap, labels=True, size="s", nums=None):
    """腕を横一列に置き、中心 x のリストを返す。番号は腕の上に数式で。"""
    w = 0.86 if size == "s" else 1.05
    cx = []
    for k in range(K):
        x = x0 + k * gap
        s.slot(x, y, size)
        cx.append(x + w / 2)
        if labels:
            s.clabel(x + w / 2, y - 0.42, "$%s$" % (nums[k] if nums else k + 1), 18, w=1.0)
    return cx


def person(s, cx, y, size="s"):
    w = 0.26 if size == "s" else 0.32
    s.player(cx - w / 2, y, size)


def row_label(s, y, markup, size=18, w=2.2):
    s.text(C.L, y, w, markup, size)


def notebook(s, x, y, who, N, mu, w=4.2, hl=None, size=16):
    """プレイヤーの手帳（N と μ̂ の表）。"""
    rows = [[who, "arm 1", "arm 2", "arm 3"],
            ["$N_{m,k}$"] + [str(v) for v in N],
            ["$\\hat{\\mu}_{m,k}$"] + [f"{v:.2f}" if isinstance(v, float) else str(v) for v in mu]]
    return s.table(x, y, [w * 0.31] + [w * 0.23] * 3, rows, size=size, row_h=0.38, hl_cells=hl)


def dkl(p, q):
    q = min(max(q, 1e-12), 1 - 1e-12)
    return (p * math.log(p / q) if p > 0 else 0) + ((1 - p) * math.log((1 - p) / (1 - q)) if p < 1 else 0)


def klucb(p, n, f):
    if n == 0:
        return 1.0
    lo, hi = p, 1.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if n * dkl(p, mid) <= f:
            lo = mid
        else:
            hi = mid
    return lo


qs = [0.6 + 0.4 * i / 80 for i in range(80)]
