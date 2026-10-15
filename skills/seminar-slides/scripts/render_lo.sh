#!/bin/bash
# LibreOffice で PDF と一覧画像 sheet-N.jpg を作る（PowerPoint がない環境・Linux 向け）。
#   render_lo.sh deck.pptx
# 注意：Segoe UI と PowerPoint の数式の描画は PowerPoint と少し違う。最終確認は PowerPoint（render_pp.sh）で行う。
set -e
IN="$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"
OUT="$(dirname "$IN")"
soffice --headless --convert-to pdf --outdir "$OUT" "$IN" >/dev/null
PDF="${IN%.*}.pdf"
rm -f "$OUT"/p-*.png "$OUT"/sheet-*.jpg
pdftoppm -r 60 -png "$PDF" "$OUT/p"
ls "$OUT"/p-*.png | split -l 12 - "$OUT/.chunk-"
i=1; for c in "$OUT"/.chunk-*; do montage $(cat "$c") -tile 3x4 -geometry +6+6 -background gray35 "$OUT/sheet-$i.jpg"; rm "$c"; i=$((i+1)); done
echo "$PDF"; ls "$OUT"/sheet-*.jpg
