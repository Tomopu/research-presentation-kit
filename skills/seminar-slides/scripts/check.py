#!/usr/bin/env python3
"""Structural check for a generated .pptx, plus a Quick Look render of slide 1.

    python3 check.py deck.pptx [--render outdir]

PowerPoint reports a file as "needs repair" rather than telling you what broke,
so verify before handing a deck over. Checks: zip integrity, every
[Content_Types] Override resolves, no dangling relationship targets, every part
has a content type, and the slide order in presentation.xml resolves.
"""

import os
import posixpath
import re
import subprocess
import sys
import zipfile

EMU = 914400  # EMU per inch


def check(path):
    problems = []
    with zipfile.ZipFile(path) as z:
        if z.testzip() is not None:
            problems.append("zip CRC failure in %s" % z.testzip())
        names = set(z.namelist())
        ct = z.read("[Content_Types].xml").decode()

        overrides = set(re.findall(r'Override PartName="/([^"]+)"', ct))
        for pn in overrides:
            if pn not in names:
                problems.append("Override points at missing part: %s" % pn)

        defaults = {e.lower() for e in re.findall(r'Default Extension="([^"]+)"', ct)}
        for n in names:
            if n.endswith("/"):
                continue
            ext = n.rsplit(".", 1)[-1].lower()
            if n not in overrides and ext not in defaults:
                problems.append("no content type for part: %s" % n)

        for n in (x for x in names if x.endswith(".rels")):
            base = posixpath.dirname(posixpath.dirname(n))
            for tgt, mode in re.findall(
                    r'Target="([^"]+)"(?:\s+TargetMode="(\w+)")?',
                    z.read(n).decode()):
                if mode == "External" or tgt.startswith("http"):
                    continue
                p = posixpath.normpath(posixpath.join(base, tgt))
                if p not in names:
                    problems.append("dangling relationship %s -> %s" % (n, p))

        pres = z.read("ppt/presentation.xml").decode()
        rels = z.read("ppt/_rels/presentation.xml.rels").decode()
        rid2 = dict(re.findall(r'Id="(rId\d+)"[^>]*Target="([^"]+)"', rels))
        order = []
        for rid in re.findall(r'<p:sldId[^>]*r:id="(rId\d+)"', pres):
            if rid not in rid2:
                problems.append("slide order references unknown %s" % rid)
            else:
                order.append(rid2[rid])
        if not order:
            problems.append("presentation has no slides")

        # anything hanging off the canvas is content the audience never sees
        sw, sh = re.search(r'sldSz cx="(\d+)" cy="(\d+)"', pres).groups()
        sw, sh = int(sw) / EMU, int(sh) / EMU
        shape_re = re.compile(r"<p:(sp|pic|cxnSp|graphicFrame)>.*?</p:\1>", re.S)
        for n, tgt in enumerate(order, 1):
            body = z.read("ppt/" + tgt).decode()
            tree = re.search(r"<p:spTree>.*</p:spTree>", body, re.S).group(0)
            for i, m in enumerate(shape_re.finditer(tree)):
                sp = m.group(0)
                off = re.search(r'<a:off x="(-?\d+)" y="(-?\d+)"/>', sp)
                ext = re.search(r'<a:ext cx="(\d+)" cy="(\d+)"/>', sp)
                if not (off and ext):
                    continue
                x, y = int(off.group(1)) / EMU, int(off.group(2)) / EMU
                w, h = int(ext.group(1)) / EMU, int(ext.group(2)) / EMU
                rot = re.search(r'<a:xfrm[^>]*rot="(-?\d+)"', sp)
                if rot and round(int(rot.group(1)) / 60000) % 180 == 90:
                    # 90°/270° 回転した図形は、中心を保ったまま縦横が入れ替わって見える
                    cx, cy = x + w / 2, y + h / 2
                    w, h = h, w
                    x, y = cx - w / 2, cy - h / 2
                r, b = x + w, y + h
                if r > sw + 0.02 or b > sh + 0.02 or x < -0.02 or y < -0.02:
                    txt = "".join(re.findall(r"<a:t>([^<]*)</a:t>", sp))[:28]
                    problems.append(
                        "slide %d shape %d off-canvas: (%.2f,%.2f)-(%.2f,%.2f) %s"
                        % (n, i, x, y, r, b, txt))

    print("%s: %d slides" % (os.path.basename(path), len(order)))
    for p in problems:
        print("  FAIL", p)
    print("  OK" if not problems else "  %d problem(s)" % len(problems))
    return not problems


def render(path, outdir):
    """Quick Look renders slide 1 only -- enough to catch a corrupt file and to
    eyeball the cover. Full visual QA still needs PowerPoint or Keynote."""
    os.makedirs(outdir, exist_ok=True)
    r = subprocess.run(["qlmanage", "-t", "-s", "1600", "-o", outdir, path],
                       capture_output=True, text=True)
    made = [f for f in os.listdir(outdir) if f.endswith(".png")]
    if not made:
        print("  render FAILED (Quick Look produced nothing -- file may be corrupt)")
        print(r.stdout.strip()[-400:] or r.stderr.strip()[-400:])
        return False
    print("  rendered:", ", ".join(posixpath.join(outdir, m) for m in made))
    return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    ok = check(sys.argv[1])
    if "--render" in sys.argv:
        i = sys.argv.index("--render")
        ok = render(sys.argv[1], sys.argv[i + 1] if len(sys.argv) > i + 1
                    else "render") and ok
    sys.exit(0 if ok else 1)
