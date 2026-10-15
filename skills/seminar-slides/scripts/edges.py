#!/usr/bin/env python3
"""PowerPoint で書き出した PDF の各ページで、本文が端の余白に食い込んでいないかを画素で調べる。

    python edges.py deck.pdf

見積もりではなく実際の描画で判定する（数式や表は見積もりより大きく描かれることがある）。
下端 6.86〜6.99in（その下は左下の出典 12pt の場所、右下はページ番号）、左 0.40in・右 12.90in の外に
背景でない画素があれば、そのページを報告する。セクション扉（紺地）は調べない。
"""
import subprocess
import sys
import tempfile
import os

from PIL import Image

DPI = 40


def check(pdf):
    bad = 0
    with tempfile.TemporaryDirectory() as d:
        subprocess.run(["pdftoppm", "-r", str(DPI), "-png", pdf, os.path.join(d, "p")], check=True)
        files = sorted(f for f in os.listdir(d) if f.endswith(".png"))
        for k, f in enumerate(files, 1):
            im = Image.open(os.path.join(d, f)).convert("RGB")
            W, H = im.size
            px = im.load()
            if sum(px[5, 5]) < 200 and sum(px[W - 5, H // 2]) < 200:
                continue      # 紺地の扉
            def ink(x0, y0, x1, y1):
                n = 0
                for x in range(int(x0 * DPI), min(W, int(x1 * DPI))):
                    for y in range(int(y0 * DPI), min(H, int(y1 * DPI))):
                        r, g, b = px[x, y]
                        if r + g + b < 690:
                            n += 1
                return n
            msgs = []
            if ink(0.3, 6.86, 9.9, 6.99) > 3:
                msgs.append("下端（6.86in より下）に食い込み")
            if ink(12.92, 1.2, 13.3, 6.9) > 3:
                msgs.append("右端（12.92in より右）に食い込み")
            if ink(0.02, 1.2, 0.40, 6.9) > 3:
                msgs.append("左端（0.40in より左）に食い込み")
            if msgs:
                bad += 1
                print("page %d: %s" % (k, "、".join(msgs)))
    print("%d page(s) with edge problems" % bad)
    return bad


if __name__ == "__main__":
    sys.exit(1 if check(sys.argv[1]) else 0)
