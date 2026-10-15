# 構成の組み立て規則

過去3資料（0421 / 0622 / 0728）に共通する骨格。**節の切れ目ごとに
「扉 → Flow 再掲 → 本文群」の3点セット**を置くのが本資料の最大の特徴。

## デッキ全体の並び

```
cover                          表紙
toc                            目次（❶❷❸…で章節を列挙）
divider   "Chapter 7. ..."     章の扉
  content ×2                   章全体の位置づけ・分類
divider   "7.1 ..."            節の扉
  content                      節の導入
  flow    "Flow of Section 7.1"  この節のロードマップ（初出）
divider   "7.1.1 ..."          小節の扉
  flow    "Flow of Section 7.1"  ★同じ Flow を再掲（現在地を示す）
  content ×5                   本文
divider   "7.1.2 ..."
  flow    "Flow of Section 7.1"  ★再掲
  content ×10
divider   "7.1.3 ..."
  flow    "Flow of Section 7.1"  ★再掲
  content ×9
divider   "Conclusion"
conclusion                     まとめ
```

分量の目安: 40枚で1節（小節3つ）。23枚なら小節2つ程度に絞る。

## 枚数と発表時間

本文スライド1枚あたり 1.5〜2.5 分（1枚に図と例を厚く載せるため）。

| 発表時間 | 全体（表紙・目次・扉込み） |
|---|---|
| 7〜10 分（修論発表など） | 12〜15 枚 |
| 30 分 | 20〜25 枚 |
| 90 分（論文ゼミ） | 45〜55 枚。動作例を (1/n) で割る分は速く進むので多めでよい |

水増ししない。簡潔に言える所（応用例・関連研究の列挙）は1枚で済ませ、時間はアルゴリズムの動作例と
実験の読み取りに使う。

## 論文ゼミの標準構成

```
cover → toc
divider Introduction     問題設定（図）→ 設定の分類 → 先行研究 → 本論文の貢献
divider Algorithm        Overview → 部品の定義 → 小さな例で動作 (1/n)…(n/n) → 理論の状況
divider Experiments      設定 → 図ごとに1枚（リードで読み取りを言い切る）
divider （自分の研究との比較・考察）
divider Conclusion       まとめ → 未解決の点・議論したい問い
References
```

## 各型の書き方

### cover（表紙）

| スロット | 内容 | 例 |
|---|---|---|
| `tag` | ゼミ種別 | `輪講ゼミ 発表資料` / `論文ゼミ 発表資料` |
| `title` | 書名・論文名 | `Graph Representation Learning` |
| `authors` | 原著者＋所属番号 | `William L. Hamilton1` |
| `venue` | 会議名・担当範囲 | `35th Conference on NeurIPS (NeurIPS 2021).` / `Chapter 7. Theoretical Motivation (pp. 75ー84)` |
| `date` `grade` `name` | 日付＋学年＋氏名 | `22.06.2026` `M2` `泉 知成` |
| `affiliations` | 所属脚注（リスト） | `["¹ McGill University"]` |

日付は **DD.MM.YYYY**。ページ範囲の区切りは全角の `ー`。

### toc（目次）

`items` に `❶ ` `❷ ` … を先頭に付けて改行区切りで列挙。章と節を混ぜてよい。
番号記号のあとは**半角スペース2つ**。

### divider（セクション扉）

濃紺一色の背景に白抜き見出しだけ。章番号を必ず含める（`Chapter 7. ...`,
`7.1.2 From Time Signals to Graph Signals`）。本文は置かない。

### flow（Flow of Section）

その節を3段階に分けて示すロードマップ。**同一の内容を小節の頭で毎回再掲する**
ことで、聴衆が現在地を見失わないようにしている。

- `lead` … 3段階を1〜2文で要約（「First, we introduce ..., and then generalize ...」）
- `step1..3` … 小節番号＋小節名（`7.1.1 Convolutions and the Fourier Transform`）
- `desc1..3` … 各段で何をするかを1〜2文

3段階に割り切れない節では無理に使わない。

### content（本文）

タイトル＋リード文＋本文領域。本資料の本文スライドは次の順で組む:

1. **タイトル** … 主張を名詞句で（`Shift Equivariance of Convolution`）
2. **リード文** … そのスライドの結論を1〜2文で言い切る（淡青の帯）
3. **本文** … 定義・式・図。式は PowerPoint の数式（`eq()`）、式番号は原典どおり
4. 必要なら出典

長い話題は `(1/5)` … `(5/5)` をタイトル末尾に付けて分割する。

### Review スライド

担当範囲より前の内容を使うときは、本文に入る前に `content` で再掲する。
タイトルは `Review (1/2)` や `Review (The connected n-point function)`。
原典の式番号（`(2.3)`, `(1.52)`）を必ず添える。

### diagram（3項目＋統合の図解）

3つの起源・3つの手法などを並べて1つに収束させる図。
角丸の箱3つ（項目名＋引用 `[Bruna+, 2014]`）、その下に一言説明、矢印で下の箱に収束させる。

### conclusion（まとめ）

`lead` に全体の要約、本文に要点を ❶〜❺ の `steps()` か箇条書きで。`source()` に参照元。

## 文体

- スライド本文は英語。ノートにタイトルと本文の日本語訳を書く（SKILL.md「ノート」）。
- 主張は言い切る（`X is Y.`）。「〜について説明する」で終わらせない。
- 箇条書きの多用を避け、リード文＋図式で見せる。
