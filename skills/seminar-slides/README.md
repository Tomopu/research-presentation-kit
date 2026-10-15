# seminar-slides

泉 知成のスライド（論文ゼミ・輪講ゼミ・修論発表）を、本人が作った過去資料と同じデザインで
`.pptx` として生成する Claude Code スキル。使い方と規則は `SKILL.md`。

## 構成

| パス | 内容 |
|---|---|
| `SKILL.md` | 規則・手順（Claude が読む本体） |
| `references/design-tokens.md` | 色・書体・文字サイズ・グリッド・線（実測値） |
| `references/layouts.md` | ページの型と座標 |
| `references/figures.md` | 説明図の語彙（プレイヤー・腕・衝突・南京錠・擬似コード・表・木・流れ） |
| `references/structure.md` | デッキ全体の骨格・枚数の目安 |
| `references/thesis.md` | 日本語スライド（修論発表）の型 |
| `scripts/deck.py` | 描画エンジン（python-pptx） |
| `scripts/omml.py` | LaTeX → PowerPoint 数式（OMML） |
| `scripts/lint.py` | レイアウト検査（余白過多・2カラム・数式の書き漏れ・はみ出し・ノート） |
| `scripts/check.py` | ファイル構造の検査 |
| `scripts/render.sh` | Keynote で PDF と一覧画像を作る |
| `assets/base.pptx` | 土台（論文ゼミ_泉0421 のマスター・レイアウト・テーマ） |
| `assets/icons/` | human / slot / lock の画像 |
| `assets/reference/` | 本人の過去資料を各環境で置く場所（リポジトリには入れない。中の README.md を参照） |
| `scripts/render_pp.sh` / `render_lo.sh` | PowerPoint（macOS）/ LibreOffice で PDF と一覧画像を作る |
| `examples/trinh2021/` | 作例（論文ゼミ 90 分。`build_1014.py` と `parts/`。本人の手元のパスを参照する部分がある） |
| `examples/fixes_20261015.py` | 本人の修正（箱を使わない箇条書き・結論の囲み・衝突の図）を部品だけで組んだ作例 |

## 必要なもの

- Python 3.10 以上と、リポジトリの `requirements.txt` のパッケージ。リポジトリの `install.sh` で `.venv` に入る
- poppler（`pdftoppm`）、ImageMagick（`montage`）
- 描画の確認：PowerPoint（`render_pp.sh`、macOS）、なければ LibreOffice（`render_lo.sh`）か Keynote（`render.sh`）
- PowerPoint（最終確認。Segoe UI は PowerPoint のクラウドフォント）

## 旧版

2026-10-05 以前の版（見本スライドを複製する方式、投影用に配色を濃くしていた）は
`~/.claude/skill-backups/seminar-slides-20261005/` に退避した。今の版は配色を本人の実測値に戻している。
| `scripts/restyle.py` | 出来上がった資料の色・表・切り替え効果だけを本人の指定に書き換える |

## 別の環境に持っていくとき

リポジトリの README.md を参照（clone → `bash install.sh` → `assets/reference/` に過去資料を置く）。

## 2026-10-15 の改訂

本人が Claude の資料を直した点（`assets/reference/スライドデザイン変更点まとめ.pptx`）を規則と部品に入れた。
- 箇条書きを塗りの箱で囲まない → `points()`、`lint.py` が箱の使いすぎを警告
- 短い結論の囲みは白地・色枠・見出しを枠の上辺に → `fieldset()`
- 衝突と固定の図：南京錠は固定されたプレイヤーの横、爆発は腕に重ねず矢印が集まる所 → `collide()`、`lock()`
改訂前の版は `~/.claude/skill-backups/seminar-slides-20261015/`。
