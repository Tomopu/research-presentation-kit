# ================================================================= Part 2: KL-UCB and Selfish KL-UCB
s = d.divider("KL-UCB and Selfish KL-UCB")
s.notes("KL-UCB と Selfish KL-UCB")

# ---- 各プレイヤーが記録するもの（N と μ̂ の説明だけ）
s = d.slide("What Each Player Records",
            lead="Each player records, for every arm, the number of pulls and the average reward it got, "
                 "where a reward of 0 from a collision is counted as it is.")
y = s.heading(C.L, s.top, "Number of pulls:")
y = s.eq(r"N_{m,k}(t) = \sum_{s=1}^{t-1}\mathbb{1}\{\pi_m(s)=k\}", y - 0.05, size=22, number="(2)")
y = s.text(C.L + 0.3, y - 0.02, C.W - 0.3, "How many times player $m$ chose arm $k$ before time $t$.", 18, "warm")
y = s.heading(C.L, y + 0.18, "Empirical mean reward:")
y = s.eq(r"\hat{\mu}_{m,k}(t) = \frac{1}{\max(N_{m,k}(t),1)}\sum_{s=1}^{t-1} r_m(s)\,\mathbb{1}\{\pi_m(s)=k\}", y - 0.05, size=22, number="(3)")
y = s.text(C.L + 0.3, y - 0.02, C.W - 0.3, "The average of the rewards that player $m$ got from arm $k$.", 18, "warm")
s.notes("各プレイヤーが記録するもの\n"
        "\n"
        "各プレイヤーは腕ごとに、引いた回数と得た報酬の平均を記録する。衝突による報酬 0 も、そのまま数に入る。\n"
        "\n"
        "・式 (2)：$N_{m,k}(t)$ は、プレイヤー $m$ が時刻 $t$ より前に腕 $k$ を選んだ回数。\n"
        "・式 (3)：$\\hat{\\mu}_{m,k}(t)$ は、プレイヤー $m$ が腕 $k$ から得た報酬の平均（$N=0$ のときは分母を 1 にする）。\n"
        "\n"
        "【口頭補足】\n"
        "・どちらもプレイヤー $m$ が自分で観測できる量だけで計算できる（原文 2.1 節）。\n"
        "・$r_m(s)$ は衝突すると 0 なので、$\\hat{\\mu}_{m,k}$ は腕の真の平均 $\\mu_k$ ではなく「実際にもらえた平均」になる。これが後で効く。")

# ---- KL-UCB 指数
s = d.slide("The KL-UCB Index",
            lead="The KL-UCB index is the **largest mean still consistent** with what the player has seen, "
                 "so an arm pulled only a few times gets a high, optimistic index.")
y = s.eq(r"d(\mu,\lambda) = \mu\log\frac{\mu}{\lambda} + (1-\mu)\log\frac{1-\mu}{1-\lambda}", s.top - 0.10, size=20, number="(4)")
y = s.eq(r"b_{m,k}(t) = \max\left\{ q \in [0,1] : N_{m,k}(t)\, d\left(\hat{\mu}_{m,k}(t), q\right) \leq f(t) \right\},\quad f(t) = \log t", y - 0.02, size=20, number="(5)")
f1000 = math.log(1000)
b10, b100, b1000 = klucb(0.6, 10, f1000), klucb(0.6, 100, f1000), klucb(0.6, 1000, f1000)
yc = y + 0.02
s.xy_chart(C.L, yc, 7.7, BOTTOM - yc, [
    ("d(0.6, q)", qs, [dkl(0.6, q) for q in qs], "ink", 2.5),
    ("N = 10", [0.6, 1.0], [f1000 / 10] * 2, "red", 1.75, True),
    ("N = 100", [0.6, 1.0], [f1000 / 100] * 2, "blue", 1.75, True),
    ("N = 1000", [0.6, 1.0], [f1000 / 1000] * 2, "green", 1.75, True)],
    x_title="q   (example: μ̂ = 0.6, t = 1000; dashed lines: f(t)/N)", y_title="d(0.6, q)", x_range=(0.6, 1.0), y_range=(0, 1.0),
    size=14, legend=True, legend_pos="t", x_fmt="0.00", y_fmt="0.0")
xb = 8.5
yy = s.heading(xb, yc + 0.05, "Example:", w=C.R - xb)
yy = s.text(xb, yy, C.R - xb, "The index is the $q$ where the curve meets the dashed line.", 18)
yy = s.bullets(xb, yy + 0.08, C.R - xb, [
    "{red-n:N = 10}:  $b = %.3f$" % b10,
    "{blue-n:N = 100}:  $b = %.3f$" % b100,
    "{green-n:N = 1000}:  $b = %.3f$" % b1000], size=18, gap=4)
s.text(xb, yy + 0.12, C.R - xb, "Fewer pulls → higher index.", 18, bold=True)
s.notes("KL-UCB 指数\n"
        "\n"
        "KL-UCB 指数は、これまでの観測と **矛盾しない範囲で最も大きい平均** なので、少ししか引いていない腕ほど指数は楽観的に高くなる。\n"
        "\n"
        "・式 (4)：ベルヌーイ分布の KL ダイバージェンス $d(\\mu,\\lambda)$。$\\mu=\\lambda$ で 0、離れるほど大きい。\n"
        "・式 (5)：指数 $b_{m,k}(t)$ の定義（原文 2.2 節）。\n"
        "・（グラフ）$\\hat{\\mu}=0.6$、$t=1000$ の例。曲線 $d(0.6,q)$ と高さ $f(t)/N$ の破線が交わる $q$ が指数。\n"
        "  - $N=10$ なら $b=0.965$、$N=100$ なら $b=0.767$、$N=1000$ なら $b=0.656$。\n"
        "・引いた回数が少ないほど、指数は高い。\n"
        "\n"
        "【口頭補足】\n"
        "・原文は $f(t)=\\log t+c\\log\\log t$（$c\\geq0$）と書き、本文の実験は $c=0$、著者の公開コードは $c=3$。\n"
        "・一度も選んでいない腕（$N=0$）の指数は 1。\n"
        "・1 人用の KL-UCB は $\\arg\\max_k b_k(t)$ を選び、1 人なら漸近最適 [Cappé et al., 2013]。")

# ---- Selfish KL-UCB
s = d.slide("Selfish KL-UCB [Besson & Kaufmann, 2018]",
            lead="Every player runs KL-UCB on its own data and ignores the other players.")
y0 = s.top + 0.30
person(s, C.L + 0.35, y0 - 0.05, "m")
s.text(C.L - 0.2, y0 - 0.38, 1.1, "player $m$", 16, "warm", align="ctr")
bx = [(1.55, 2.6, "own data", "$N_{m,k},\\ \\hat{\\mu}_{m,k}$", "lead", "ink"),
      (4.75, 2.6, "index (5)", "$b_{m,k}(t)$ for every arm $k$", "lead", "ink"),
      (7.95, 2.6, "choice", "arm with the largest index", "yellow", "amber")]
for i, (x, w, cap, t, f, ln) in enumerate(bx):
    s.text(x, y0 - 0.38, w, cap, 16, "warm", align="ctr")
    s.box(x, y0, w, 0.72, t, fill=f, line=ln, lw=0.75, size=18)
    if i < 2:
        s.arrow(x + w + 0.05, y0 + 0.36, bx[i + 1][0] - 0.05, y0 + 0.36, lw=1.5)
s.text(10.75, y0 - 0.05, C.R - 10.75, "no messages\nno phases", 18, "red", True, align="ctr")
yb = y0 + 0.95
avail = BOTTOM - yb
s.code(C.L, yb, C.W, [
    "**Algorithm 1**   Selfish KL-UCB  (for player $m=1,\\dots,M$)",
    "{red-n:for} $t=1,\\dots,T$ {red-n:do}",
    "  {red-n:for} $k=1,\\dots,K$ {red-n:do}",
    "    Compute  $b_{m,k}(t)=\\max\\{q\\in[0,1]: N_{m,k}(t)\\,d(\\hat{\\mu}_{m,k}(t),q)\\leq f(t)\\}$",
    "  {red-n:end for}",
    "  Draw arm  $\\pi_m(t)=\\arg\\max_{k=1,\\dots,K}\\{b_{m,k}(t)\\}$",
    "  Observe reward $r_m(t)$ and update statistics",
    "{red-n:end for}"], size=18 if avail >= 3.05 else 16, hl={5: "pale-blue"})
s.notes("Selfish KL-UCB [Besson & Kaufmann, 2018]\n"
        "\n"
        "各プレイヤーが自分のデータで KL-UCB を動かし、他のプレイヤーを無視する。\n"
        "\n"
        "・（上の図）プレイヤー $m$ は、自分の統計量 $N_{m,k}$, $\\hat{\\mu}_{m,k}$ → 全腕の指数 $b_{m,k}(t)$ → 指数が最大の腕、の順に決める。メッセージもフェーズもない。\n"
        "・（下）原文 Algorithm 1：各時刻に全腕の指数を計算し、$\\arg\\max$ の腕を引き、報酬を観測して統計量を更新する。\n"
        "\n"
        "【口頭補足】\n"
        "・Selfish は「他のプレイヤーが存在しないかのように、1 人の場合の最適を目指す」という意味（原文 2.2 節）。")

# ---- 衝突で使用中の腕は悪く見える
s = d.slide("Collisions Make Occupied Arms Look Bad",
            lead="An arm that another player is using returns 0 to a newcomer, so to the newcomer it looks like a bad arm "
                 "and the players separate without any message.")
y0 = s.top + 0.05
figlabel(s, C.L, y0 - 0.05, 5.4, "P2 tries the arm of P1: both get $r=0$")
cx = arms(s, 1.35, y0 + 1.05, 3, 1.45, size="m")
p1, p2 = cx[0] - 0.28, cx[0] + 0.28
person(s, p1, y0 + 2.35, "m")
person(s, p2, y0 + 2.35, "m")
s.arrow(p1, y0 + 2.30, cx[0] - 0.10, y0 + 1.68)
s.arrow(p2, y0 + 2.30, cx[0] + 0.10, y0 + 1.68)
s.collision(cx[0], y0 + 1.33)
s.lock(cx[0] + 0.42, y0 + 0.85, 0.30)
s.clabel(p1 - 0.30, y0 + 3.2, "P1", 16, "warm", w=0.7)
s.clabel(p2 + 0.30, y0 + 3.2, "P2", 16, "warm", w=0.7)
s.text(C.L, y0 + 3.55, 5.4, "true means: $\\boldsymbol{\\mu}=(0.9,\\ 0.6,\\ 0.3)$", 16, "warm", align="ctr")
xb = 6.35
figlabel(s, xb, y0 - 0.05, C.R - xb, "What P2 believes after $10^4$ steps")
s.bar_chart(xb, y0 + 0.40, C.R - xb, 3.15, ["arm 1  (used by P1)", "arm 2", "arm 3"],
            [("true mean", [0.9, 0.6, 0.3], "gray"), ("P2's estimate", [0.071, 0.607, 0.233], "red")],
            horizontal=False, size=14, legend=True, value_range=(0, 1.0), labels=True, fmt="0.00", gap=80)
s.text(xb, y0 + 3.55, C.R - xb, "The best arm looks like the worst arm to P2.", 18, "red", True, align="ctr")
s.notes("衝突によって、使用中の腕は悪く見える\n"
        "\n"
        "他人が使っている腕は、後から来た人には報酬 0 を返す。そのため後から来た人にはその腕が悪い腕に見え、プレイヤーはメッセージなしで分かれる。\n"
        "\n"
        "・（左の図）P1 が arm 1 に座っている。P2 が arm 1 を試すと衝突し、2 人とも $r=0$。\n"
        "・（右のグラフ）$10^4$ ステップ後に P2 が信じている平均。灰色が真の平均、赤が P2 の推定値。\n"
        "  - arm 1（P1 が使用中）：真の平均 0.9 に対して、P2 の推定値は 0.07。\n"
        "  - arm 2 と arm 3 は、真の平均に近い（0.61 と 0.23）。\n"
        "・P2 には最良の腕が最悪の腕に見えるので、P2 は arm 2 に留まる。\n"
        "\n"
        "【口頭補足】\n"
        "・グラフは Selfish KL-UCB を 1 回走らせた実測値（$M=2$、$K=3$、$\\boldsymbol{\\mu}=(0.9,0.6,0.3)$、$T=10^4$、toy_selfish.py の seed 1）。P2 は arm 1 を 14 回しか試しておらず、そのほとんどが衝突だった。\n"
        "・原文 2.4 節：他のプレイヤーが固定の腕に留まるなら、その腕の平均を 0 に置き換えた 1 人用の問題になる。")

# ---- 問題点 (1/2)：線形リグレット
s = d.slide("Problem of Selfish KL-UCB", part="(1/2)",
            lead="On some runs of Selfish KL-UCB, a group of players collides without an end, and the regret grows linearly.")
y = s.heading(C.L, s.top, "Proposition 1 [Boursier & Perchet, 2019]:")
y = s.text(C.L + 0.3, y, C.W - 0.3, "There exists $K$, $M$ and $\\boldsymbol{\\mu}\\in[0,1]^K$ such that under Selfish UCB1:", 20)
y = s.eq(r"\liminf_{T\to\infty}\frac{R_{\boldsymbol{\mu}}(T)}{T} > 0", y, size=24, number="(6)")
y = s.text(C.L + 0.3, y - 0.05, C.W - 0.3, "i.e. the regret grows linearly.", 20)
y = s.heading(C.L, y + 0.08, "All-or-nothing behaviour:")
wb = 5.95
s.box(C.L, y, wb, None, "{green:Good runs}\nThe players separate, and the regret stays small.",
      fill="pale-green", line="green", lw=1.0, size=18, radius=0.08, ins=(0.15, 0.06, 0.15, 0.06))
s.box(6.71, y, wb, None, "{red:Bad runs}\nA subset of players collides forever: linear regret.",
      fill="pale-red", line="red", lw=1.0, size=18, radius=0.08, ins=(0.15, 0.06, 0.15, 0.06))
s.notes("Selfish KL-UCB の問題点（1/2）\n"
        "\n"
        "Selfish KL-UCB では、一部の試行で何人かのプレイヤーが終わりなく衝突し続け、リグレットが線形に増える。\n"
        "\n"
        "・命題 1 [Boursier & Perchet, 2019]：ある $K$、$M$、$\\boldsymbol{\\mu}$ について、Selfish UCB1 のもとで $\\liminf_{T\\to\\infty}R_{\\boldsymbol{\\mu}}(T)/T>0$、つまりリグレットが線形に増える。\n"
        "・「うまくいくか、全くだめか」の振る舞い（原文 2.2 節）：\n"
        "  - 良い試行：プレイヤーが分かれ、リグレットは小さいまま。\n"
        "  - 悪い試行：一部のプレイヤーが永遠に衝突し、線形リグレットになる。\n"
        "\n"
        "【口頭補足】\n"
        "・命題 1 の証明は UCB1 の指数を使う Selfish UCB1 についてのもの。原文の脚注は「実験では Selfish UCB1 も Selfish KL-UCB も同じ問題を示す」と述べている。")

# ---- 問題点 (2/2)：対称性
s = d.slide("Problem of Selfish KL-UCB", part="(2/2)",
            lead="The cause is symmetry: two players with the same observations choose the same arm, collide, "
                 "and so keep the same observations.")
y = s.text(C.L, s.top, C.W, "Consider two players $m \\neq m'$ who have the same observations at time $t$:", 20)
y = s.eq(r"N_{m,k}(t) = N_{m',k}(t) \quad\text{and}\quad \hat{\mu}_{m,k}(t) = \hat{\mu}_{m',k}(t) \quad\text{for all } k = 1,\dots,K", y + 0.02, size=22)
y += 0.05
xw = 7.6
steps = [("Same index:", "$b_{m,k}(t) = b_{m',k}(t)$ for all $k$.", "ink"),
         ("Same arm:", "$\\pi_m(t) = \\pi_{m'}(t)$, so they collide and both get $r=0$.", "ink"),
         ("Same observations at $t+1$:", "\"this cascade of collisions might go on forever\" (Section 2.3).", "red")]
for i, (h, t, c) in enumerate(steps):
    s.num(C.L + 0.05, y - 0.06, i + 1, c)
    s.text(C.L + 0.70, y, xw - 0.70, "{%s:%s}  %s" % (c, h, t), 20)
    hh = 0.55 if i < 2 else 0.95
    if i < 2:
        s.shape("triangle", C.L + 0.29, y + hh + 0.06, 0.14, 0.12, fill="ink", line="ink", flipV=True)
    y = y + hh + 0.28
# 右の小さな図：同じ手帳の 2 人が同じ腕へ
fx = 9.2
cxs = arms(s, fx, s.top + 1.85, 2, 1.55, size="m")
pa, pb = cxs[0] - 0.28, cxs[0] + 0.28
person(s, pa, s.top + 3.05, "m")
person(s, pb, s.top + 3.05, "m")
s.arrow(pa, s.top + 3.00, cxs[0] - 0.10, s.top + 2.47)
s.arrow(pb, s.top + 3.00, cxs[0] + 0.10, s.top + 2.47)
s.collision(cxs[0], s.top + 2.13)
s.clabel(pa - 0.45, s.top + 3.25, "$m$", 18, "warm", w=0.7)
s.clabel(pb + 0.48, s.top + 3.25, "$m'$", 18, "warm", w=0.7)
s.notes("Selfish KL-UCB の問題点（2/2）\n"
        "\n"
        "原因は対称性である。同じ観測を持つ 2 人は同じ腕を選んで衝突し、その結果、観測は同じままになる。\n"
        "\n"
        "・時刻 $t$ に同じ観測を持つ 2 人 $m\\neq m'$ を考える：すべての $k$ で $N_{m,k}(t)=N_{m',k}(t)$ かつ $\\hat{\\mu}_{m,k}(t)=\\hat{\\mu}_{m',k}(t)$。\n"
        "❶ 指数が同じ：すべての $k$ で $b_{m,k}(t)=b_{m',k}(t)$（指数は $N$、$\\hat{\\mu}$、$t$ だけで決まるため）。\n"
        "❷ 選ぶ腕が同じ：$\\pi_m(t)=\\pi_{m'}(t)$ なので衝突し、2 人とも $r=0$。\n"
        "❸ 時刻 $t+1$ でも観測が同じ：「この衝突の連鎖は永遠に続くかもしれない」（2.3 節）。\n"
        "\n"
        "【口頭補足】\n"
        "・$t=1$ では全員が $N=0$ なので、最初から全員が対称である。実装では指数が同点のときに腕を乱数で選ぶので必ず詰まるわけではないが、一度そろうと抜け出せない。\n"
        "・私の小さな例（$M=2$、$K=3$、同点は乱数で選ぶ）では、100 試行のうち 1 試行が詰まった。腕とプレイヤーが少ないほど詰まりやすい（原文 2.3 節。$M=K=2$ の図 1 では 500 試行中約 200 試行）。")

# ================================================================= Part 3: Randomized Selfish KL-UCB
s = d.divider("Randomized Selfish KL-UCB")
s.notes("Randomized Selfish KL-UCB")

# ---- R-SKL
s = d.slide("Randomized Selfish KL-UCB (R-SKL)",
            lead="R-SKL adds a small Gaussian term $Z_{m,k}(t)/t$, drawn by each player itself, to every KL-UCB index.")
yb = s.top
yc = s.code(C.L, yb, C.W, [
    "**Algorithm 2**   Randomized Selfish KL-UCB  (for player $m=1,\\dots,M$)",
    "{red-n:for} $t=1,\\dots,T$ {red-n:do}",
    "  {red-n:for} $k=1,\\dots,K$ {red-n:do}",
    "    Compute  $b_{m,k}(t)=\\max\\{q\\in[0,1]: N_{m,k}(t)\\,d(\\hat{\\mu}_{m,k}(t),q)\\leq f(t)\\}$",
    "    Draw  $Z_{m,k}(t)\\sim \\mathcal{N}(0,1)$",
    "  {red-n:end for}",
    "  Draw arm  $\\pi_m(t)=\\arg\\max_{k=1,\\dots,K}\\{b_{m,k}(t)+Z_{m,k}(t)/t\\}$",
    "  Observe reward $r_m(t)$ and update statistics",
    "{red-n:end for}"], size=18, hl={4: "yellow", 6: "yellow"})
s.text(C.L, yc + 0.12, C.W, "{u:Yellow}: the only changes from Selfish KL-UCB.  $Z_{m,k}(t)$ is i.i.d. and known only to player $m$.", 18)
s.notes("Randomized Selfish KL-UCB（R-SKL）\n"
        "\n"
        "R-SKL は、各プレイヤーが自分で引く小さな正規乱数の項 $Z_{m,k}(t)/t$ を、すべての KL-UCB 指数に足す。\n"
        "\n"
        "・（原文 Algorithm 2）Selfish KL-UCB からの変更は黄色の 2 行だけ：\n"
        "  - 腕ごとに $Z_{m,k}(t)\\sim\\mathcal{N}(0,1)$ を引く。\n"
        "  - 選ぶ腕を $\\arg\\max_k\\{b_{m,k}(t)+Z_{m,k}(t)/t\\}$ にする。\n"
        "・$Z_{m,k}(t)$ はプレイヤー・腕・時刻ごとに独立で、プレイヤー $m$ 本人しか知らない。\n"
        "\n"
        "【口頭補足】\n"
        "・乱数が入るのは腕を選ぶためのスコアだけで、$N$、$\\hat{\\mu}$、$f(t)$ は変えない。衝突時の報酬 0 も特別扱いしない。")

# ---- 乱数が対称性を崩す
s = d.slide("How the Noise Breaks the Symmetry",
            lead="Two players with the same observations still draw different noise, so they choose different arms "
                 "with positive probability and the collisions eventually stop.")
y0 = s.top + 0.05
half = 5.95
for j, (title, col_, ok) in enumerate([("Selfish KL-UCB", "red", False), ("Randomized Selfish KL-UCB", "green", True)]):
    x0 = C.L + j * (half + 0.22)
    figlabel(s, x0, y0 - 0.05, half, title)
    cxs = arms(s, x0 + 1.25, y0 + 0.92, 3, 1.35, size="m", labels=False)
    for k, c in enumerate(cxs):
        s.clabel(c, y0 + 0.45, "$b_%d$" % (k + 1), 18, w=1.0)
    if ok:
        pa, pb = cxs[0], cxs[1]
        s.arrow(pa, y0 + 2.12, cxs[0], y0 + 1.55)
        s.arrow(pb, y0 + 2.12, cxs[1], y0 + 1.55)
    else:
        pa, pb = cxs[0] - 0.28, cxs[0] + 0.28
        s.arrow(pa, y0 + 2.12, cxs[0] - 0.10, y0 + 1.55)
        s.arrow(pb, y0 + 2.12, cxs[0] + 0.10, y0 + 1.55)
        s.collision(cxs[0], y0 + 1.20)
    person(s, pa, y0 + 2.17, "m")
    person(s, pb, y0 + 2.17, "m")
    s.clabel(pa - (0.30 if not ok else 0), y0 + 2.98, "$m$", 18, "warm", w=0.6)
    s.clabel(pb + (0.30 if not ok else 0), y0 + 2.98, "$m'$", 18, "warm", w=0.6)
    if ok:
        s.text(x0 + 0.05, y0 + 2.30, 1.7, "$+\\,Z_{m,k}(t)/t$", 16, "blue", align="ctr")
        s.text(cxs[1] + 0.30, y0 + 2.30, 1.9, "$+\\,Z_{m',k}(t)/t$", 16, "blue", align="ctr")
    s.box(x0, y0 + 3.42, half, None,
          "{green:different arms with positive probability}" if ok
          else "{red:same arm with probability 1}",
          fill="pale-green" if ok else "pale-red", line=col_, lw=1.0, size=18, ins=(0.1, 0.1, 0.1, 0.1))
s.line(C.L + half + 0.11, y0 + 0.4, C.L + half + 0.11, y0 + 3.3, "line-gray", 1.0)
s.notes("乱数が対称性を崩す仕組み\n"
        "\n"
        "同じ観測を持つ 2 人でも、引く乱数は違う。そのため正の確率で別々の腕を選び、衝突はいずれ止まる。\n"
        "\n"
        "・（左）Selfish KL-UCB：指数 $b_1,b_2,b_3$ が 2 人で同じなので、確率 1 で同じ腕を選び、衝突する。\n"
        "・（右）R-SKL：指数は同じでも、$m$ は $Z_{m,k}(t)/t$、$m'$ は $Z_{m',k}(t)/t$ を足すので、正の確率で別の腕を選ぶ。一度別の腕を選べば、2 人の観測は違うものになる。\n"
        "\n"
        "【口頭補足】\n"
        "・原文 2.3 節の説明：「同じ観測を持つ 2 人は、Selfish KL-UCB では確率 1 で同じ腕を選び、無限に続きうる衝突の連鎖を起こす。Randomized Selfish KL-UCB では、別の腕を選ぶ確率が正であり、衝突はいずれ止まる。」\n"
        "・私の小さな例（$M=2$、$K=3$）では、$t=1$ は 2 人とも arm 1 で衝突し、$t=2$ に指数が同じ $(0.5,1,1)$ のまま乱数で arm 2 と arm 1 に分かれた。")

# ---- なぜ 1/t か
s = d.slide("Why the Noise Is Divided by $t$",
            lead="Dividing by $t$ makes the noise strong at the start, when ties must be broken, and negligible later, "
                 "so KL-UCB stays optimal for one player.")
y = s.heading(C.L, s.top - 0.05, "Proposition 2 (single player, $M=1$):  for any arm $k$ with $\\mu_k<\\mu_{(1)}$,", w=C.W)
y = s.eq(r"\limsup_{T\to\infty}\frac{\mathbb{E}[N_k(T)]}{\log T} \leq \frac{1}{d(\mu_k,\mu_{(1)})}", y - 0.08, size=20, number="(8)")
y = s.heading(C.L, y + 0.02, "Size of the noise $Z/t$ against two indices that differ by $0.03$:", w=C.W)
ax0, ax1 = 3.0, 9.0          # スコア 0.3〜1.3 を 6in に描く
sc = lambda v: ax0 + (v - 0.3) * (ax1 - ax0)
ia, ib = 0.78, 0.81
rows = [("$t=2$", 0.5, "noise ≈ ±0.5: the order of the arms changes often"),
        ("$t=100$", 0.01, "noise ≈ ±0.01: the order changes only for close indices"),
        ("$t=10^4$", 0.0001, "noise ≈ ±0.0001: the order follows the indices")]
for i, (lab, sd, msg) in enumerate(rows):
    yy = y + 0.10 + i * 0.74
    s.text(C.L, yy + 0.08, 2.2, "**%s**" % lab, 20)
    s.line(ax0, yy + 0.32, ax1, yy + 0.32, "line-gray", 1.0)
    wband = max(2 * sd * (ax1 - ax0), 0.03)
    s.box(max(sc(ia) - wband / 2, ax0), yy + 0.10, min(wband, ax1 - ax0), 0.20, fill="pale-blue", line="blue", lw=0.75, prst="rect")
    s.box(max(sc(ib) - wband / 2, ax0), yy + 0.34, min(wband, ax1 - ax0), 0.20, fill="pale-red", line="red", lw=0.75, prst="rect")
    s.line(sc(ia), yy + 0.04, sc(ia), yy + 0.60, "blue", 2.25)
    s.line(sc(ib), yy + 0.04, sc(ib), yy + 0.60, "red", 2.25)
    s.text(ax1 + 0.15, yy + 0.02, C.R - ax1 - 0.15, msg, 16, h=0.6, anchor="ctr")
s.text(ax0, y + 0.10 + 3 * 0.74 - 0.05, ax1 - ax0, "score  (blue: index $0.78$,  red: index $0.81$,  bands: index ± noise)", 14, "warm", align="ctr")
s.notes("なぜ乱数を $t$ で割るのか\n"
        "\n"
        "$t$ で割ると、乱数は同点を崩す必要がある最初のうちは強く、後ではほぼ無視できる。そのため 1 人の場合の KL-UCB の最適性が保たれる。\n"
        "\n"
        "・命題 2（$M=1$）：$\\mu_k<\\mu_{(1)}$ となる任意の腕 $k$ について式 (8) が成り立つ。つまり R-SKL は 1 人の場合に漸近最適である。\n"
        "・（図）指数が 0.03 だけ違う 2 本の腕（青 0.78、赤 0.81）に対する乱数 $Z/t$ の大きさ。帯は「指数 ± 乱数の大きさ」。\n"
        "  - $t=2$：乱数は約 ±0.5。腕の順位は頻繁に入れ替わる。\n"
        "  - $t=100$：約 ±0.01。指数が近いときだけ入れ替わる。\n"
        "  - $t=10^4$：約 ±0.0001。順位は指数どおりになる。\n"
        "\n"
        "【口頭補足】\n"
        "・原文 2.4 節：乱数の項の大きさ $1/t$ は「少なくとも 1 人の場合には漸近最適性を壊さないほど小さい」。\n"
        "・系：他のプレイヤーが全員固定の腕に留まるなら、その腕は平均 0 に見えるだけなので、残る 1 人は最適に学習できる。\n"
        "・証明の骨子（原文 6 節）：乱数の差が $t\\delta$ 以上になる確率は $e^{-t^2\\delta^2/2}$ 程度で、その和は有限。だから乱数は $\\log T$ の項に効かない。")

# ---- 図 1（原論文の比較のグラフと説明）
s = d.slide("Evidence: Randomization Removes the Trap",
            lead="In the experiment of the paper, Selfish KL-UCB gets stuck in almost 200 of 500 runs, while R-SKL never does.")
y0 = s.top
hi = 2.6
figlabel(s, C.L, y0 - 0.05, hi * 1.5, "Total regret of 500 runs")
figlabel(s, C.L + hi * 1.5 + 0.2, y0 - 0.05, hi * 864 / 504, "Cumulative regret")
s.image(F("22_rndnorndhist.png"), C.L, y0 + 0.40, h=hi)
s.image(F("22_rndnorndcumregret.png"), C.L + hi * 1.5 + 0.2, y0 + 0.40, h=hi)
s.callout(1.45, y0 + 1.55, 1.75, 0.62, "stuck runs\n(regret ≈ $10^4$)", (3.93, y0 + 2.55), size=14, line="red", color="red")
s.text(C.L, y0 + 0.40 + hi + 0.05, 8.6, "**Figure 1:** $M=2$, $K=2$, $\\boldsymbol{\\mu}=(0.9,0.1)$, $T=10{,}000$. Shaded areas: 90-th percentile.", 14, "warm")
xb = 9.3
yy = s.heading(xb, y0, "What the paper says:", w=C.R - xb)
s.bullets(xb, yy, C.R - xb, [
    "Selfish KL-UCB incurs a {red:linear regret for almost 200 runs}.",
    "R-SKL has {green:only one mode}: its regret did not exceed $10^3$ in any run.",
    "The endless collisions occur especially often when the numbers of players and arms are small."], size=18, gap=10)
s.notes("証拠：乱数は罠を取り除く\n"
        "\n"
        "原論文の実験では、Selfish KL-UCB は 500 回中約 200 回で詰まるが、R-SKL は一度も詰まらない。\n"
        "\n"
        "・図 1：$M=2$、$K=2$、$\\boldsymbol{\\mu}=(0.9,0.1)$、$T=10{,}000$。左は 500 回の総累積リグレットのヒストグラム、右は累積リグレットの推移（陰影は 90 パーセンタイル）。\n"
        "・原論文の説明（2.3 節）：\n"
        "  - Selfish KL-UCB は約 200 回で線形リグレットになる（ヒストグラムの $10^4$ 付近の山）。\n"
        "  - R-SKL の山は 1 つだけで、どの試行でもリグレットは $10^3$ を超えなかった。\n"
        "  - 無限に続く衝突は、プレイヤー数と腕の数が少ないときに特に起きやすい。\n"
        "\n"
        "【口頭補足】\n"
        "・この例は $K=M$ で、本論文や Izumi et al. の主な設定 $M<K$ の外にある。\n"
        "・私の再実験（AJCAI 論文の補足資料 H.4）でも、Selfish KL-UCB は 300 回中 77 回で分離しなかった。")

# ---- 証明されていること・いないこと
s = d.slide("What Is Proved and What Is Not",
            lead="Optimality is proved only for one player, and for two or more players the authors could not prove "
                 "any regret bound.")
y0 = s.top
wb = 5.95
s.text(C.L, y0, wb, "{green:Proved}", 20, align="ctr")
s.text(6.71, y0, wb, "{red:Not proved}", 20, align="ctr")
s.box(C.L, y0 + 0.50, wb, 1.50,
      "$M=1$: R-SKL is asymptotically optimal (Proposition 2).\n"
      "It stays optimal for one player when all the others stay on fixed arms.",
      fill="pale-green", line="green", lw=1.0, size=18, align="l", anchor="t", bullet="•", gap=8, radius=0.08,
      ins=(0.2, 0.15, 0.2, 0.1))
s.box(6.71, y0 + 0.50, wb, 1.50,
      "$M\\geq2$: no regret upper bound.\n"
      "The authors only {red:conjecture} that the regret is $O(\\log T)$.",
      fill="pale-red", line="red", lw=1.0, size=18, align="l", anchor="t", bullet="•", gap=8, radius=0.08,
      ins=(0.2, 0.15, 0.2, 0.1))
s.quote(C.L, y0 + 2.30, C.W,
        "\"Despite our most sincere efforts, {u:we were unable to prove a regret upper bound} for Randomized Selfish KL-UCB "
        "in the multi-player setting. ... We conjecture that Randomized Selfish KL-UCB has logarithmic regret, and we believe "
        "that this is an important, but certainly challenging open problem.\"",
        source="[Trinh & Combes, 2021, Section 2.5]", size=18)
s.notes("何が証明され、何が証明されていないか\n"
        "\n"
        "最適性が証明されているのは 1 人の場合だけで、2 人以上では、著者はリグレット上界を証明できなかった。\n"
        "\n"
        "・証明されていること：\n"
        "  - $M=1$ のとき、R-SKL は漸近最適（命題 2）。\n"
        "  - 他の全員が固定の腕に留まるとき、残る 1 人にとって最適。\n"
        "・証明されていないこと：\n"
        "  - $M\\geq2$ のリグレット上界はない。\n"
        "  - 著者は、リグレットが $O(\\log T)$ であると **予想** しているだけである。\n"
        "・引用（2.5 節）の訳：「最大限の努力にもかかわらず、多人数の設定における Randomized Selfish KL-UCB のリグレット上界は証明できなかった。"
        "……Randomized Selfish KL-UCB のリグレットは対数オーダーであると予想する。これは重要だが、間違いなく難しい未解決問題であると考える。」\n"
        "\n"
        "【口頭補足】\n"
        "・1.3 節の「still seems to incur a logarithmic regret」、3.3 節の「its regret still seems logarithmic」も、根拠が実験であることを示す言い方。以降の実験は「証明のない手法の実験結果」として見る。")

# ---- なぜ解析が難しいのか（私の考察）
s = d.slide("Why Is the Multi-Player Analysis So Hard?",
            lead="The standard KL-UCB proof needs i.i.d. rewards and a single learner, and both assumptions break "
                 "when several selfish players collide.")
y = s.top + 0.02
items = [("Rewards are not i.i.d.:", "$r_m(t)$ depends on the arms chosen by the other players, and their choices depend on their own past."),
         ("The index is no longer optimistic:", "collisions make $\\hat{\\mu}_{m,k}$ smaller than $\\mu_k$, so $b_{m,k}(t)\\geq\\mu_k$ can fail even for a top arm."),
         ("$M$ learners are coupled:", "one must show that all players settle on different top-$M$ arms and stay there, with no phases to separate them in time."),
         ("The noise fades as $1/t$:", "the tie-breaking must succeed early, and without the noise the regret can be linear (Proposition 1).")]
for i, (h, t) in enumerate(items):
    s.num(C.L + 0.05, y - 0.06, i + 1, "ink")
    y = s.text(C.L + 0.70, y, C.W - 0.70, "{ink:%s}  %s" % (h, t), 20) + 0.10
s.text(C.L, y - 0.02, C.W, "These four points are our own view. The paper gives no reason why the proof failed.", 16, "warm")
s.notes("なぜ多人数の解析は難しいのか\n"
        "\n"
        "標準的な KL-UCB の証明は「報酬が i.i.d.」「学習者が 1 人」を使うが、自分勝手に動く複数のプレイヤーが衝突すると、どちらも成り立たなくなる。\n"
        "\n"
        "❶ 報酬が i.i.d. でない：$r_m(t)$ は他のプレイヤーが選んだ腕に依存し、その選択は各自の過去に依存する。\n"
        "❷ 指数が楽観的でなくなる：衝突で $\\hat{\\mu}_{m,k}$ が $\\mu_k$ より小さくなるので、上位の腕でも $b_{m,k}(t)\\geq\\mu_k$ が崩れうる。\n"
        "❸ $M$ 人の学習が絡み合う：全員が上位 $M$ 本の別々の腕に落ち着き、そこに留まることを示す必要がある。プレイヤーを時間で分けるフェーズもない。\n"
        "❹ 乱数が $1/t$ で消えていく：同点の解消は早いうちに成功しなければならない。乱数がなければリグレットは線形になりうる（命題 1）。\n"
        "・この 4 点は私の考察であり、原論文は証明できなかった理由を述べていない。\n"
        "\n"
        "【口頭補足】\n"
        "・❶ について：1 人用の証明は、腕 $k$ の $N$ 回の報酬が平均 $\\mu_k$ の i.i.d. であることから、$\\hat{\\mu}_k$ の集中不等式を使う。多人数では「腕 $k$ から得た報酬」の平均が、他人がその腕にいた割合で変わる。\n"
        "・❷ について：UCB 型の証明の要は「最適な腕の指数は高い確率で真の平均以上」。先に他人が座った上位の腕は平均 0 に見えるので、これは意図された振る舞いでもある。つまり「どの腕が自分にとって最適か」が他人の動きで変わる。\n"
        "・❸ について：SIC-MMAB や Huang et al. は、初期化で全員を別々の腕に分け、フェーズで同期することで、各フェーズを 1 人用に近い問題に分解して解析している。R-SKL にはその分解がない。\n"
        "・❹ について：命題 2 の証明では乱数の影響の和が有限であることだけを使えばよいが、多人数では逆に「乱数が十分に効いて分離が起きること」を示す必要があり、向きが逆になる。")
