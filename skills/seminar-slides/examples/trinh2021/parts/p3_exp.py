# ================================================================= Part 4: Numerical Experiments
s = d.divider("Numerical Experiments")
s.notes("数値実験")

# ---- 実験設定 (1/2)：比べる手法
s = d.slide("Experimental Setup", part="(1/2)",
            lead="R-SKL gets no information, while each earlier algorithm gets the true value of the parameter it needs.")
y0 = s.top + 0.15
cw = 2.85
cards = [("R-SKL", "(this paper)", "{red:nothing}", True),
         ("SIC-MMAB2", "[Boursier+ 2019]", "true $\\mu_{(K)}$", False),
         ("EC-SIC  ($p=5$)", "[Shi+ 2020]", "true $\\mu_{(K)}$", False),
         ("Lugosi 2", "[Lugosi+ 2018]", "true $\\mu_{(M)}$", False)]
for i, (name, ref, given, me) in enumerate(cards):
    x = C.L + i * (cw + 0.24)
    s.box(x, y0, cw, 1.05, "**%s**\n%s" % (name, ref), fill="pale-red" if me else "lead", line="red" if me else "ink",
          lw=1.0, size=18, radius=0.08)
    s.shape("downArrow", x + cw / 2 - 0.18, y0 + 1.12, 0.36, 0.38, fill="ink", line="ink")
    s.text(x + cw / 2 + 0.25, y0 + 1.12, 1.2, "is given", 14, "warm")
    s.box(x, y0 + 1.58, cw, 0.70, given, fill="white", line="red" if me else "line-gray", lw=1.0, size=20, prst="rect")
s.bullets(C.L, y0 + 2.65, C.W, [
    "The earlier algorithms need only a bound, but they get the exact value, which is the best possible input.",
    "Every curve is the average of at least 50 runs, and shaded areas are 95% confidence intervals."], size=20, gap=10)
s.notes("実験設定（1/2）\n"
        "\n"
        "R-SKL には何も与えず、既存手法には、それぞれが必要とするパラメータの真の値を与える。\n"
        "\n"
        "・（カード）比べる手法と、与える情報：\n"
        "  - R-SKL（本論文）：何も与えない。\n"
        "  - SIC-MMAB2 [Boursier+ 2019]：真の $\\mu_{(K)}$。\n"
        "  - EC-SIC（$p=5$）[Shi+ 2020]：真の $\\mu_{(K)}$。\n"
        "  - Lugosi 2 [Lugosi+ 2018]：真の $\\mu_{(M)}$。\n"
        "・既存手法は下界が分かれば動くが、真の値を与えている。これは最も有利な入力である。\n"
        "・どの曲線も 50 回以上の平均で、色付きの帯は 95% 信頼区間。\n"
        "\n"
        "【口頭補足】\n"
        "・Lugosi & Mehrabian の Alg. 1 は図に入れていない。探索だけで $1.2\\times10^6$ ステップを超え、どの設定でも線形リグレットになるため（原文 3 節）。\n"
        "・$M=2$、$K=3$ の図にだけ、Bubeck & Budzinski (2020) の協調型手法も入っている。")

# ---- 実験設定 (2/2)：環境
s = d.slide("Experimental Setup", part="(2/2)",
            lead="The arm means are linearly spaced between $\\mu_{(1)}$ and $\\mu_{(K)}$, and three ranges are tested "
                 "for each pair $(M,K)$.")
y = s.eq(r"\mu_{(k)} = \mu_{(1)}\frac{K-k}{K-1} + \mu_{(K)}\frac{k-1}{K-1},\qquad k = 1,\dots,K", s.top - 0.10, size=20, number="(9)")
xa, xz = 3.4, 9.2
sx = lambda v: xa + v * (xz - xa)
envs = [("(i)", "$0.99, \\dots, 0.01$", [0.99, 0.745, 0.5, 0.255, 0.01], "hardest for SIC-MMAB2"),
        ("(ii)", "$0.2, \\dots, 0.1$", [0.2, 0.175, 0.15, 0.125, 0.1], ""),
        ("(iii)", "$0.9, \\dots, 0.8$", [0.9, 0.875, 0.85, 0.825, 0.8], "easiest for SIC-MMAB2")]
for i, (tag, rng, pts, note) in enumerate(envs):
    yy = y + 0.10 + i * 0.66
    s.text(C.L, yy, 2.8, "**%s**  %s" % (tag, rng), 20)
    s.line(xa, yy + 0.22, xz, yy + 0.22, "warm", 1.25)
    for v in (0, 0.5, 1.0):
        s.line(sx(v), yy + 0.14, sx(v), yy + 0.30, "warm", 1.25)
    for v in pts:
        s.shape("ellipse", sx(v) - 0.09, yy + 0.13, 0.18, 0.18, fill="ink", line="ink")
    if note:
        s.text(xz + 0.2, yy + 0.02, C.R - xz - 0.2, note, 16, "red")
yy = y + 0.10 + 3 * 0.66 - 0.12
for v, t in ((0, "$0$"), (0.5, "$0.5$"), (1.0, "$1$")):
    s.clabel(sx(v), yy, t, 16, "warm", w=0.8)
s.text(xa, yy + 0.30, xz - xa, "means of the arms $\\mu_{(1)},\\dots,\\mu_{(K)}$ (drawn for $K=5$)", 14, "warm", align="ctr")
s.text(C.L, yy + 0.72, C.W, "Sizes: $(M,K) = (2,3),\\ (2,5),\\ (5,10),\\ (10,15)$.   Horizon: $T = 2\\times10^6$.", 20)
s.notes("実験設定（2/2）\n"
        "\n"
        "腕の平均は $\\mu_{(1)}$ から $\\mu_{(K)}$ まで等間隔に並べ、各 $(M,K)$ について 3 通りの範囲を試す。\n"
        "\n"
        "・式 (9)：平均が等間隔の環境（原文 3.1 節）。\n"
        "・（数直線、$K=5$ の場合を描いた）3 通りの範囲：\n"
        "  - (i) $0.99,\\dots,0.01$：SIC-MMAB2 に最も不利。\n"
        "  - (ii) $0.2,\\dots,0.1$。\n"
        "  - (iii) $0.9,\\dots,0.8$：SIC-MMAB2 に最も有利。\n"
        "・規模は $(M,K)=(2,3),(2,5),(5,10),(10,15)$、期間は $T=2\\times10^6$。\n"
        "\n"
        "【口頭補足】\n"
        "・SIC-MMAB2 のフェーズの長さは $1/\\mu_{(K)}$ に比例する。(i) の $(M,K)=(2,3)$ では最初の探索フェーズが $4800K\\log(T)/\\mu_{(K)}\\geq2\\times10^7$ で $T$ を超える。(iii) では約 $3\\times10^5$ ステップ。")

# ---- 図 2
heads = ["(ii)  means from 0.2 to 0.1", "(iii)  means from 0.9 to 0.8", "(i)  means from 0.99 to 0.01"]
s = d.slide("Linearly Spaced Means: Results",
            lead="R-SKL has the lowest regret in all 12 environments, and for $(M,K)=(5,10)$ with means from 0.2 to 0.1 "
                 "its regret is **200 times smaller** than that of EC-SIC.")
fw = 3.98
fh = fw * 504 / 864
y0 = s.top - 0.05
for j, (f, h) in enumerate(zip(["31_m5k10_02.png", "31_m5k10_08.png", "31_m5k10_099.png"], heads)):
    x = C.L + j * (fw + 0.09)
    figlabel(s, x, y0 - 0.02, fw, h, 16)
    s.image(F(f), x, y0 + 0.40, w=fw)
s.frame(C.L - 0.02, y0 + 0.37, fw + 0.04, fh + 0.06, "red", 2.0)
y = y0 + 0.40 + fh + 0.10
s.text(C.L, y, C.W, "**Figure 2**, row $(M,K)=(5,10)$, $T=2\\times10^6$.  {red:Orange (R-SKL) stays almost flat at the bottom of every panel.}", 16)
s.bullets(C.L, y + 0.42, C.W, [
    "The other rows $(2,3)$, $(2,5)$ and $(10,15)$ show the same order, and the gap grows with the number of players.",
    "SIC-MMAB2 grows almost linearly when $\\mu_{(K)}$ is small."], size=18, gap=2)
s.notes("期待値が等間隔の環境：結果\n"
        "\n"
        "12 環境すべてで R-SKL のリグレットが最も小さく、$(M,K)=(5,10)$、平均 0.2〜0.1 では、既存最良の EC-SIC の **200 分の 1** である。\n"
        "\n"
        "・図 2 の $(M,K)=(5,10)$ の行、$T=2\\times10^6$。左から (ii) 0.2〜0.1、(iii) 0.9〜0.8、(i) 0.99〜0.01。\n"
        "・オレンジの R-SKL は、どの図でも下でほぼ平ら。赤枠が「200 倍」の環境。\n"
        "・ほかの行 $(2,3)$、$(2,5)$、$(10,15)$ でも順位は同じで、プレイヤーが増えるほど差は広がる。\n"
        "・SIC-MMAB2 は $\\mu_{(K)}$ が小さいとほぼ線形に増える。\n"
        "\n"
        "【口頭補足】\n"
        "・「200 倍」は原文 3.1 節の本文の記述で、数値の表はない。図から読むと EC-SIC は $t=2\\times10^6$ で約 $2.2\\times10^5$。\n"
        "・縦軸の桁は図ごとに違う（$10^4$〜$10^6$）。R-SKL の線が見えないのは「ゼロだから」ではなく「桁が違うから」。\n"
        "・Lugosi 2 が階段状に増えるのは、フェーズ構造の表れ。")

# ---- 図 3
s = d.slide("Varying $\\mu_{(K)}$, $\\Delta$ and $M$",
            lead="R-SKL stays the best when the worst mean, the gap or the number of players changes.")
fw = 6.9
y0 = s.top - 0.05
figlabel(s, C.L, y0 - 0.02, fw, "Final regret when $M = 1,\\dots,9$  ($K=10$, means from 0.9 to 0.1)", 16)
s.image(F("32_M.png"), C.L, y0 + 0.40, w=fw)
fh = fw * 1400 / 2400
s.callout(4.65, y0 + 2.55, 1.6, 0.45, "R-SKL ≈ 0", (5.8, y0 + 0.40 + fh * 0.835), size=16, line="red", color="red")
xb = 7.75
yy = s.heading(xb, y0 + 0.30, "Three experiments (Figure 3):", w=C.R - xb)
yy = s.bullets(xb, yy + 0.05, C.R - xb, [
    "Worst mean $\\mu_{(K)}$ from 0.1 to 0.8.",
    "Gap $\\Delta = \\mu_{(M)}-\\mu_{(M+1)}$ from 0.1 to 0.001.",
    "Number of players $M$ from 1 to 9 (left)."], size=18, gap=8)
s.text(xb, yy + 0.25, C.R - xb, "In all three, R-SKL has the lowest final regret.", 18, "red", True)
s.notes("$\\mu_{(K)}$、$\\Delta$、$M$ を変える\n"
        "\n"
        "最悪の腕の平均、ギャップ、プレイヤー数のどれを変えても、R-SKL が最も良い。\n"
        "\n"
        "・（図）図 3 の右の図：$K=10$、平均 0.9〜0.1 の等間隔で、$M=1$〜9 を変えたときの最終累積リグレット。R-SKL（オレンジ）はほぼ 0。\n"
        "・3 つの実験（図 3、3.2 節）：\n"
        "  - 最悪の腕の平均 $\\mu_{(K)}$ を 0.1〜0.8 で変える（$M=5$, $K=9$）。\n"
        "  - ギャップ $\\Delta=\\mu_{(M)}-\\mu_{(M+1)}$ を 0.1〜0.001 で変える（$M=5$, $K=9$）。\n"
        "  - プレイヤー数 $M$ を 1〜9 で変える（左の図）。\n"
        "・3 つとも、R-SKL の最終リグレットが最も小さい。\n"
        "\n"
        "【口頭補足】\n"
        "・Lugosi 2 は $M$ とともに増え、SIC-MMAB2 は $10^6$ 台のまま。EC-SIC は $K=M$ では動かない。\n"
        "・$\\mu_{(K)}$ が小さいところで SIC-MMAB2 が良く見えるのは、収束していないためである（原文）。")

# ---- 特殊な場合
s = d.slide("A Corner Case: All Means Are Equal",
            lead="Only when all arms have exactly the same mean does SIC-MMAB2 beat R-SKL, and a tiny change of the means "
                 "reverses the result.")
fw = 5.3
y0 = s.top - 0.05
figlabel(s, C.L, y0 - 0.02, fw, "Equal means:  $\\boldsymbol{\\mu}=(0.5,\\dots,0.5)$", 16)
figlabel(s, C.R - fw, y0 - 0.02, fw, "Slightly perturbed:  $\\boldsymbol{\\mu}\\sim\\mathcal{U}([0.49,0.51]^K)$", 16)
s.image(F("33_same.png"), C.L, y0 + 0.40, w=fw)
s.image(F("33_almostsame.png"), C.R - fw, y0 + 0.40, w=fw)
y = y0 + 0.40 + fw * 504 / 864 + 0.08
s.text(C.L, y, C.W, "**Figure 4:** $M=5$, $K=10$.  Left: SIC-MMAB2 stays near 0 and R-SKL reaches about $2.5\\times10^4$.  "
       "Right: SIC-MMAB2 grows almost linearly and passes R-SKL.", 16)
s.notes("特殊な場合：全腕の平均が等しい\n"
        "\n"
        "すべての腕の平均が厳密に等しいときだけ、SIC-MMAB2 が R-SKL を上回り、平均をわずかに変えると結果は逆転する。\n"
        "\n"
        "・図 4：$M=5$、$K=10$。\n"
        "  - 平均が等しい場合（左）：SIC-MMAB2 はほぼ 0、R-SKL は約 $2.5\\times10^4$。\n"
        "  - わずかに揺らした場合（右）：SIC-MMAB2 はほぼ線形に増え、$t=0.75\\times10^6$ 付近で R-SKL を追い越す。\n"
        "\n"
        "【口頭補足】\n"
        "・平均がすべて等しいなら、最初に分かれてしまえば最適で、SIC-MMAB2 はまさにそう動く。R-SKL は KL-UCB の探索を続けるため、他人の腕を試して衝突する。\n"
        "・原文は R-SKL について「its regret still seems logarithmic」と述べるだけで、証明はない。")

# ---- 図 5
s = d.slide("Against Algorithms With Collision Sensing",
            lead="R-SKL often beats SIC-MMAB, which **can see collisions**, and its regret is close to that of MCTopM.")
fw = 6.9
fh = fw * 504 / 864
y0 = s.top - 0.05
figlabel(s, C.L, y0 - 0.02, fw, "$(M,K)=(10,15)$, means from 0.9 to 0.8", 16)
s.image(F("4_m10k15_sic_08.png"), C.L, y0 + 0.40, w=fw)
s.callout(2.2, y0 + 2.40, 2.6, 0.60, "R-SKL below MCTopM", (2.4, y0 + 0.40 + fh * 0.84), size=16, line="red", color="red")
xb = 7.75
yy = s.heading(xb, y0 + 0.30, "Figure 5 (Section 4):", w=C.R - xb)
yy = s.bullets(xb, yy + 0.05, C.R - xb, [
    "MCTopM and SIC-MMAB use collision information, and R-SKL does not.",
    "SIC-MMAB is 10–100 times higher in most environments.",
    "R-SKL is close to MCTopM, and lower when the means are close."], size=18, gap=8)
s.notes("衝突検知ありの手法との比較\n"
        "\n"
        "R-SKL は、**衝突が見える** SIC-MMAB をしばしば上回り、MCTopM にも近い。\n"
        "\n"
        "・（図）図 5 の $(M,K)=(10,15)$、平均 0.9〜0.8 の環境。（吹き出し）R-SKL が MCTopM より下にある。\n"
        "・MCTopM と SIC-MMAB は衝突の情報を使い、R-SKL は使わない。\n"
        "・SIC-MMAB は多くの環境で 1〜2 桁大きい。\n"
        "・R-SKL は MCTopM に近く、平均が近い環境（0.9〜0.8）では下回る。\n"
        "\n"
        "【口頭補足】\n"
        "・図 5 は $(5,10)$ と $(10,15)$ の 2 行 × 平均の範囲 3 列の 6 枚。R-SKL が MCTopM を下回るのは 0.9〜0.8 の列で、$(10,15)$ で最もはっきりしている。")

# ---- 動的な設定
s = d.slide("Players Who Enter and Leave",
            lead="When players enter and leave over time, R-SKL converges much faster than DYN-MMAB "
                 "and earns 91–97% of the optimal reward.")
fw = 5.2
y0 = s.top - 0.05
figlabel(s, C.L, y0 - 0.02, fw, "Players enter one by one ($K=4$)", 16)
s.image(F("52_dynamic.png"), C.L, y0 + 0.40, h=BOTTOM - y0 - 0.40)
xb = 6.6
figlabel(s, xb, y0 - 0.02, C.R - xb, "Players enter and leave ($K=10$)", 16)
yy = s.text(xb, y0 + 0.50, C.R - xb, "Arrivals are Poisson with rate $\\lambda$, and each player stays for an exponential time "
            "with mean $1/\\nu$.", 18)
yy = s.heading(xb, yy + 0.25, "Reward / optimal reward:", w=C.R - xb)
s.text(xb + 0.3, yy + 0.10, 3.0, "**R-SKL**", 24, "red", h=0.7, anchor="ctr")
s.text(xb + 3.2, yy + 0.10, 2.8, "**91–97%**", 36, "red", h=0.7, anchor="ctr")
s.text(xb + 0.3, yy + 0.95, 3.0, "Musical Chairs", 24, h=0.7, anchor="ctr")
s.text(xb + 3.2, yy + 0.95, 2.8, "69–90%", 36, h=0.7, anchor="ctr")
s.text(xb, yy + 1.85, C.R - xb, "Range over 6 pairs $(\\lambda,\\nu)$, $T=10^6$ (Table 2).", 14, "warm")
s.notes("プレイヤーが入って出ていく場合\n"
        "\n"
        "プレイヤーが途中で入ったり出たりする設定でも、R-SKL は DYN-MMAB よりはるかに速く収束し、最適な報酬の 91〜97% を得る。\n"
        "\n"
        "・（左の図）図 6 左：$K=4$、プレイヤーが 1 人ずつ入って出ていかない。DYN-MMAB は約 $4.9\\times10^5$ まで線形に増えてから止まり、R-SKL はほぼ 0。\n"
        "・（右）プレイヤーが出ていきもする設定（5.2 節）：到着はレート $\\lambda$ のポアソン過程、滞在時間は平均 $1/\\nu$ の指数分布。\n"
        "・得た報酬と最適な報酬の比：R-SKL は 91〜97%、Musical Chairs は 69〜90%（$(\\lambda,\\nu)$ の 6 通りでの範囲、$T=10^6$、表 2）。\n"
        "\n"
        "【口頭補足】表 2 の値\n"
        "・R-SKL（$\\lambda=1/1000$ ／ $1/10^4$）：$\\nu=1/500$ で 91±2% ／ 91±1%、$\\nu=1/1000$ で 92±2% ／ 94±1%、$\\nu=1/10^4$ で 93±1% ／ 97±1%。\n"
        "・Musical Chairs（同じ順）：69±1% ／ 69±3%、72±1% ／ 70±3%、90±1% ／ 72±3%。\n"
        "・原文本文は「平均 8 人の現実的な設定で 95%」と書くが、その条件（$\\lambda=1/1000$, $\\nu=1/10^4$）の表の値は 93±1% で一致しない。")
