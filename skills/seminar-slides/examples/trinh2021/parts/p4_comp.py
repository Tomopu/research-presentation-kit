# ================================================================= Part 5: Comparison with Izumi et al. (2026)
s = d.divider("Comparison with Izumi et al. (2026)")
s.notes("Izumi et al. (2026) との比較")

# ---- Izumi et al. の手法（修論中間発表 5・6 枚目のフェーズの帯）
s = d.slide("The Method of Izumi et al. (2026)",
            lead="Izumi et al. extend Huang et al. (2022) by using $n$ good arms as parallel channels, "
                 "so that $n$ groups of players can send at the same time.")
y1 = s.top + 0.42
s.heading(C.L, s.top - 0.05, "Huang et al. (2022): 3 initialization phases + 1 exploration phase")
s.paste(RTH, 5, [5, 6, 7, 8, 9, 27, 28, 30], dy=y1 - 3.12, retext={
    5: ("① Find a good arm",), 6: ("Rank players",), 7: ("③ Count players",), 8: ("④ Explore and assign",),
    9: ("via one good arm $\\tilde{k}$", 16, "005F00", True, "ctr"),
    27: ("via one good arm $\\tilde{k}$", 16, "005F00", True, "ctr"),
    28: ("via one good arm $\\tilde{k}$", 16, "C00000", True, "ctr")})
y2 = y1 + 1.55
s.heading(C.L, y2 - 0.47, "Izumi et al. (2026): the same 4 phases, with $n$ channels")
s.paste(RTH, 6, [4, 5, 6, 7, 8, 9, 10, 11], dy=y2 - 3.12, retext={
    4: ("① Find $n$ good arms", 15, "005F00", True, "ctr"), 5: ("Rank players",), 6: ("③ Count players",),
    7: ("④ Explore and assign",),
    8: ("via $n$ good arms", 16, "005F00", True, "ctr"),
    9: ("via $n$ good arms", 16, "005F00", True, "ctr"),
    10: ("via $n$ good arms", 16, "D72727", True, "ctr")})
yb = y2 + 1.15
s.bullets(C.L, yb, C.W, [
    "Messages sent one after another in a phase:  $M-1$  →  $\\lceil M/n\\rceil + n - 2$   (main setting: $15$ → {red:6}).",
    "Both methods have a {blue:proved regret bound}, and R-SKL has none."], size=20, gap=6)
s.notes("Izumi et al. (2026) の手法\n"
        "\n"
        "Izumi et al. は Huang et al. (2022) を拡張し、good arm を $n$ 本、並列の通信路として使う。これで $n$ 組のプレイヤーが同時に送信できる。\n"
        "\n"
        "・（上の帯）Huang et al.：① good arm を 1 本見つける → ② ランク付け → ③ 人数の推定（ここまで初期化）→ ④ 探索と割当。どのフェーズも good arm $\\tilde{k}$ 1 本で通信する。\n"
        "・（下の帯）Izumi et al.：同じ 4 フェーズだが、good arm $n$ 本で通信する。\n"
        "・1 フェーズで順番に送る回数は $M-1$ から $\\lceil M/n\\rceil+n-2$ に減る。主設定（$M=16$、$n=4$）では 15 → 6。\n"
        "・どちらの手法もリグレット上界が証明されている。R-SKL にはない。\n"
        "\n"
        "【口頭補足】\n"
        "・Izumi et al. の上界では、通信項の係数が $M$ から $M/n+n-1$ に下がる代わりに、初期化項と通信項に $\\gamma=\\mu_{(1)}/\\mu_{(n)}$ が掛かる。$n=1$ のとき Huang et al. の手法に一致する。")

# ---- 比較の設定
s = d.slide("Setup of the Comparison",
            lead="R-SKL was run in the same simulator and the same environments as the method of Izumi et al., "
                 "in two versions: $c=0$ of the paper text and $c=3$ of the authors' code.")
y = s.table(C.L, s.top, [3.0, 9.12], [
    ["Item", "Value"],
    ["Main setting", "$K=40$, $M=16$, $T=10^7$, $\\delta = 1/(T\\ln T)$"],
    ["Means", "linearly spaced from 0.9 to 0.1, arm order shuffled in each trial"],
    ["Trials", "100 (steep $(20,8)$: 50, R-SKL $c=3$ in the main setting: 30)"],
    ["Other sizes", "$(10,4)$ $T=10^6$,  $(20,8)$ $T=2\\times10^6$,  $(30,12)$ $T=3\\times10^6$,  steep $(20,8)$ $T=10^6$"]],
    size=16, row_h=0.38, col_align=["ctr", "l"])
yh = s.heading(C.L, y + 0.18, "Check of our R-SKL implementation:")
yb = s.bullets(C.L, yh, C.W, [
    "3,000 random states: the chosen arm agrees with the paper's definition in every state.",
    "$K=2,3,5$: the mean regret agrees with the authors' code within 4%."], size=18, gap=4)
s.box(C.L, yb + 0.18, C.W, None, "$c=3$ gives $1.45$–$1.85$ times higher regret than $c=0$, and the conclusions do not change.",
      fill="yellow", line="amber", lw=0.75, size=18, align="l", ins=(0.2, 0.08, 0.2, 0.08))
s.notes("比較の設定\n"
        "\n"
        "R-SKL を、Izumi et al. の手法と同じシミュレーター・同じ環境で動かした。論文本文どおりの $c=0$ と、著者のコードどおりの $c=3$ の 2 つの版を使った。\n"
        "\n"
        "・（表）\n"
        "  - 主設定：$K=40$、$M=16$、$T=10^7$、$\\delta=1/(T\\ln T)$。\n"
        "  - 平均は 0.9〜0.1 の等間隔、試行ごとに腕の並びをランダムにする。\n"
        "  - 試行数 100（急減衰は 50、主設定の $c=3$ だけ 30）。\n"
        "  - ほかの規模：$(10,4)$、$(20,8)$、$(30,12)$、急減衰 $(20,8)$。\n"
        "・R-SKL の実装の確認：\n"
        "  - ランダムな 3,000 状態で、選ぶ腕は論文の定義とすべて一致。\n"
        "  - $K=2,3,5$ で、平均リグレットは著者のコードと 4% 以内で一致。\n"
        "・（黄色の箱）$c=3$ は $c=0$ の 1.45〜1.85 倍のリグレットになるが、結論は変わらない。\n"
        "\n"
        "【口頭補足】\n"
        "・Huang et al. と Izumi et al. の手法は、最終割当が決まった時点でシミュレーションを止め、残り時間は固定割当の期待損失を足す。R-SKL は $T$ まで実際に動かす。\n"
        "・$c=3$ の版は、探索関数が $\\log t+3\\log\\log t$ で指数が全体に高くなる。衝突したステップ数は $c=0$ の約 1.8 倍だった。")

# ---- 主設定の結果
s = d.slide("Main Setting: Result",
            lead="In the main setting, the regret of R-SKL is about **580 times smaller** than the best result "
                 "of Izumi et al. ($n=4$).")
y0 = s.top
s.bar_chart(C.L, y0, 7.6, BOTTOM - y0, ["Huang", "Izumi n=4", "R-SKL c=3", "R-SKL c=0"],
            [("regret", [19427536, 10047926, 26364, 17240], ["gray", "ink", "pale-blue", "red"])],
            horizontal=True, log=True, size=14, value_range=(1000, 100000000), value_title="cumulative regret (log scale)")
xb = 8.35
y = s.table(xb, y0 + 0.05, [2.6, 1.71], [
    ["Method", "Regret"],
    ["Huang et al.", "$19{,}427{,}536$"],
    ["Izumi et al. ($n=4$)", "$10{,}047{,}926$"],
    ["R-SKL ($c=0$)", "$17{,}240$"],
    ["R-SKL ($c=3$)", "$26{,}364$"]], size=16, row_h=0.38, col_align=["l", "r"])
s.bullets(xb, y + 0.18, C.R - xb, ["Huang / R-SKL $\\approx 1{,}127$", "Izumi / R-SKL $\\approx 583$",
                                   "$K=40$, $M=16$, $T=10^7$"], size=18, gap=4)
s.notes("主設定の結果\n"
        "\n"
        "主設定では、R-SKL のリグレットは Izumi et al. の最良（$n=4$）の **約 580 分の 1** である。\n"
        "\n"
        "・（グラフ・表、対数軸）Huang et al. 19,427,536、Izumi et al.（$n=4$）10,047,926、R-SKL $c=0$ 17,240、R-SKL $c=3$ 26,364。\n"
        "・比は Huang/R-SKL ≈ 1,127、Izumi/R-SKL ≈ 583。$K=40$、$M=16$、$T=10^7$。\n"
        "\n"
        "【口頭補足】\n"
        "・AJCAI 論文は「上界が証明された手法どうしの比較」として Huang et al. と比べ、R-SKL は practical reference point として載せている。\n"
        "・試行数は 100（R-SKL の $c=3$ だけ 30）。")

# ---- 5 設定
s = d.slide("Results Across Five Settings",
            lead="In all five settings, the regret of R-SKL is **199 to 583 times smaller** than the best result of Izumi et al.")
y0 = s.top
figlabel(s, C.L, y0 - 0.05, 7.6, "Regret of Izumi et al. (best $n$)  /  regret of R-SKL ($c=0$)", 16)
s.bar_chart(C.L, y0 + 0.38, 7.6, BOTTOM - y0 - 0.38,
            ["(10, 4)", "(20, 8)", "(30, 12)", "(40, 16)", "steep (20, 8)"],
            [("ratio", [279, 438, 537, 583, 199], ["ink", "ink", "ink", "red", "gray"])],
            horizontal=True, size=16, value_range=(0, 700), labels=True, fmt="0", gap=55)
xb = 8.45
yy = s.heading(xb, y0 + 0.35, "$(M, K)$ with $K = 2.5M$:", w=C.R - xb)
yy = s.bullets(xb, yy + 0.05, C.R - xb, [
    "The gap grows with the size of the problem.",
    "Coordinated methods need $O(K^2)$ steps only to initialize.",
    "Steep means: parallel channels give no gain."], size=18, gap=10)
s.notes("5 つの設定での結果\n"
        "\n"
        "5 つの設定すべてで、R-SKL のリグレットは Izumi et al. の最良の **199〜583 分の 1** である。\n"
        "\n"
        "・（グラフ）Izumi et al. の最良の $n$ でのリグレットを、R-SKL（$c=0$）のリグレットで割った比。$(10,4)$ で 279、$(20,8)$ で 438、$(30,12)$ で 537、$(40,16)$ で 583、急減衰 $(20,8)$ で 199。\n"
        "・問題が大きいほど差は広がる。\n"
        "・協調型の手法は、初期化だけで $O(K^2)$ ステップかかる。\n"
        "・平均が急に減る設定では、並列化の利得がない（$n=1$ が最良）。\n"
        "\n"
        "【口頭補足】各設定の値（Huang ／ Izumi の最良 ／ R-SKL $c=0$）\n"
        "・$(40,16)$, $T=10^7$：19,427,536 ／ 10,047,926（$n=4$）／ 17,240。\n"
        "・$(30,12)$, $T=3\\times10^6$：7,838,699 ／ 4,427,049（$n=3$）／ 8,247。\n"
        "・$(20,8)$, $T=2\\times10^6$：2,382,434 ／ 1,563,497（$n=2$）／ 3,569。\n"
        "・$(10,4)$, $T=10^6$：292,255 ／ 225,124（$n=2$）／ 807。\n"
        "・急減衰 $(20,8)$, $T=10^6$：1,239,788 ／ 1,239,788（$n=1$）／ 6,234。")

# ---- 勝ち負け
s = d.slide("Where the Method of Izumi et al. Wins and Loses",
            lead="The method of Izumi et al. beats Huang et al. when the means decay gradually, but **it never beats R-SKL**.")
y0 = s.top
fw = 6.3
s.image(F("regret_huang_vs_izumi.png"), C.L, y0, w=fw)
s.text(C.L, y0 + fw * 960 / 1600, fw, "$(40,16)$: Huang et al. (black dashed) and Izumi et al. with $n=1,\\dots,8$", 14, "warm", align="ctr")
xb = 7.1
y = s.heading(xb, y0, "{green:Wins} (against Huang et al.)", w=C.R - xb)
y = s.bullets(xb, y, C.R - xb, ["$23.0$–$48.3\\%$ lower regret in the four settings with gradual means.",
                                 "The best $n$ is 2, 2, 3 and 4."], size=18, gap=4)
y = s.heading(xb, y + 0.30, "{red:Loses}", w=C.R - xb)
y = s.bullets(xb, y, C.R - xb, ["Against R-SKL: 199–583 times higher regret.",
                                 "Too many channels ($n=7, 8$) are worse than Huang et al.",
                                 "Steep means: $n=1$ is the best."], size=18, gap=4)
s.notes("Izumi et al. の手法が勝つところ・負けるところ\n"
        "\n"
        "Izumi et al. の手法は、平均がゆるやかに減る設定で Huang et al. を上回るが、**R-SKL を上回る設定はない**。\n"
        "\n"
        "・（図）$(40,16)$ での Huang et al.（黒の破線）と Izumi et al. の $n=1$〜8 の累積リグレット。\n"
        "・勝ち（Huang et al. に対して）：\n"
        "  - 平均がゆるやかに減る 4 設定で、リグレットを 23.0〜48.3% 削減。\n"
        "  - 最良の $n$ は 2, 2, 3, 4。\n"
        "・負け：\n"
        "  - R-SKL に対しては、リグレットが 199〜583 倍。\n"
        "  - 通信路が多すぎる（$(40,16)$ の $n=7, 8$）と Huang et al. より悪い。\n"
        "  - 平均が急に減る設定では $n=1$ が最良。\n"
        "\n"
        "【口頭補足】\n"
        "・目指すものが違う。Izumi et al. は上界が証明された手法の改善で、R-SKL には上界がない。\n"
        "・急減衰の設定で $n=2$ の最終割当が成功したのは 50 試行中 29 試行、$n=3, 4$ は 0 試行。")

# ---- コスト 1：初期化
s = d.slide("Why R-SKL Is Faster (1): No Initialization",
            lead="In the main setting, the initialization of Huang et al. alone loses about 5.4 million regret, "
                 "which is **more than 300 times** the whole regret of R-SKL.")
yc0 = s.top
s.paste(RTH, 5, [5, 6, 7, 8, 30], dy=yc0 - 3.12, retext={
    5: ("① Find a good arm",), 6: ("Rank players",), 7: ("③ Count players",), 8: ("④ Explore and assign",)})
yl = yc0 + 0.63
for cxx, t, c in [(2.20, "111,744 steps", "005F00"), (5.10, "120,960 steps", "005F00"), (8.10, "243,200 steps", "005F00"),
                  (11.15, "until assignment", "C00000")]:
    s.clabel(cxx, yl, t, 16, c, True, w=3.0)
yc = yl + 0.50
tg = [i / 10 for i in range(31)]
hu = [0, 1028329, 2173681, 3336192, 4506003, 5666554, 6858805, 8030645, 9222182, 10391259, 11562629, 12756475, 13895666,
      15062352, 16148900, 17229954, 18105323, 18681849, 18987205, 19114495, 19175894, 19236488, 19300307, 19313393,
      19349075, 19359595, 19369430, 19379381, 19402191, 19426311, 19426416]
ou = [0, 1026283, 2088594, 3190825, 4356022, 5505274, 6622467, 7671600, 8509262, 9084075, 9393602, 9558167, 9640139,
      9775109, 9811816, 9870776, 9872805, 9879173, 9949399, 9955649, 9956788, 9957872, 9958994, 9961087, 10024638,
      10047926, 10047926, 10047926, 10047926, 10047926, 10047926]
s.xy_chart(C.L, yc, 8.0, BOTTOM - yc, [
    ("Huang", tg, [v / 1e6 for v in hu], "gray", 2.5),
    ("Izumi (n = 4)", tg, [v / 1e6 for v in ou], "ink", 2.5),
    ("R-SKL (whole run)", [0, 3.0], [0.01724, 0.01724], "red", 2.5),
    ("end of initialization", [0.476, 0.476], [0, 20], "green", 1.5, True)],
    x_title="t  (million steps)", y_title="cumulative regret (million)",
    x_range=(0, 3), y_range=(0, 20), size=14, legend=True, legend_pos="t", x_fmt="0.0", y_fmt="0")
xb = 8.85
s.bullets(xb, yc + 0.25, C.R - xb, [
    "Huang et al. lose {red-n:5.4 million} before the initialization ends.",
    "R-SKL loses {red-n:17,240} in the whole run, because it has no phases."], size=18, gap=12)
s.notes("R-SKL が速い理由（1）：初期化がない\n"
        "\n"
        "主設定では、Huang et al. の初期化だけで約 540 万のリグレットを失う。これは R-SKL のリグレット全体の **300 倍を超える**。\n"
        "\n"
        "・（上の帯）Huang et al. の 4 フェーズと、各初期化フェーズのステップ数：① 111,744、② 120,960、③ 243,200。④ は割当が決まるまで。\n"
        "・（グラフ）主設定（$K=40$, $M=16$, $T=10^7$）の平均累積リグレット。灰色が Huang et al.、紺が Izumi et al.（$n=4$）、赤が R-SKL の全期間の値（この目盛ではほぼ 0）、緑の破線が Huang et al. の初期化の終わり。\n"
        "・Huang et al. は、初期化が終わるまでに約 540 万を失う。\n"
        "・R-SKL はフェーズがないので、全期間で 17,240 しか失わない。\n"
        "\n"
        "【口頭補足】\n"
        "・初期化中の 1 ステップあたりのリグレットは約 11.3 で、最大値 $\\sum_{m\\leq16}\\mu_{(m)}=11.94$ の 95%。初期化中はほとんど報酬を得られない。\n"
        "・Izumi et al.（$n=4$）は初期化を 475,904 ステップから 268,616 ステップに短縮する。\n"
        "・出典は mpmab-simu の camera_ready_20260925_K40_M16_main。初期化の終わりでの平均累積リグレットは 5,384,495（17,240 の約 312 倍）。")

# ---- コスト 2：衝突による通信（修論中間発表 4 枚目の図）
s = d.slide("Why R-SKL Is Faster (2): No Communication",
            lead="Coordinated methods send each bit by colliding on purpose for $\\tau = 76$ steps, "
                 "during which the receiver earns nothing.")
s.paste(RTH, 4, [2, 6, 8] + list(range(9, 39)), dy=-0.86, retext={
    6: ('Send "0": collide',), 8: ('Send "1": stay away',),
    26: ("Receiver", None, None, None, None, 1.2), 28: ("Receiver", None, None, None, None, 1.2),
    27: ("Sender", None, None, None, None, 1.2), 29: ("Sender", None, None, None, None, 1.2),
    21: ("$\\tau$ pulls", 16, "body", False, "ctr", 1.1), 25: ("$\\tau$ pulls", 16, "body", False, "ctr", 1.1),
    35: ("collide every time",), 36: ("receiver always gets 0",),
    37: ("$r=1$ at least once\nin $\\tau$ pulls (w.h.p.)", 14, "body", False, "ctr"), 38: ('receiver decodes "1"',)})
s.text(C.L, 6.12, C.W, "Steps with a collision in $(30,12)$:   Huang et al. $875{,}009$,   Izumi et al. $503{,}897$,   R-SKL {red:2,637}.", 20)
s.notes("R-SKL が速い理由（2）：通信がない\n"
        "\n"
        "協調型の手法は、わざと衝突を起こして 1 ビットずつ送る。1 ビットに $\\tau=76$ ステップかかり、その間、受信者は報酬を得られない。\n"
        "\n"
        "・（左）「0」を送る：受信者が座る good arm $\\tilde{k}$ に送信者も来て、$\\tau$ 回引く。毎回衝突し、受信者の報酬は常に 0。\n"
        "・（右）「1」を送る：送信者は別の腕 $k$ を $\\tau$ 回引く。受信者は高い確率で 1 回は $r=1$ を得て、「1」を受け取ったと判断する。\n"
        "・$(30,12)$ で衝突が起きたステップ数：Huang et al. 875,009、Izumi et al.（$n=3$）503,897、R-SKL 2,637。\n"
        "\n"
        "【口頭補足】\n"
        "・$\\tau=\\lceil\\ln(1/\\delta)/\\tilde{\\mu}\\rceil$（$\\tilde{\\mu}$ は good arm の平均の下限）。主設定では 76。$\\delta=1/(T\\ln T)$ を小さく取るほど長くなる。")

# ---- 分かっていることと推測（表にしない）
s = d.slide("What We Know and What We Guess",
            lead="R-SKL is fast mainly because it does not pay the fixed costs of coordination, "
                 "but this is an empirical picture and not a proof.")
y0 = s.top
cw = 3.9
groups = [("From the paper", "blue", "lead", "ink",
           ["No prior knowledge, no phases, no communication.",
            "One player: a bad arm is tried only about $\\log T/d(\\mu_k,\\mu_{(1)})$ times."]),
          ("From our data", "green", "pale-green", "green",
           ["Initialization of Huang et al.: about 5.4 million regret.",
            "Collisions: $875{,}009$ steps for Huang et al., $2{,}637$ for R-SKL."]),
          ("Guess", "red", "pale-red", "red",
           ["Collisions push the players onto different arms.",
            "The regret is $O(\\log T)$ for $M\\geq2$ (conjecture)."])]
for i, (head, hc, fill, ln, items) in enumerate(groups):
    x = C.L + i * (cw + 0.21)
    s.text(x, y0, cw, "{%s:%s}" % (hc, head), 20, align="ctr")
    s.box(x, y0 + 0.48, cw, 2.05, "\n".join(items), fill=fill, line=ln, lw=1.0, size=18, align="l", anchor="t",
          bullet="•", gap=10, radius=0.08, ins=(0.15, 0.15, 0.15, 0.1))
s.box(C.L, y0 + 2.80, C.W, None,
      "**Weak points of R-SKL:** it has no regret bound, and it is worse than SIC-MMAB2 when all means are equal (Section 3.3).",
      fill="yellow", line="amber", lw=0.75, size=18, align="l", ins=(0.2, 0.1, 0.2, 0.1))
s.notes("分かっていることと推測\n"
        "\n"
        "R-SKL が速い主な理由は、協調の固定費を払わないことである。ただしこれは実験から見た姿であり、証明ではない。\n"
        "\n"
        "・原論文から分かること：\n"
        "  - 事前知識・フェーズ・通信を必要としない（1.3 節・7 節）。\n"
        "  - 1 人なら、悪い腕 $k$ を試す回数は約 $\\log T/d(\\mu_k,\\mu_{(1)})$ だけ（命題 2）。\n"
        "・私のデータから分かること：\n"
        "  - Huang et al. の初期化は、主設定で約 540 万のリグレット。\n"
        "  - $(30,12)$ で衝突が起きたステップ数は、Huang et al. 875,009、R-SKL 2,637。\n"
        "・推測：\n"
        "  - 衝突がプレイヤーを別々の腕に押しやる。\n"
        "  - $M\\geq2$ でリグレットは $O(\\log T)$（著者の予想）。\n"
        "・（黄色の箱）R-SKL の弱点：リグレット上界がない。すべての平均が等しいときは SIC-MMAB2 より悪い（3.3 節）。\n"
        "\n"
        "【口頭補足】\n"
        "・シミュレーターは Huang et al. と Izumi et al. の手法を割当の確定で止めて残りの期待損失を足し、R-SKL は $T$ まで動かす。これは協調型の手法にやや有利な条件である。\n"
        "・上界のオーダーが同じ $\\log T$ でも、$K^2M$ や $KM^2\\ln^2(1/\\Delta_M)$ に掛かる定数が大きいと、$T=10^7$ ではこの固定費が支配的になる。")
