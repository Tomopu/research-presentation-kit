"""日本語ナレーション・字幕つきの説明動画を、matplotlib のコマと TTS の音声で作るエンジン。

台本（場面ごとの (字幕, 読み上げ) の列）と、場面ごとの描画関数 draw(fig, t, cues, data) を渡すと、

1. 文ごとに TTS で音声を作って長さを測り（cues = 各文の (開始, 終了) 秒）
2. 場面ごとに 1 コマずつ描いて ffmpeg に流し、音声と合わせ（場面は並列に作る）
3. 場面をつないで 1 本の mp4 にする

    import sys, os; sys.path.insert(0, "<skill>/scripts")
    from video import *                      # 色・部品・Video
    SCENES = [dict(title="1. 仕組み", lines=[("字幕の文。", "読み上げの文。"), ...]), ...]
    def draw0(fig, t, cues, data):
        i = which(cues, t)                   # いま読んでいる文の番号
        frame_base(fig, SCENES[0]["title"], SCENES[0]["lines"][i][0])
        ...
    Video(SCENES, [draw0, ...], build_data=lambda: {}, out="out.mp4").main(sys.argv[1:])

コマンド：`python script.py`（全部）、`python script.py 3 5`（場面 3 と 5 だけ作り直してつなぐ）、
`python script.py preview [場面...]`（各文の終わりのコマを PNG にして配置を確かめる）。

TTS は環境変数 VIDEO_TTS で選ぶ：say（macOS、既定。声は VIDEO_VOICE、既定 Kyoko）、
espeak（espeak-ng。日本語の質は低い）、silent（無音。文字数から長さを見積もる。配置の確認用）。
"""
from __future__ import annotations

import math
import os
import shutil
import subprocess
import sys
import wave
from concurrent.futures import ProcessPoolExecutor

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Ellipse  # noqa: F401（作例が使う）
import numpy as np

# ------------------------------------------------------------------ 設定
FPS = 24
W, H = 1280, 720
GAP = 0.30          # 文と文のあいだの無音（秒）
HEAD = 0.6          # 場面の最初の無音（秒）
TAIL = 0.8          # 場面の最後の余白（秒）
SR = 22050
FFMPEG = os.environ.get("FFMPEG") or shutil.which("ffmpeg") or "/opt/homebrew/bin/ffmpeg"
TTS = os.environ.get("VIDEO_TTS", "say" if sys.platform == "darwin" else "silent")
VOICE = os.environ.get("VIDEO_VOICE", "Kyoko")
RATE = int(os.environ.get("VIDEO_RATE", "205"))

# 色（seminar-slides と同じ値）
NAVY, INK, GRAY, LIGHT = "#0D114A", "#1C1F28", "#7F7F7F", "#D9DBE8"
YEL, PRED, PANEL = "#F6EAC3", "#FFCEC6", "#F4F5FA"
RED, GREEN, ORANGE, BLUE = "#D14B46", "#196723", "#E69F00", "#0070C0"


def _setup_fonts():
    """日本語の書体を選ぶ（macOS はヒラギノ、Linux は Noto Sans CJK JP など）。"""
    have = {f.name for f in font_manager.fontManager.ttflist}
    cands = ["Hiragino Sans", "Noto Sans CJK JP", "Noto Sans JP", "IPAexGothic", "Yu Gothic", "Arial Unicode MS"]
    plt.rcParams["font.family"] = [c for c in cands if c in have] or ["sans-serif"]
    plt.rcParams["mathtext.fontset"] = "cm"
    plt.rcParams["axes.facecolor"] = "none"


_setup_fonts()


# ------------------------------------------------------------------ 描画の部品
def wrap_ja(text, width):
    """日本語の字幕を折り返す。全角を 1、半角を 0.55 と数え、読点・句点の直後（なければ空白）で切る。"""
    lines, cur, w = [], "", 0.0
    for ch in text:
        cur += ch
        w += 0.55 if ord(ch) < 0x2000 else 1.0
        if w >= width:
            cut = max(cur.rfind("、"), cur.rfind("。"))
            if cut < len(cur) * 0.5:
                cut = cur.rfind(" ")
            if cut < len(cur) * 0.5:
                cut = len(cur) - 1
            lines.append(cur[:cut + 1].strip())
            cur = cur[cut + 1:]
            w = sum(0.55 if ord(c) < 0x2000 else 1.0 for c in cur)
    if cur.strip():
        lines.append(cur.strip())
    out = []
    for ln in lines:            # 句読点だけが次の行に落ちないようにする
        if out and ln and ln[0] in "、。」）":
            out[-1] += ln[0]
            ln = ln[1:]
        if ln:
            out.append(ln)
    return out


def box(fig, x, y, w, h, fc, ec="none", lw=1.5, r=0.012, z=-1):
    """図の座標（0〜1）で角丸の面を置く。既定では軸より下に描く（軸の背景は透明）。"""
    fig.add_artist(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=fc, ec=ec, lw=lw,
                                  transform=fig.transFigure, zorder=z))


def frame_base(fig, title, caption):
    """1 コマの土台：白地、左上のタイトル（紺 26pt）と下線、下の字幕の帯（D9DBE8）。"""
    fig.clf()
    fig.patch.set_facecolor("white")
    if title:
        fig.text(0.04, 0.925, title, fontsize=26, weight="bold", color=NAVY, va="center")
        fig.add_artist(plt.Line2D([0.04, 0.96], [0.875, 0.875], color=NAVY, lw=2))
    if caption:
        box(fig, 0.03, 0.018, 0.94, 0.115, LIGHT, r=0.01, z=1)
        lines = wrap_ja(caption, 44)
        fig.text(0.5, 0.075, "\n".join(lines[:3]), fontsize=18 if len(lines) <= 2 else 15.5,
                 color=INK, ha="center", va="center", linespacing=1.35)


def which(cues, t):
    """時刻 t に読まれている文の番号（文の間は直前の文）。"""
    k = 0
    for i, (s, _) in enumerate(cues):
        if t >= s:
            k = i
    return k


def prog(cues, i, t, j=None):
    """文 i の開始から文 j の終了（既定は文 i の終了）までの進み具合 0〜1。アニメーションの時間軸に使う。"""
    s = cues[i][0]
    e = cues[j if j is not None else i][1]
    return float(np.clip((t - s) / max(e - s, 1e-6), 0, 1))


def fade(cues, i, t, dur=0.5):
    """文 i が始まってから dur 秒で 0→1。項目を文に合わせて出すときに使う。"""
    return float(np.clip((t - cues[i][0]) / dur, 0, 1))


def panel(fig, rows, x=0.67, y0=0.17, y1=0.85):
    """右の説明欄。rows は (文字, dict(fontsize=..., color=..., weight=..., dy=次の行までの間隔))。"""
    box(fig, x, y0, 0.97 - x, y1 - y0, PANEL)
    y = y1 - 0.04
    for line, kw in rows:
        kw = dict(kw)
        dy = kw.pop("dy", 0.055)
        fig.text(x + 0.02, y, line, va="top", **kw)
        y -= dy


def side_panel(fig, _unused, rows, x=0.70, y0=0.17):
    """旧名（TS の作例が使う）。panel() と同じ。"""
    panel(fig, rows, x=x, y0=y0)


def clean(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.tick_params(labelsize=12)


def arrow(fig, p, q, color, lw=2.5, alpha=1):
    fig.add_artist(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=22, color=color, lw=lw,
                                   transform=fig.transFigure, alpha=alpha))


# ------------------------------------------------------------------ 音声
def tts(text, wav):
    """text を読み上げて wav（モノラル 16bit、SR Hz）に書き、長さ（秒）を返す。"""
    if TTS == "silent":
        n = sum(1.0 if ord(c) >= 0x2000 else 0.5 for c in text)
        a = np.zeros(int(n * 0.13 * SR), np.int16)
        with wave.open(wav, "w") as w:
            w.setnchannels(1), w.setsampwidth(2), w.setframerate(SR)
            w.writeframes(a.tobytes())
        return len(a) / SR
    raw = wav + ".raw.aiff" if TTS == "say" else wav + ".raw.wav"
    if TTS == "say":
        subprocess.run(["say", "-v", VOICE, "-r", str(RATE), "-o", raw, text], check=True)
    elif TTS == "espeak":
        subprocess.run(["espeak-ng", "-v", "ja", "-w", raw, text], check=True)
    else:
        raise ValueError(f"VIDEO_TTS={TTS} は使えない（say / espeak / silent）")
    subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-i", raw, "-ar", str(SR), "-ac", "1", wav], check=True)
    os.remove(raw)
    with wave.open(wav) as w:
        return w.getnframes() / SR


# ------------------------------------------------------------------ 動画
def no_data():
    return {}


class Video:
    """台本と描画関数から動画を作る。scenes[k] = dict(title=..., lines=[(字幕, 読み上げ), ...])、
    draws[k](fig, t, cues, data) が場面 k の時刻 t のコマを描く。build_data() は各場面の作業プロセスで 1 回呼ぶ。"""

    def __init__(self, scenes, draws, build_data=None, out="video.mp4", build_dir=None, workers=5):
        assert len(scenes) == len(draws)
        self.scenes, self.draws, self.build_data = scenes, draws, build_data or no_data
        self.out = os.path.abspath(out)
        self.build = build_dir or os.path.splitext(self.out)[0] + "_build"
        self.workers = workers
        os.makedirs(self.build, exist_ok=True)

    def synth(self, k):
        """場面 k の音声を作り、各文の (開始, 終了) 秒と全体の長さを返す。"""
        pieces, cues, t = [np.zeros(int(HEAD * SR), np.int16)], [], HEAD
        for i, (_, speech) in enumerate(self.scenes[k]["lines"]):
            wav = os.path.join(self.build, f"s{k}_{i}.wav")
            d = tts(speech, wav)
            with wave.open(wav) as w:
                a = np.frombuffer(w.readframes(w.getnframes()), np.int16)
            cues.append((t, t + d))
            pieces += [a, np.zeros(int(GAP * SR), np.int16)]
            t += d + GAP
        pieces.append(np.zeros(int(TAIL * SR), np.int16))
        audio = np.concatenate(pieces)
        with wave.open(os.path.join(self.build, f"scene{k}.wav"), "w") as w:
            w.setnchannels(1), w.setsampwidth(2), w.setframerate(SR)
            w.writeframes(audio.tobytes())
        return cues, len(audio) / SR

    def render(self, k):
        cues, dur = self.synth(k)
        data = self.build_data()
        fig = plt.figure(figsize=(W / 100, H / 100), dpi=100)
        out = os.path.join(self.build, f"scene{k}.mp4")
        wav = os.path.join(self.build, f"scene{k}.wav")
        # 音量は場面ごとに -16 LUFS にそろえる（say の声は場面によって大きさが違う）
        proc = subprocess.Popen([FFMPEG, "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgba",
                                 "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", wav,
                                 "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-preset", "medium",
                                 "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "44100",
                                 "-c:a", "aac", "-b:a", "160k", "-shortest", out], stdin=subprocess.PIPE)
        for f in range(int(math.ceil(dur * FPS))):
            self.draws[k](fig, f / FPS, cues, data)
            fig.canvas.draw()
            proc.stdin.write(bytes(fig.canvas.buffer_rgba()))
        proc.stdin.close()
        proc.wait()
        plt.close(fig)
        return k, dur

    def preview(self, k):
        """各文の終わりごろのコマを PNG にする（build_dir/preview/s{場面}_{文}.png）。"""
        cues, dur = self.synth(k)
        data = self.build_data()
        fig = plt.figure(figsize=(W / 100, H / 100), dpi=100)
        d = os.path.join(self.build, "preview")
        os.makedirs(d, exist_ok=True)
        for j, (_, e) in enumerate(cues):
            self.draws[k](fig, e - 0.05, cues, data)
            fig.savefig(os.path.join(d, f"s{k}_{j}.png"), dpi=50)
        plt.close(fig)
        return k, dur

    def concat(self):
        lst = os.path.join(self.build, "list.txt")
        with open(lst, "w") as f:
            for k in range(len(self.scenes)):
                f.write(f"file 'scene{k}.mp4'\n")
        subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst,
                        "-c", "copy", self.out], check=True)
        return self.out

    def main(self, args):
        job = self.preview if args and args[0] == "preview" else self.render
        args = args[1:] if args and args[0] == "preview" else args
        ks = [int(a) for a in args] or list(range(len(self.scenes)))
        with ProcessPoolExecutor(self.workers) as ex:
            for k, d in ex.map(job, ks):
                print(f"scene {k}: {d:.1f} s", flush=True)
        if job == self.render:
            print(self.concat())
