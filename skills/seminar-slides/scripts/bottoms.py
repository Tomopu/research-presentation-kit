import sys, glob, subprocess, os, tempfile
from PIL import Image
D = 50
pdf = sys.argv[1]
with tempfile.TemporaryDirectory() as t:
    subprocess.run(["pdftoppm", "-r", str(D), "-png", pdf, t + "/p"], check=True)
    for f in sorted(glob.glob(t + "/p-*.png")):
        im = Image.open(f).convert("RGB"); W, H = im.size; px = im.load()
        if sum(px[5, 5]) < 200:
            continue
        low = 0
        for y in range(int(6.0 * D), int(7.45 * D)):
            for x in range(int(0.3 * D), int(9.9 * D)):
                if sum(px[x, y]) < 690:
                    low = y; break
        n = int(f.rsplit("-", 1)[1][:-4])
        flag = "  <-- over" if low / D > 6.80 else ""
        if flag or "-a" in sys.argv:
            print("page %2d (slide no. %2d): content bottom %.2f in%s" % (n, n - 1, low / D, flag))
