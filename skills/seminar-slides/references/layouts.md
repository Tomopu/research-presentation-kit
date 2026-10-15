# ページの型（座標つき）

本人の資料から抜き出した型。座標はインチ。リード帯の下端を `s.top` とする（1行なら 2.27、2行なら 2.59）。
**どの型も本文が 6.8in 前後まで届く。** 届かないときは図を大きくする。

## A. 定義＋数式＋記号の説明（1カラム）

本人の例：Setup: Regret Definition、Convolution の定義、Laplace operator。

```
[リード帯]
Definition:                         (太字 20pt, x 0.54)
  The regret after T rounds ...     (20pt, x 0.80)
            R(T) = ...                       (7.12)   ← 数式 22〜24pt 中央、式番号は右端
 ⎧ where:                                          ⎫  ← 角かっこ(中かっこ)で囲んで記号の説明
 ⎨ • V(S(t),t) = ... : System reward   • μ = ...   ⎬     箇条書きを2列に並べてよい（記号の説明だけ）
 ⎩ • S = {...}                                     ⎭
```

## B. 図（左）＋規則の箱（右）

本人の例：Orthogonalization procedure (1/9)〜(9/9)、Rank Assignment。アルゴリズムの動作例はこれ。

```
[リード帯：このステップで何が起きるかを1〜2文]
Example: [t = 2]                     t  0 1 [2] 3        ← 右上：時刻の帯（x 8.0〜12.66）
Arm k (K = 4)   [▣] [▣] [✸] [▣]       Communication Phase
                  ↖   ↑   ↗           ┌────────────────────┐
Player m (M = 3)  🧍   🧍   🧍          │ if s_m = 0 then ... │  ← 規則の箱（x 8.0〜12.66, y 4.4〜6.8）
State s_m        s=0  s=0 [s=3]        │ else ...  ▒▒▒▒▒▒▒▒ │
                         2 mod 4 = 2   └────────────────────┘
```

- 図の領域 x 0.54〜7.8、規則の箱 x 8.0〜12.66。**左右とも下端 6.8 まで**
- 同じ型を (1/9)…(9/9) と続け、変わるところだけ変える

## C. Overview（段階の一覧）

本人の例：Overview of the Algorithm（段階が変わるたびに再掲）。

```
[リード帯：アルゴリズム全体を1〜2文]
Initialization Phase [Wang+ 2020]        (緑 太字)
❶ Orthogonalization Procedure:  説明      (緑の❶、見出しは緑太字、説明は黒)
▼
❷ Rank Assignment:  説明
Algorithm BEACON                          (青 太字)
❸ Communication Phase:  説明
▼
❹ Exploration Phase:  説明
```

`steps()` を2回（緑・青）。再掲するときは今の段以外を `gray` にしてもよい。

## D. 分類の木＋右に観測量

本人の例：Classification of MP-MAB (1/2), (2/2)、Convolutional GNN Model Classification。
左から根→枝→葉。葉の右に数式。右端に「Difficulty」の縦矢印。注目の葉は赤。

## E. 図を大きく＋キャプション

本人の例：Numerical Experiment、Three Theoretical Origins of GNNs。
図は 0.54〜12.66 の幅いっぱい（2枚なら左右に 5.8in ずつ）、下に `Figure N:` とキャプション 16pt。
リード帯で「図から何が読めるか」を言い切る。読み取ってほしい所に赤枠・吹き出し。

## F. 箇条書き＋小見出し（文章のページ）

本人の例：Abstract、Setup: Constraints、Problems of the Conventional Communication Phase。

```
Background & Problem :                    (太字)
 • ...（20pt、2行まで）
Objectives of this Paper:
 ❶ ...                                    (丸数字 28pt＋本文)
 ❷ ...
```

文章だけのページでも、下半分に小さな図（例：Sender→arm←Sender の通信の図）を入れて
6.8in まで埋めるのが本人の書き方。

## G. 表が主役

本人の例：Rank Assignment (1/2)・(2/2)。
左に表（幅 7〜9in）、右に説明の箇条書きと規則の箱。または表を幅いっぱいにして丸で印を付ける。

## H. Flow of Section（節の現在地）

本人の例：Flow of Section 7.1（各小節の頭で再掲）。
3段を横線でつなぎ、点（●）を置き、上に小節名（太字 18pt）、下に説明（18pt）。今の段だけ赤、他は灰色。

```python
xs = [2.2, 6.67, 11.1]                         # 点の中心
s.line(0.9, 4.75, 12.4, 4.75, "gray", 1.5)
for i, (t, d) in enumerate(steps):
    c = "red" if i == cur else "gray"
    s.shape("ellipse", xs[i]-0.11, 4.64, 0.22, 0.22, fill=c, line=c)
    s.text(xs[i]-1.9, 3.75, 3.8, t, 18, c, True, align="ctr")
    s.text(xs[i]-1.9, 5.05, 3.8, d, 18, c, align="ctr")
```

## I. 比較（左右対称）

本人の例：Difference between Homogeneous and Heterogeneous。
左右に同じ形の図、中央に灰色の縦線。違う所だけ赤。下に1行の結論。

## J. 定理（数式の項に名前）

本人の例：Regret Analysis for Linear Reward Function。
`Theorem 1:` 太字、1行の主張、数式を大きく（24pt）、項の下に `\underbrace{}_{\text{...}}`、
その下に「Comparison with Previous Work and Lower Bound」の箇条書き（数式つき）。

## 本人の資料との見比べ

一覧画像を作って並べる。

```bash
scripts/render_pp.sh assets/reference/論文ゼミ_泉0421.pptx   # PDF と画像を作ってから見比べる
montage /tmp/ref/p-1[3-9].png -tile 3x -geometry +4+4 ref.jpg
```

- 論文ゼミ：`assets/reference/論文ゼミ_泉0421.pptx`（14〜17 枚目は非表示）
- 輪講ゼミ：`~/reserch/03_slides/01_輪講ゼミ/輪講ゼミ_泉0622.pdf`（本人の手元だけ。同梱していない）
- 修論発表：`assets/reference/泉知成_修論中間発表スライド_完成.pptx`
- Claude の資料を本人が直した例：`assets/reference/スライドデザイン変更点まとめ.pptx`（変更前・変更後）

## 箇条書き・対比・結論の型（2026-10-15 本人の修正）

作例：`examples/fixes_20261015.py`（変更点まとめの「変更後」3 枚を部品だけで組んだもの）。

- **対比の 2 列**（例：Cautions / Reasons to trust）：リード帯の下 2.59in に、左右 5.95in ずつ（隙間 0.22in）の
  `points(heading=..., color="red" / "green")`。箱で囲まない
- **結論の囲み**（例：Good runs / Bad runs）：下端 6.8in に揃えて `fieldset()` を横に 2 つ（高さ 0.94in、幅 5.95in）。
  見出しは枠の上辺（y − 0.30）に 20pt 太字で載る
- **衝突の図**（左半分 0.54〜6.0in）＋**実験の棒グラフ**（右半分 6.35〜12.66in）：図は `collide()` と `lock()`、
  右のグラフの下に赤字 18pt の一言（「The best arm looks like the worst arm to P2.」）
