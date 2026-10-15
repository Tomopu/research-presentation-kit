#!/bin/bash
# PowerPoint で PDF に書き出し、ページ画像 qa/p-NN.png と一覧画像 qa/sheet-N.jpg を作る。
# 使い方: render_pp.sh deck.pptx   （wip_trinh2021 へのアクセス許可が PowerPoint に要る）
set -e
IN="$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"
OUT="$(dirname "$IN")"
PDF="${IN%.*}.pdf"
rm -f "$PDF"
osascript <<OSA
with timeout of 600 seconds
tell application "Microsoft PowerPoint"
  open POSIX file "$IN"
  delay 6
  set p to missing value
  repeat with q in (get every presentation)
    if full name of q is "$IN" then set p to contents of q
  end repeat
  save p in (POSIX file "$PDF") as save as PDF
  close p saving no
end tell
end timeout
OSA
rm -f "$OUT"/p-*.png "$OUT"/sheet-*.jpg
pdftoppm -r 60 -png "$PDF" "$OUT/p"
ls "$OUT"/p-*.png | split -l 12 - "$OUT/.chunk-"
i=1; for c in "$OUT"/.chunk-*; do montage $(cat "$c") -tile 3x4 -geometry +6+6 -background gray35 "$OUT/sheet-$i.jpg"; rm "$c"; i=$((i+1)); done
echo "$PDF"; ls "$OUT"/sheet-*.jpg
