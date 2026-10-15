# research-presentation-kit

研究発表の資料を、泉 知成の過去資料と同じデザインで作るための Claude Code スキルと描画エンジンのセット。

| スキル | 作るもの | エンジン |
|---|---|---|
| [`seminar-slides`](skills/seminar-slides/) | 論文ゼミ・輪講ゼミ・修論発表のスライド（`.pptx`）。英語本文＋日本語ノート、数式は PowerPoint の数式、図は PowerPoint の図形 | `scripts/deck.py`（python-pptx）、`omml.py`（LaTeX → 数式）、`lint.py` ほか検査 |
| [`explainer-video`](skills/explainer-video/) | 概念の説明動画（`.mp4`）。日本語ナレーション・字幕・アニメーション | `scripts/video.py`（matplotlib のコマ＋TTS＋ffmpeg） |

Claude Code に「論文ゼミのスライドを作って」「この内容を動画にまとめて」と頼むと、対応するスキルが読まれる。
規則（色・寸法・文字サイズ、本人のフィードバック、避ける癖）は各スキルの `SKILL.md` にある。

## セットアップ

### 1. 外部の道具

| 道具 | 用途 | macOS（Homebrew） |
|---|---|---|
| Python 3.10 以上 | エンジン | `brew install python@3.12` |
| ffmpeg | 動画の書き出し | `brew install ffmpeg` |
| poppler（`pdftoppm`） | スライドの確認画像 | `brew install poppler` |
| ImageMagick（`montage`） | スライドの一覧画像 | `brew install imagemagick` |
| Microsoft PowerPoint | スライドの本番の描画確認（`render_pp.sh`） | App Store / Microsoft 365 |
| LibreOffice（任意） | PowerPoint がない環境での確認（`render_lo.sh`） | `brew install --cask libreoffice` |
| `say`（macOS に標準） | 動画の読み上げ（声は Kyoko） | ― |

Linux では `apt install python3-venv ffmpeg poppler-utils imagemagick libreoffice fonts-noto-cjk` で足りる
（読み上げは `VIDEO_TTS=silent` か `espeak`。本番の声は macOS で作る）。

### 2. clone してインストール

```bash
git clone https://github.com/Tomopu/research-presentation-kit.git ~/develop/research-presentation-kit
cd ~/develop/research-presentation-kit
bash install.sh
```

`install.sh` がすること：
- リポジトリに `.venv` を作り、`requirements.txt`（python-pptx・lxml・matplotlib・numpy・pandas）を入れる
- `skills/seminar-slides` と `skills/explainer-video` を `~/.claude/skills/` にシンボリックリンクする
  （前からある同名のフォルダは `~/.claude/skill-backups/` に退避し、中の過去資料はリポジトリ側へ写す）
- 外部の道具があるかを表示する

更新は `git pull` だけでよい（リンクなので、そのまま反映される）。

### 3. 本人の過去資料を置く（スライドの図を複製するとき）

`seminar-slides` は本人の過去資料から図を複製する（`paste()`）。資料はリポジトリに入れていないので、各環境で置く。

```bash
cp 論文ゼミ_泉0421.pptx 泉知成_修論中間発表スライド_完成.pptx スライドデザイン変更点まとめ.pptx \
   ~/develop/research-presentation-kit/skills/seminar-slides/assets/reference/
```

置かなくても、`paste()` 以外（部品で描く図・数式・表・検査）はすべて動く。詳しくは
[`assets/reference/README.md`](skills/seminar-slides/assets/reference/README.md)。

### 4. 動くか確かめる

```bash
PY=~/.claude/skills/seminar-slides/.venv/bin/python
$PY ~/.claude/skills/seminar-slides/examples/fixes_20261015.py /tmp/check.pptx
$PY ~/.claude/skills/seminar-slides/scripts/lint.py /tmp/check.pptx
cd ~/.claude/skills/explainer-video/examples/ucb_klucb && $PY ucb_sim.py && VIDEO_TTS=silent $PY ucb_explainer.py preview 5
```

## 手本（gallery）

### スライド：本人の仕上げた資料

`gallery/slides/` は、本人が仕上げた論文ゼミ（Trinh & Combes 2021、90 分）の抜粋。デザインの合格基準はこの見た目。

| | |
|---|---|
| ![](gallery/slides/cover.png) 表紙 | ![](gallery/slides/setup.png) 問題設定（過去資料の図を複製） |
| ![](gallery/slides/taxonomy.png) 分類の木（難易度の矢印） | ![](gallery/slides/timeline.png) 年表と位置づけ |
| ![](gallery/slides/algorithm.png) アルゴリズム（流れ＋擬似コード） | ![](gallery/slides/example.png) 動作の対比の図 |
| ![](gallery/slides/experiment.png) 原論文の実験図と読み方 | ![](gallery/slides/table.png) 表のデザイン |

### スライド：本人が Claude の資料を直した点（変更前 → 変更後）

| 変更前 | 変更後 | 直した点 |
|---|---|---|
| ![](gallery/fixes/1_fieldset_before.png) | ![](gallery/fixes/1_fieldset_after.png) | 塗りの箱をやめ、白地・色枠・見出しを枠の上辺に（`fieldset()`） |
| ![](gallery/fixes/2_collision_before.png) | ![](gallery/fixes/2_collision_after.png) | 南京錠は固定されたプレイヤーの横、爆発は腕に重ねず矢印が集まる所（`collide()`） |
| ![](gallery/fixes/3_points_before.png) | ![](gallery/fixes/3_points_after.png) | 箇条書きを箱で囲まない。色つき見出し＋色つきの要点（`points()`） |

### 動画

| | | |
|---|---|---|
| ![](gallery/video/ts_30.png) | ![](gallery/video/ts_230.png) | ![](gallery/video/ts_262.png) |
| ![](gallery/video/ucb_70.png) | ![](gallery/video/ucb_185.png) | ![](gallery/video/ucb_230.png) |

## 構成

```
install.sh              セットアップ
requirements.txt        Python のパッケージ（版を固定）
skills/seminar-slides/  スライドのスキル（SKILL.md・references/・scripts/・assets/・examples/）
skills/explainer-video/ 動画のスキル（SKILL.md・scripts/video.py・examples/）
gallery/                手本の画像
```
