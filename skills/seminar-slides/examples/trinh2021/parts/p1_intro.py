# ================================================================= 表紙・目次・Part 1（導入）
s = d.cover(tag="論文ゼミ 発表資料",
            title="A High Performance, Low Complexity Algorithm for Multi-Player Bandits Without Collision Sensing Information",
            authors="Cindy Trinh¹, Richard Combes¹",
            venue="arXiv preprint arXiv:2102.10200 (2021).",
            date="14.10.2026", grade="M2", name="泉 知成",
            affiliations=["¹ CentraleSupélec, L2S, France"])
s.notes("衝突検知情報なしのマルチプレイヤー・バンディットに対する、高性能かつ低計算量のアルゴリズム\n"
        "\n"
        "・著者：Cindy Trinh、Richard Combes（CentraleSupélec, L2S, フランス）\n"
        "・arXiv:2102.10200（2021）")

s = d.toc(TOC)
s.notes("目次\n"
        "\n"
        "❶ 導入\n❷ KL-UCB と Selfish KL-UCB\n❸ Randomized Selfish KL-UCB\n❹ 数値実験\n❺ Izumi et al. (2026) との比較\n❻ まとめ")

# ---- MP-MAB の復習（論文ゼミ_泉0421 の 3 枚目をそのまま使う）
s = d.slide("Review: Multi-Player Multi-Armed Bandits (MP-MAB)")
s.paste(R0421, 3, [2, 3, 4, 5, 6, 8, 9, 10, 11, 12] + list(range(13, 32)) + [33], retext={
    33: ("Multiple players share a single bandit, and choosing the same arm at the same time causes "
         "**“collisions”** and reward loss.", 20, "body", False, "l")})
s.notes("復習：マルチプレイヤー多腕バンディット（MP-MAB）\n"
        "\n"
        "複数のプレイヤーが 1 つのバンディットを共有し、同じ腕を同時に選ぶと **「衝突」** が起きて報酬を失う。\n"
        "\n"
        "・2010 年に Liu & Zhao がコグニティブ無線向けに提案した。\n"
        "・（集中型は Anantharam et al., 1987）\n"
        "・応用：\n"
        "  - 主に **コグニティブ無線**、特に周波数の機会的な共用（OSA）。\n"
        "  - IoT やスマート車両にも応用される。")

# ---- Setup（論文ゼミ_泉0421 の 6 枚目。記号を本論文に合わせる）
s = d.slide("Setup: Multi-Player Multi-Armed Bandits (MP-MAB)")
L24 = lambda t: (t, 24, "ink", False, "ctr")
s.paste(R0421, 6, list(range(2, 10)) + list(range(11, 35)) + list(range(36, 53)) + [54, 55, 56, 57], retext={
    40: ("**Arm reward** $X_k(t)$", 20, "ink", False, "l"),
    41: L24("$X_1(t),$"), 42: L24("$X_K(t)$"),
    57: ("i.i.d. Bernoulli\nwith mean $\\mu_k$", 16, "body", False, "ctr"),
    54: ("**Choice** $\\pi_m(t)$", 20, "ink", False, "l"),
    37: L24("$\\pi_1(t),$"), 39: L24("$\\pi_2(t),$"), 22: L24("$\\pi_M(t)$"),
    44: ("$\\pi_m(t)\\in\\{1,\\dots,K\\}$", 16, "body", False, "l"),
    26: ("**Player** $m$  $(M\\leq K)$", 20, "ink", False, "l"),
    29: ("**Reward** $r_m(t)$", 20, "ink", False, "l"),
    30: L24("$r_1(t),$"), 31: L24("$r_2(t),$"), 32: L24("$r_M(t)$"),
    50: ("$\\eta_k(t)=\\mathbb{1}\\{\\#\\{m:\\pi_m(t)=k\\}\\geq2\\}$", 18, "body", False, "ctr"),
    55: ("($=1$ if two or more players chose arm $k$)", 16, "body", False, "ctr"),
    48: ("Each player receives the reward:",),
    47: ("$r_m(t)=X_{\\pi_m(t)}(t)\\left(1-\\eta_{\\pi_m(t)}(t)\\right)$", 18, "body", False, "ctr")})
s.notes("設定：マルチプレイヤー多腕バンディット（MP-MAB）\n"
        "\n"
        "・腕 $k=1,\\dots,K$ の報酬 $X_k(t)$ は i.i.d. のベルヌーイ分布で、平均は $\\mu_k$。\n"
        "・各時刻 $t=1,\\dots,T$ に、プレイヤー $m=1,\\dots,M$（$M\\leq K$）は腕 $\\pi_m(t)\\in\\{1,\\dots,K\\}$ を 1 本選ぶ。\n"
        "・2 人以上が同じ腕 $k$ を選ぶと衝突が起きる。その指示変数を $\\eta_k(t)$ と書く（2 人以上が選んだら 1）。\n"
        "・プレイヤー $m$ が受け取る報酬は $r_m(t)=X_{\\pi_m(t)}(t)(1-\\eta_{\\pi_m(t)}(t))$。衝突すると 0 になる。\n"
        "\n"
        "【口頭補足】\n"
        "・前回の論文ゼミ（Shi et al., 2021）は腕の平均がプレイヤーごとに違う設定だったが、今回は全プレイヤーで同じ $\\mu_k$。")

# ---- Regret の定義（論文ゼミ_泉0421 の 9 枚目の書き方）
s = d.slide("Setup: Regret Definition")
s.paste(R0421, 9, [4, 5, 9, 10, 11])
s.eq(r"R_{\boldsymbol{\mu}}(T) = \sum_{t=1}^{T}\left(\sum_{m=1}^{M}\mu_{(m)} - \sum_{m=1}^{M}\mathbb{E}\left[r_m(t)\right]\right)", 3.35, size=24, h=1.25)
s.bullets(1.39, 5.08, 10.8, [
    "$\\mu_{(1)} \\geq \\cdots \\geq \\mu_{(K)}$ : expected rewards of the arms in decreasing order",
    "$\\sum_{m=1}^{M}\\mu_{(m)}$ : reward of an oracle that puts one player on each of the top $M$ arms",
    "$r_m(t)$ : reward of player $m$, which is 0 when it collides"], size=20, gap=2)
s.notes("設定：リグレットの定義\n"
        "\n"
        "目標：全プレイヤーの累積報酬の合計を最大にする（**リグレットを最小にする**）。\n"
        "\n"
        "・$T$ ラウンド後のリグレットは、上位 $M$ 本の腕に 1 人ずつ座る理想と、実際に得た報酬の期待値の差の合計。\n"
        "・$\\mu_{(1)}\\geq\\cdots\\geq\\mu_{(K)}$：腕の平均を大きい順に並べたもの。\n"
        "・$\\sum_{m=1}^{M}\\mu_{(m)}$：$\\boldsymbol{\\mu}$ を知っていて最適に動く場合（オラクル）の 1 ラウンドの報酬。\n"
        "・$r_m(t)$：プレイヤー $m$ の報酬。衝突すると 0。\n"
        "\n"
        "【口頭補足】\n"
        "・原文 1.1 節は $\\mathbb{E}[r_{\\pi_m(t)}(t)]$ と書いているが、意味は $\\mathbb{E}[r_m(t)]$。")

# ---- 衝突検知なし（修論中間発表 3 枚目の分類の木）
s = d.slide("No Collision Sensing: the Hardest Setting",
            lead="A player observes **only its own reward**, so a reward of 0 does not tell whether it collided or was just unlucky.")
s.paste(RTH, 3, list(range(5, 24)), dy=0.12, retext={
    6: ("Centralized",), 7: ("Decentralized\n(no messages)",),
    8: ("Full sensing",), 9: ("Statistic sensing",), 10: ("Collision sensing",), 11: ("No sensing",),
    18: ("sees all rewards and all collisions", 16, "body", False, "l"),
    22: ("sees $X_k(t)$ and $r_m(t)$", 16, "body", False, "l"),
    23: ("sees $\\eta_k(t)$ and $r_m(t)$", 16, "body", False, "l"),
    19: ("sees **only** $r_m(t)$", 16, "red", False, "l"),
    21: ("Difficulty", None, None, None, None, 1.4)})
s.text(11.82, 3.20, 0.85, "easy", 16, "blue", True)
s.text(11.82, 5.55, 0.85, "hard", 16, "red", True)
s.box(C.L + 0.15, 5.35, 4.3, None, "$r_m(t)=0$:  collision?  or bad luck?", fill="pale-red", line="red", lw=1.0,
      size=18, color="red", ins=(0.15, 0.06, 0.15, 0.06))
s.text(C.L + 0.15, 6.0, 4.6, "Players also do not know $M$ or their own index $m$, so all of them follow the same rule.", 16, "warm")
s.notes("衝突検知なし：最も難しい設定\n"
        "\n"
        "プレイヤーは **自分の報酬だけ** を観測するので、報酬 0 を見ても、衝突したのか運が悪かっただけなのか分からない。\n"
        "\n"
        "・（図）MP-MAB は集中型と分散型に分かれ、分散型は観測できる量で 4 つに分かれる。下に行くほど難しい。\n"
        "  - 完全検知：全アームの報酬と衝突が見える。\n"
        "  - 統計検知：$X_k(t)$ と $r_m(t)$ が見える。\n"
        "  - 衝突検知：$\\eta_k(t)$ と $r_m(t)$ が見える。\n"
        "  - **検知なし**：$r_m(t)$ だけ（本論文）。\n"
        "・（赤い箱）$r_m(t)=0$ は、衝突か、運が悪かっただけか。\n"
        "・プレイヤーは $M$ も自分の番号 $m$ も知らないので、全員が同じ規則で動く。\n"
        "\n"
        "【口頭補足】\n"
        "・報酬 1 なら衝突していないことは確実で、0 だけがあいまい、という非対称性がある。")

# ---- 既存手法と位置づけ（年表）
s = d.slide("Earlier Algorithms and Where This Paper Stands",
            lead="Earlier algorithms without collision sensing need prior knowledge, while R-SKL needs none "
                 "but has {red:no proof} for many players.")
y0 = s.top + 0.02
xs = [1.25, 3.05, 4.85, 6.65, 8.55, 10.35, 12.05]
yrs = ["2018", "2018", "2019", "2020", "2021", "2022", "2026"]
s.line(0.6, y0 + 0.55, 12.45, y0 + 0.55, "ink", 2.0)
s.shape("triangle", 12.42, y0 + 0.45, 0.2, 0.2, fill="ink", line="ink", rot=90)
names = ["Lugosi &\nMehrabian 1", "Lugosi &\nMehrabian 2", "SIC-MMAB2\n[Boursier+]", "EC-SIC\n[Shi+]",
         "{red:This paper}\n{red:R-SKL}", "Huang et al.\n(COLT)", "{blue:Izumi et al.}\n(AJCAI)"]
know = ["$M$", "$\\mu_{(M)}$", "bound on $\\mu_{(K)}$", "$\\Delta$, $\\mu_{(K)}$", "{red:none}", "none", "none"]
for i, x in enumerate(xs):
    c = "red" if i == 4 else ("blue" if i == 6 else "ink")
    s.shape("ellipse", x - 0.11, y0 + 0.44, 0.22, 0.22, fill=c, line=c)
    s.clabel(x, y0 - 0.05, yrs[i], 18, c, True, w=1.2)
    s.text(x - 0.88, y0 + 0.72, 1.76, names[i], 16, "body", align="ctr")
    s.box(x - 0.82, y0 + 1.45, 1.64, 0.44, know[i], fill="pale-red" if i == 4 else "white",
          line="red" if i == 4 else "line-gray", lw=0.75, size=16, prst="rect")
yb = y0 + 2.08
s.line(1.25 - 0.82, yb, 6.65 + 0.82, yb, "warm", 1.5)
s.line(1.25 - 0.82, yb - 0.10, 1.25 - 0.82, yb, "warm", 1.5)
s.line(6.65 + 0.82, yb - 0.10, 6.65 + 0.82, yb, "warm", 1.5)
s.text(0.43, yb + 0.03, 7.04, "required knowledge + phases. A phase can be longer than $T$.", 16, "warm", align="ctr")
s.box(C.L, y0 + 2.72, 5.95, None,
      "**R-SKL (this paper)**\nno phases, no communication\n{red:no regret bound for} $M \\geq 2$",
      fill="pale-red", line="red", lw=1.0, size=18, radius=0.08, ins=(0.1, 0.1, 0.1, 0.1))
s.box(6.71, y0 + 2.72, 5.95, None,
      "**Huang et al. / Izumi et al.**\nphases + communication through collisions\n{blue:proved regret bound}",
      fill="lead", line="ink", lw=1.0, size=18, radius=0.08, ins=(0.1, 0.1, 0.1, 0.1))
s.notes("既存手法と本論文の位置づけ\n"
        "\n"
        "衝突検知なしの既存手法は事前知識を必要とする。R-SKL は何も必要としないが、**多人数での証明がない**。\n"
        "\n"
        "・（年表と下の箱）各手法が必要とする知識：\n"
        "  - 2018 Lugosi & Mehrabian Alg. 1：$M$。Alg. 2：$\\mu_{(M)}$。\n"
        "  - 2019 SIC-MMAB2：$\\mu_{(K)}$ の下界。2020 EC-SIC：$\\Delta$ と $\\mu_{(K)}$。\n"
        "  - 2021 本論文 R-SKL、2022 Huang et al.、2026 Izumi et al.：不要。\n"
        "・（かぎかっこ）既存手法は事前知識とフェーズを使う。$\\mu_{(K)}$ が小さいとフェーズが $T$ より長くなりうる。\n"
        "・（左の箱）R-SKL：フェーズなし・通信なし。$M\\geq2$ のリグレット上界はない。\n"
        "・（右の箱）Huang et al.・Izumi et al.：フェーズと衝突による通信を使う。リグレット上界が証明されている。\n"
        "\n"
        "【口頭補足】\n"
        "・フェーズの長さの例：$(M,K)=(2,3)$、$T=2\\times10^6$ で SIC-MMAB2（$\\mu_{(K)}=0.01$）の最初の探索フェーズは $4800K\\log(T)/\\mu_{(K)}\\geq2\\times10^7>T$（原文 3.1 節）。\n"
        "・Huang et al. の第 2・第 3 著者は本論文の著者と同じ 2 人。Izumi et al. (2026) は Huang et al. を拡張した手法。")

# ---- この論文はどこまで信頼できるか
s = d.slide("How Far Can We Trust This Paper?",
            lead="The paper is an arXiv preprint without peer review or a regret proof, but its authors are established "
                 "bandit researchers and its experiments can be reproduced.")
y0 = s.top
wc = 5.95
s.text(C.L, y0, wc, "{red:Cautions}", 20, align="ctr")
s.text(6.71, y0, wc, "{green:Reasons to trust the experiments}", 20, align="ctr")
s.box(C.L, y0 + 0.50, wc, 2.95,
      "**arXiv preprint only**: one version (19 Feb. 2021), no journal or conference version.\n"
      "**No regret bound for** $M\\geq2$: every claim for many players rests on experiments.\n"
      "**Cited 3 times** (Semantic Scholar, Oct. 2026). The authors' own follow-up at COLT 2022 does not cite it.",
      fill="pale-red", line="red", lw=1.0, size=18, align="l", anchor="t", bullet="•", gap=10, radius=0.08,
      ins=(0.2, 0.18, 0.2, 0.1))
s.box(6.71, y0 + 0.50, wc, 2.95,
      "**R. Combes** (Assoc. Prof., CentraleSupélec): bandit papers at ICML 2014, NIPS 2015, NeurIPS 2017 and 2024, COLT 2022 and 2025.\n"
      "**C. Trinh**: first author at ALT 2020, with Kaufmann, Vernade and Combes.\n"
      "**Public code**: our own implementation reproduces its results (Part 5).",
      fill="pale-green", line="green", lw=1.0, size=18, align="l", anchor="t", bullet="•", gap=10, radius=0.08,
      ins=(0.2, 0.18, 0.2, 0.1))
s.notes("この論文はどこまで信頼できるか\n"
        "\n"
        "本論文は査読もリグレットの証明もない arXiv のプレプリントだが、著者はバンディットの分野で実績のある研究者で、実験は再現できる。\n"
        "\n"
        "・注意する点：\n"
        "  - **arXiv のプレプリントのみ**：1 版だけ（2021 年 2 月 19 日）。ジャーナルにも会議にも載っていない。\n"
        "  - **$M\\geq2$ のリグレット上界がない**：多人数についての主張は、すべて実験に基づく。\n"
        "  - **引用は 3 件**（Semantic Scholar、2026 年 10 月）。著者自身の続編（COLT 2022）も本論文を引用していない。\n"
        "・実験を信頼できる理由：\n"
        "  - **R. Combes**（CentraleSupélec 准教授）：ICML 2014、NIPS 2015、NeurIPS 2017・2024、COLT 2022・2025 にバンディットの論文がある。\n"
        "  - **C. Trinh**：ALT 2020 の筆頭著者（Kaufmann、Vernade、Combes と共著）。\n"
        "  - **コードが公開**されており、私の実装でも結果を再現できた（5 部）。\n"
        "\n"
        "【口頭補足】\n"
        "・Combes の代表的な論文：Unimodal Bandits（ICML 2014、引用 150 件）、Combinatorial Bandits Revisited（NIPS 2015）、Minimal Exploration in Structured Stochastic Bandits（NeurIPS 2017、引用 128 件）。OpenAlex では論文 106 本、被引用 1,422 件、h 指数 21。\n"
        "・続編は Huang, Combes, Trinh「Towards Optimal Algorithms for Multi-Player Bandits without Collision Sensing Information」（COLT 2022、引用 19 件）。証明つきの手法を提案しており、Izumi et al. (2026) はこれを拡張している。\n"
        "・引用数は Semantic Scholar の値で、Google Scholar とは数え方が違う。")

# ---- 貢献
s = d.slide("Contributions of This Paper",
            lead="The paper proposes **Randomized Selfish KL-UCB** (R-SKL), a simple algorithm that needs no prior knowledge "
                 "and beats the earlier algorithms in almost all experiments.")
y = s.top + 0.10
items = [("Algorithm:", "each player runs KL-UCB on its own data and adds a small random term. No phases, no communication."),
         ("Static experiments:", "beats EC-SIC, SIC-MMAB2 and Lugosi 2, sometimes by several orders of magnitude, and sometimes even methods with collision sensing."),
         ("Dynamic experiments:", "beats DYN-MMAB when players enter over time, and works when players enter and leave."),
         ("Theory:", "only the single-player case is proved. The multi-player regret bound is an {red:open problem}.")]
for i, (h, t) in enumerate(items):
    c = "red" if i == 3 else "ink"
    s.num(C.L + 0.05, y - 0.06, i + 1, c)
    y = s.text(C.L + 0.70, y, C.W - 0.70, "{%s:%s}  %s" % (c, h, t), 20) + 0.22
s.source("Code: github.com/ctrnh/multi_player_multi_armed_bandit_algorithms")
s.notes("本論文の貢献\n"
        "\n"
        "本論文は、事前知識を必要としない単純な手法 **Randomized Selfish KL-UCB（R-SKL）** を提案し、ほぼすべての実験で既存手法を上回ることを示す。\n"
        "\n"
        "❶ アルゴリズム：各プレイヤーが自分のデータで KL-UCB を使い、小さな乱数の項を足す。フェーズも通信もない。\n"
        "❷ 静的な環境の実験：EC-SIC、SIC-MMAB2、Lugosi 2 を上回り、桁違いのこともある。衝突検知を使う手法より良い場合もある。\n"
        "❸ 動的な環境の実験：プレイヤーが途中で入る設定で DYN-MMAB を上回り、入って出る設定でも動く。\n"
        "❹ 理論：証明されているのは 1 人の場合だけ。多人数でのリグレット上界は **未解決問題**。")
