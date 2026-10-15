#!/usr/bin/env bash
# research-presentation-kit を入れる。
#   1. リポジトリに Python の環境 .venv を作り、requirements.txt を入れる
#   2. skills/ の各スキルを ~/.claude/skills/ にシンボリックリンクする（各スキルの .venv はリポジトリの .venv を指す）
#   3. 外部の道具（ffmpeg・poppler・ImageMagick・PowerPoint / LibreOffice・say）があるかを確かめる
#
#   bash install.sh                       # python3 を使う
#   PYTHON=python3.12 bash install.sh
#   CLAUDE_SKILLS_DIR=/path/to/skills bash install.sh
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
PYTHON="${PYTHON:-python3}"
SKILLS_DIR="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"

"$PYTHON" -c 'import sys; assert sys.version_info >= (3, 10), "Python 3.10 以上が要る"'
echo "== Python の環境: $ROOT/.venv"
[ -x "$ROOT/.venv/bin/python" ] || "$PYTHON" -m venv "$ROOT/.venv"
"$ROOT/.venv/bin/pip" install -q --upgrade pip
"$ROOT/.venv/bin/pip" install -q -r "$ROOT/requirements.txt"

echo "== スキルのリンク: $SKILLS_DIR"
mkdir -p "$SKILLS_DIR"
for d in "$ROOT"/skills/*/; do
  name="$(basename "$d")"
  ln -sfn ../../.venv "$ROOT/skills/$name/.venv"
  dst="$SKILLS_DIR/$name"
  if [ -e "$dst" ] && [ ! -L "$dst" ]; then
    # 前からある実体のフォルダは退避する。中の過去資料（assets/reference/*.pptx）はリポジトリ側へ写す
    if [ -d "$dst/assets/reference" ]; then
      find "$dst/assets/reference" -maxdepth 1 -name '*.pptx' -exec cp -n {} "$ROOT/skills/$name/assets/reference/" \;
    fi
    # スキルのフォルダの中に残すと同じ名前のスキルが 2 つ読まれるので、外（~/.claude/skill-backups/）へ退避する
    mkdir -p "$HOME/.claude/skill-backups"
    bak="$HOME/.claude/skill-backups/$name.bak-$(date +%Y%m%d%H%M%S)"
    mv "$dst" "$bak"
    echo "   既存の $dst を $bak に退避した"
  fi
  ln -sfn "$ROOT/skills/$name" "$dst"
  echo "   $name -> $ROOT/skills/$name"
done

echo "== 外部の道具"
check() { command -v "$1" >/dev/null && echo "   ok  $1" || echo "   なし $1 （$2）"; }
check ffmpeg   "動画の書き出しに必須"
check pdftoppm "poppler。スライドの確認画像に必要"
check montage  "ImageMagick。スライドの一覧画像に必要"
check say      "macOS の読み上げ。なければ VIDEO_TTS=silent / espeak"
if [ -d "/Applications/Microsoft PowerPoint.app" ]; then echo "   ok  PowerPoint"; else check soffice "PowerPoint がないときのスライド確認（LibreOffice）"; fi

n=$(find "$ROOT/skills/seminar-slides/assets/reference" -maxdepth 1 -name '*.pptx' | wc -l | tr -d ' ')
echo "== 過去資料: skills/seminar-slides/assets/reference/ に $n 個（README.md を参照）"
echo "完了。Python: $ROOT/.venv/bin/python"
