"""本人の修正（assets/reference/スライドデザイン変更点まとめ.pptx の「変更後」）を、部品だけで組んだ作例。
fieldset()（結論の囲み）、collide() と lock()（衝突と固定の図）、points()（箱で囲まない対比の箇条書き）。
    $PY examples/fixes_20261015.py out.pptx
"""
import sys; import os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
from deck import Deck, C
d = Deck()
s = d.slide("Problem of Selfish KL-UCB", part="(1/2)",
            lead="On some runs of Selfish KL-UCB, a group of players collides without an end, and the regret grows linearly.")
y = s.heading(C.L, s.top, "Proposition 1 [Boursier & Perchet, 2019]:")
y = s.text(C.L + 0.3, y + 0.05, C.W - 0.3, "There exists $K$, $M$ and $\\boldsymbol{\\mu}\\in[0,1]^K$ such that under Selfish UCB1:")
y = s.eq(r"\liminf_{T\to\infty}\frac{R_{\boldsymbol{\mu}}(T)}{T} > 0", y + 0.05, number="(6)")
y = s.text(C.L + 0.3, y + 0.05, C.W - 0.3, "i.e. the regret grows linearly.")
y = s.heading(C.L, y + 0.15, "All-or-nothing behaviour:")
bw = (C.W - 0.22) / 2
s.fieldset(C.L, y + 0.5, bw, 0.94, "Good runs", "The players separate, and the regret stays small.", "green")
s.fieldset(C.L + bw + 0.22, y + 0.5, bw, 0.94, "Bad runs", "A subset of players collides forever: linear regret.", "red")
s.notes("t\n\nx")

s = d.slide("Collisions Make Occupied Arms Look Bad",
            lead="An arm that another player is using returns 0 to a newcomer, so to the newcomer it looks like a bad arm.")
xs = [1.35, 2.80, 4.25]
for k, x in enumerate(xs, 1):
    s.slot(x, 3.48, "m"); s.clabel(x + 0.52, 3.05, "$%d$" % k, 18)
cx, py = s.collide((xs[0], 3.48), [1.59, 3.08], size="s" if False else "m")
s.lock(1.59 - 0.6, py - 0.45)
s.clabel(1.72, py + 0.85, "P1", 16); s.clabel(3.21, py + 0.85, "P2", 16)
s.notes("t\n\nx")

s = d.slide("How Far Can We Trust This Paper?",
            lead="The paper is an arXiv preprint without peer review or a regret proof, but its authors are established bandit researchers.")
bw = (C.W - 0.22) / 2
s.points(C.L, s.top, bw, ["**arXiv preprint only**: one version (19 Feb. 2021), no journal or conference version.",
                          "**No regret bound for $M\\geq 2$**: every claim for many players rests on experiments.",
                          "**Cited 3 times** (Semantic Scholar, Oct. 2026)."], color="red", heading="Cautions")
s.points(C.L + bw + 0.22, s.top, bw, ["**R. Combes** (Assoc. Prof., CentraleSupélec): bandit papers at ICML, NeurIPS, COLT.",
                                      "**C. Trinh**: first author at ALT 2020.",
                                      "**Public code**: our own implementation reproduces its results."], color="green",
         heading="Reasons to trust the experiments")
s.notes("t\n\nx")
d.save(sys.argv[1] if len(sys.argv) > 1 else "fixes_20261015.pptx")
