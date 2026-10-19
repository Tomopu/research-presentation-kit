"""字幕（表示用の文）から読み上げ用の文を作る。

    from yomi import yomi, display
    yomi("UCB1 の上乗せは $\\sqrt{2\\ln t / N_k}$ です。")   # → 「ユーシービー・ワンの上乗せは、ルート、2 ログ ティー わる エヌ ケー、です。」
    display("{R-SKL|アール・エス・ケー・エル} は…")             # → 「R-SKL は…」（画面に出す文）

- `$...$` の中の LaTeX は、数式の読み方の規則で日本語にする（分数は「B 分の A」、上付きは「の 2 乗」、
  下付きは記号の後に読む、ギリシャ文字はカタカナ、\\hat は「ハット」など）
- `{表記|よみ}` はその場だけの読みの指定（画面には表記、声にはよみ）
- 数式の外の専門用語は lexicon.tsv（と、呼び出し側の追加の辞書）で置き換える。長い語から先に当てる
"""
from __future__ import annotations

import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))

GREEK = {"alpha": "アルファ", "beta": "ベータ", "gamma": "ガンマ", "delta": "デルタ", "epsilon": "イプシロン",
         "varepsilon": "イプシロン", "zeta": "ゼータ", "eta": "イータ", "theta": "シータ", "vartheta": "シータ",
         "iota": "イオタ", "kappa": "カッパ", "lambda": "ラムダ", "mu": "ミュー", "nu": "ニュー", "xi": "グザイ",
         "pi": "パイ", "rho": "ロー", "sigma": "シグマ", "tau": "タウ", "upsilon": "ウプシロン", "phi": "ファイ",
         "varphi": "ファイ", "chi": "カイ", "psi": "プサイ", "omega": "オメガ", "Gamma": "ガンマ", "Delta": "デルタ",
         "Theta": "シータ", "Lambda": "ラムダ", "Xi": "グザイ", "Pi": "パイ", "Sigma": "シグマ", "Phi": "ファイ",
         "Psi": "プサイ", "Omega": "オメガ"}
LETTER = dict(zip("abcdefghijklmnopqrstuvwxyz",
                  ["エー", "ビー", "シー", "ディー", "イー", "エフ", "ジー", "エイチ", "アイ", "ジェー", "ケー", "エル", "エム",
                   "エヌ", "オー", "ピー", "キュー", "アール", "エス", "ティー", "ユー", "ブイ", "ダブリュー", "エックス",
                   "ワイ", "ゼット"]))
FUNC = {"log": "ログ", "ln": "ログ", "exp": "エクスポネンシャル", "max": "マックス", "min": "ミン", "arg": "アーグ",
        "sin": "サイン", "cos": "コサイン", "tan": "タンジェント", "lim": "リミット", "liminf": "リムインフ",
        "limsup": "リムスープ", "inf": "インフ", "sup": "スープ", "Pr": "確率", "det": "デターミナント",
        "argmax": "アーグマックス", "argmin": "アーグミン"}
SYM = {"le": "以下", "leq": "以下", "ge": "以上", "geq": "以上", "neq": "ノットイコール", "approx": "ほぼ",
       "pm": "プラスマイナス", "times": "かける", "cdot": "かける", "in": "の要素", "notin": "の要素でない",
       "sim": "、は、次に従う、", "infty": "無限大", "to": "から", "rightarrow": "から", "mapsto": "を移す",
       "sum": "和", "prod": "積", "int": "積分", "partial": "パーシャル", "nabla": "ナブラ",
       "dots": "から", "ldots": "から", "cdots": "から", "lesssim": "以下", "gtrsim": "以上", "propto": "に比例",
       "forall": "すべての", "exists": "ある", "cup": "和集合", "cap": "共通部分", "subset": "部分集合",
       "mid": "ただし", "colon": "ただし", "lVert": "ノルム", "rVert": "", "|": "ノルム"}
SPACE = {",", ";", ":", "!", "quad", "qquad", " ", "left", "right", "big", "Big", "bigl", "bigr", "Bigl", "Bigr",
         "displaystyle", "textstyle", "{", "}", "langle", "rangle", "lfloor", "rfloor", "lceil", "rceil"}
ACCENT = {"hat": "ハット", "widehat": "ハット", "bar": "バー", "overline": "バー", "tilde": "チルダ",
          "widetilde": "チルダ", "dot": "ドット", "vec": "ベクトル"}
CHAR = {"=": "イコール", "+": "プラス", "-": "マイナス", "<": "より小さい", ">": "より大きい", "/": "わる",
        ",": "、", "(": " ", ")": " ", "[": " ", "]": " ", "|": "、", "!": "の階乗", "'": "プライム", "*": "スター",
        "−": "マイナス", "×": "かける", "≤": "以下", "≥": "以上", ":": "ただし"}
WORD = {"Beta": "ベータ", "KL": "ケーエル", "Bernoulli": "ベルヌーイ", "Bin": "二項", "Unif": "一様", "Var": "分散",
        "Cov": "共分散", "Regret": "リグレット", "UCB": "ユーシービー", "LCB": "エルシービー", "d": "ディー"}


def _word(a):
    """\\mathrm{...} の中身：辞書にある語はその読み、3 文字以下の大文字は 1 文字ずつ、それ以外は数式として読む。"""
    if a in WORD:
        return WORD[a]
    if re.fullmatch(r"[A-Z]{1,3}", a):
        return "".join(LETTER[ch.lower()] for ch in a)
    if re.fullmatch(r"[A-Za-z]{4,}", a):
        return a
    return math_yomi(a)


def _group(s, i):
    """s[i] から始まる 1 引数（{...} か 1 文字か \\命令）を取り出し、(中身, 次の位置) を返す。"""
    while i < len(s) and s[i] == " ":
        i += 1
    if i >= len(s):
        return "", i
    if s[i] == "{":
        depth, j = 1, i + 1
        while j < len(s) and depth:
            depth += {"{": 1, "}": -1}.get(s[j], 0)
            j += 1
        return s[i + 1:j - 1], j
    if s[i] == "\\":
        m = re.match(r"\\([A-Za-z]+|.)", s[i:])
        return m.group(0), i + len(m.group(0))
    return s[i], i + 1


def math_yomi(s):
    """LaTeX の数式 1 つを日本語の読みにする。"""
    out, i = [], 0
    while i < len(s):
        c = s[i]
        if c == "\\":
            m = re.match(r"\\([A-Za-z]+|.)", s[i:])
            name, i = m.group(1), i + len(m.group(0))
            if name == "frac" or name == "dfrac" or name == "tfrac":
                a, i = _group(s, i)
                b, i = _group(s, i)
                out.append(f"{math_yomi(b)}ぶんの{math_yomi(a)}")
            elif name == "sqrt":
                a, i = _group(s, i)
                out.append(f"ルート {math_yomi(a)}")
            elif name in ACCENT:
                a, i = _group(s, i)
                out.append(f"{math_yomi(a)}{ACCENT[name]}")
            elif name in ("mathrm", "text", "textrm", "operatorname", "mathit", "mathsf", "mathbf", "boldsymbol", "bm"):
                a, i = _group(s, i)
                out.append(_word(a) if name != "text" else a)
            elif name == "mathbb":
                a, i = _group(s, i)
                out.append({"E": "期待値", "R": "実数", "N": "自然数", "1": "指示関数", "P": "確率"}.get(a, a))
            elif name == "mathcal":
                a, i = _group(s, i)
                out.append({"N": "正規分布"}.get(a, LETTER.get(a.lower(), a)))
            elif name in GREEK:
                out.append(GREEK[name])
            elif name in FUNC:
                out.append(FUNC[name])
            elif name in SYM:
                out.append(SYM[name])
            elif name in SPACE or name in ("{", "}"):
                out.append(" ")
            else:
                out.append(name)
        elif c == "^":
            a, i = _group(s, i + 1)
            r = math_yomi(a).strip()
            out.append({"2": "の2乗", "3": "の3乗", "*": "スター", "\\top": "転置", "T": "転置"}.get(a.strip(), f"の{r}乗"))
        elif c == "_":
            a, i = _group(s, i + 1)
            out.append(" " + math_yomi(a))
        elif c == "O" and s[i + 1:i + 2] == "(":
            out.append("オーダー")
            i += 1
        elif c.isalpha() and c.isascii():
            out.append(LETTER.get(c.lower(), c) if not (c.isupper() and c in "KMNT") else
                       {"K": "ケー", "M": "エム", "N": "エヌ", "T": "ティー"}[c])
            i += 1
        elif c.isdigit() or c == ".":
            m = re.match(r"[0-9.]+", s[i:])
            out.append(m.group(0))
            i += len(m.group(0))
        else:
            out.append(CHAR.get(c, "" if c in "{} " else c))
            i += 1
    txt = " ".join(t for t in out if t is not None)
    return re.sub(r"\s+", " ", txt).strip()


def load_lexicon(extra=None):
    """lexicon.tsv（表記<TAB>よみ）を読み、extra（dict）で上書きする。"""
    lex = {}
    path = os.path.join(HERE, "lexicon.tsv")
    if os.path.exists(path):
        for line in open(path, encoding="utf-8"):
            line = line.rstrip("\n")
            if line and not line.startswith("#") and "\t" in line:
                k, v = line.split("\t", 1)
                lex[k] = v
    lex.update(extra or {})
    return lex


_RUBY = re.compile(r"\{([^{}|]+)\|([^{}]+)\}")


def display(text):
    """画面に出す文：{表記|よみ} を表記にする。"""
    return _RUBY.sub(lambda m: m.group(1), text)


def yomi(text, lexicon=None, pause="、"):
    """読み上げ用の文：{表記|よみ} はよみ、$...$ は数式の読み、残りは辞書で置き換える。

    pause は数式の前に入れる間（say なら "[[slnc 250]]"）。**数式の後には間を入れない。**
    数式の後で区切ると、続く「です」「になる」などが 1 語として読み直され、「でぇ〜す」と伸びるため
    （2026-10-19 に音声の波形で確かめた：間の後の「です」は 0.33 秒、つなげると約 0.15 秒）。"""
    lex = load_lexicon(lexicon) if not isinstance(lexicon, dict) or "__loaded__" not in lexicon else lexicon
    text = _RUBY.sub(lambda m: "\x00" + m.group(2) + "\x01", text)       # 読みを指定した所は辞書を当てない
    parts = re.split(r"(\$[^$]+\$|\x00[^\x01]*\x01)", text)
    keys = sorted(lex, key=len, reverse=True)
    pat = re.compile("|".join(re.escape(k) for k in keys)) if keys else None
    out = []
    for p in parts:
        if p.startswith("$") and p.endswith("$") and len(p) > 1:
            r = math_yomi(p[1:-1]).strip("、 ")
            # 1〜2 語の短い記号（「腕 k」の k など）の前には間を入れない
            out.append(("\x02" if len(r.split()) >= 3 or len(r) >= 8 else "") + r)
        elif p.startswith("\x00"):
            out.append(p[1:-1])
        elif pat:
            out.append(pat.sub(lambda m: lex[m.group(0)], p))
        else:
            out.append(p)
    s = "".join(out)
    s = re.sub(r"\s+", " ", s)
    # 日本語（かな・漢字・句読点）の前後の空白は消す。数式の語どうしの空白（短い間）は残す
    jp = r"[\u3040-\u309f\u4e00-\u9fff、。，．（）「」]"
    s = re.sub(rf"\s+(?={jp})|(?<={jp})\s+", "", s)
    s = re.sub(r"、+", "、", s)
    s = re.sub(r"、([。、])", r"\1", s)
    s = re.sub(r"。、", "。", s)
    # 数式の前の間：文頭なら入れない、直前の読点は間に置き換える
    s = re.sub(r"^\x02", "", s)
    s = re.sub(r"(?<=[。])\x02", "", s)
    s = re.sub(r"、?\x02", pause, s)
    return s.strip("、 ").strip()


if __name__ == "__main__":
    import sys
    for line in sys.argv[1:] or ["UCB1 の上乗せは $\\sqrt{2\\ln t / N_k}$ です。",
                                 "$U_k(t) = \\max\\{q : N_k \\mathrm{KL}(\\hat\\mu_k, q) \\le \\ln t\\}$",
                                 "$\\theta_{m,k}(t) \\sim \\mathrm{Beta}(1 + S_{m,k}, 1 + N_{m,k} - S_{m,k})$",
                                 "後悔は $O(\\log T)$ で、$\\frac{8 \\ln T}{\\Delta_k^2}$ 回まで。",
                                 "{R-SKL|アール・エス・ケー・エル} は KL-UCB の index に $Z/t$ を足す。"]:
        print(display(line), "\n  →", yomi(line))
