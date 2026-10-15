#!/bin/bash
# 使い方: render.sh deck.pptx [出力ディレクトリ]
# Keynote で PDF に書き出し、ページ画像（qa/p-NN.png）と一覧画像（qa/sheet-N.jpg）を作る。
# PowerPoint が使えないときの代替。通常は render_pp.sh（PowerPoint の本番の描画）を使う。
# Keynote は PowerPoint の数式（OMML）を描画できるが、表の中の数式と Segoe UI は描けない。
# Keynote を終了させるので、本人が Keynote で作業中でないことを確かめてから使う。
set -e
IN="$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"
OUT="${2:-$(dirname "$IN")/qa}"
mkdir -p "$OUT"
BASE="$(basename "${IN%.*}")"
PDF="$OUT/$BASE.pdf"
rm -f "$PDF"
osascript -e 'tell application "Keynote" to quit saving no' >/dev/null 2>&1 || true
sleep 3
osascript <<OSA
tell application "Keynote"
  activate
  open POSIX file "$IN"
  repeat 90 times
    delay 1
    try
      set d to front document
      exit repeat
    end try
  end repeat
  delay 4
  export front document to POSIX file "$PDF" as PDF
  close front document saving no
end tell
tell application "Keynote" to quit saving no
OSA
rm -f "$OUT"/p-*.png "$OUT"/sheet-*.jpg
pdftoppm -r 60 -png "$PDF" "$OUT/p"
ls "$OUT"/p-*.png | split -l 12 - "$OUT/.chunk-"
i=1; for c in "$OUT"/.chunk-*; do montage $(cat "$c") -tile 3x4 -geometry +6+6 -background gray35 "$OUT/sheet-$i.jpg"; rm "$c"; i=$((i+1)); done
echo "$PDF"; ls "$OUT"/sheet-*.jpg
