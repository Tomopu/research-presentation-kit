# ================================================================= Part 6: Conclusion（扉なし）
s = d.slide("Summary",
            lead="R-SKL adds a tiny Gaussian term to Selfish KL-UCB, which breaks the symmetry and makes it beat "
                 "all earlier algorithms without collision sensing in experiments.")
y = s.top + 0.05
items = [("Algorithm:", "$\\arg\\max_k\\{b_{m,k}(t)+Z_{m,k}(t)/t\\}$. No phases, no communication, no prior knowledge.", "ink"),
         ("Theory:", "optimal for $M=1$. {red:No regret bound for} $M\\geq2$ (open problem).", "red"),
         ("Experiments in the paper:", "best in almost all static and dynamic settings. Weaker only when all means are equal.", "ink"),
         ("Comparison with Izumi et al.:", "199–583 times lower regret in five settings.", "ink"),
         ("Why:", "no fixed cost for initialization and communication.", "ink")]
for i, (h, t, c) in enumerate(items):
    s.num(C.L + 0.05, y - 0.06, i + 1, c)
    y = s.text(C.L + 0.70, y, C.W - 0.70, "{%s:%s}  %s" % (c, h, t), 20) + (0.45 if i == 0 else 0.20)
s.source("Source: Trinh & Combes (2021), arXiv:2102.10200. Our data: mpmab-simu outputs (camera_ready_2026092x).")
s.notes("まとめ\n"
        "\n"
        "R-SKL は Selfish KL-UCB に小さな正規乱数の項を足す。これで対称性が崩れ、実験では衝突検知なしの既存手法をすべて上回る。\n"
        "\n"
        "❶ アルゴリズム：$\\arg\\max_k\\{b_{m,k}(t)+Z_{m,k}(t)/t\\}$。フェーズ・通信・事前知識なし。\n"
        "❷ 理論：$M=1$ で最適。$M\\geq2$ のリグレット上界はない（**未解決問題**）。\n"
        "❸ 原論文の実験：静的・動的のほぼすべてで最良。平均がすべて等しい場合だけ不利。\n"
        "❹ Izumi et al. との比較：5 設定で 199〜583 分の 1 のリグレット。\n"
        "❺ 理由：初期化と通信の固定費がない。")

s = d.slide("Open Problem and Next Step",
            lead="The analysis of R-SKL is left as an open problem, and closing the gap between proved methods and R-SKL "
                 "is the next target.")
y = s.quote(C.L, s.top, C.W, "\"We hope this work will encourage the community toward the analysis of this algorithm, "
            "a challenging but promising open problem.\"", source="[Trinh & Combes, 2021, Section 7]", size=18)
y = s.quote(C.L, y + 0.12, C.W, "\"Randomized Selfish KL-UCB reached a much lower regret in our experiments, and closing this gap "
            "with a proved bound is left for future work.\"", source="[Izumi & Nakamura, AJCAI 2026, Conclusion]", size=18)
y = s.heading(C.L, y + 0.12, "Possible directions:")
y = s.bullets(C.L, y, C.W, ["Reduce the fixed cost of coordinated methods further.",
                            "Try to analyze R-SKL, starting from simple cases such as $M=2$.",
                            "Combine a proved method with a selfish phase."], size=18, gap=2)
s.notes("未解決問題と今後\n"
        "\n"
        "R-SKL の解析は未解決問題として残されており、証明つきの手法と R-SKL の差を縮めることが次の課題である。\n"
        "\n"
        "・引用（原論文 7 節）の訳：「本研究が、このアルゴリズムの解析――難しいが有望な未解決問題――へと研究者を促すことを願う。」\n"
        "・引用（AJCAI 論文の結論）の訳：「Randomized Selfish KL-UCB は実験ではるかに低いリグレットを達成した。この差を証明つきの上界で縮めることは今後の課題である。」\n"
        "・方向の案：\n"
        "  - 協調型の固定費をさらに削減する。\n"
        "  - $M=2$ などの単純な場合から R-SKL の解析を試みる。\n"
        "  - 証明つきの手法と selfish な段階を組み合わせる。\n"
        "\n"
        "【口頭補足】\n"
        "・議論のための問い：R-SKL が永遠に衝突し続ける確率は 0 か？ Selfish UCB1 には線形リグレットの例があり、R-SKL ではまだ分かっていない。")

s = d.slide("References")
s.bullets(C.L, s.top, C.W, [
    "C. Trinh and R. Combes. A high performance, low complexity algorithm for multi-player bandits without collision sensing information. arXiv:2102.10200, 2021.",
    "W. Huang, R. Combes, and C. Trinh. Towards optimal algorithms for multi-player bandits without collision sensing information. COLT, 2022.",
    "T. Izumi and A. Nakamura. Multi-channel communication algorithm for multi-player multi-armed bandits without collision sensing. AJCAI, 2026.",
    "L. Besson and E. Kaufmann. Multi-player bandits revisited. ALT, 2018.",
    "E. Boursier and V. Perchet. SIC-MMAB: Synchronisation involves communication in multiplayer multi-armed bandits. NeurIPS, 2019.",
    "G. Lugosi and A. Mehrabian. Multiplayer bandits without observing collision information. arXiv:1808.08416, 2018.",
    "C. Shi, W. Xiong, C. Shen, and J. Yang. Decentralized multi-player multi-armed bandits with no collision information. AISTATS, 2020.",
    "O. Cappé, A. Garivier, O.-A. Maillard, R. Munos, and G. Stoltz. Kullback–Leibler upper confidence bounds for optimal sequential allocation. Annals of Statistics, 2013."],
    size=18, gap=8)
s.notes("参考文献")

d.save(OUT)
print("saved", OUT, len(d.slides), "slides")
