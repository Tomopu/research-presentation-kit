#!/usr/bin/env python3
"""LaTeX -> OMML (Office Math Markup) for PowerPoint. Stdlib only.

Equations produced by this module are real PowerPoint equation objects: click
one in PowerPoint and the equation editor opens. That is the whole point --
an equation pasted as a picture cannot be corrected five minutes before a talk.

    from omml import latex_to_omml, block_math, inline_math

    block_math(r"\\sum_{i=1}^{n} x_i = \\frac{a}{b}", size=24)   # display, centred
    inline_math(r"\\delta_{G-u}(x,y)", size=20)                  # inside a run

Variables are emitted as plain ASCII with i="1"; PowerPoint renders that
through Cambria Math exactly as it renders its own equations, and the result
stays editable as ordinary characters.

Supported: sub/superscripts, \\frac, \\sqrt, \\sum \\prod \\int with limits,
\\left...\\right and bare delimiters, \\begin{cases}, \\text \\mathrm \\mathbf
\\mathcal, greek, and the relation/operator symbols listed in SYMBOL. Anything
unrecognised is passed through as an upright literal rather than dropped, so a
gap shows up on the slide instead of silently vanishing.
"""

import re

MATH_FONT = 'panose="02040503050406030204" pitchFamily="18" charset="0"'

GREEK = {
    "alpha": "α", "beta": "β", "gamma": "γ", "delta": "δ", "epsilon": "ϵ",
    "varepsilon": "ε", "zeta": "ζ", "eta": "η", "theta": "θ", "vartheta": "ϑ",
    "iota": "ι", "kappa": "κ", "lambda": "λ", "mu": "μ", "nu": "ν", "xi": "ξ",
    "pi": "π", "rho": "ρ", "sigma": "σ", "tau": "τ", "upsilon": "υ",
    "phi": "ϕ", "varphi": "φ", "chi": "χ", "psi": "ψ", "omega": "ω",
    "Gamma": "Γ", "Delta": "Δ", "Theta": "Θ", "Lambda": "Λ", "Xi": "Ξ",
    "Pi": "Π", "Sigma": "Σ", "Upsilon": "Υ", "Phi": "Φ", "Psi": "Ψ",
    "Omega": "Ω",
}

SYMBOL = {
    "in": "∈", "notin": "∉", "ni": "∋", "subset": "⊂", "subseteq": "⊆",
    "subsetneq": "⊊", "supset": "⊃", "supseteq": "⊇", "cup": "∪", "cap": "∩",
    "setminus": "∖", "emptyset": "∅", "varnothing": "∅",
    "leq": "≤", "leqslant": "⩽", "geq": "≥", "geqslant": "⩾", "neq": "≠",
    "ne": "≠", "approx": "≈", "equiv": "≡", "sim": "∼", "simeq": "≃",
    "propto": "∝", "ll": "≪", "gg": "≫",
    "to": "→", "rightarrow": "→", "leftarrow": "←", "mapsto": "↦",
    "Rightarrow": "⇒", "Leftarrow": "⇐", "iff": "⟺", "Leftrightarrow": "⟺",
    "leftrightarrow": "↔", "Longrightarrow": "⟹", "Longleftarrow": "⟸",
    "implies": "⟹", "longrightarrow": "⟶",
    "times": "×", "cdot": "⋅", "div": "÷", "pm": "±", "mp": "∓",
    "cdots": "⋯", "ldots": "…", "dots": "…", "vdots": "⋮", "ddots": "⋱",
    "forall": "∀", "exists": "∃", "nexists": "∄", "neg": "¬", "lnot": "¬",
    "land": "∧", "lor": "∨", "infty": "∞", "partial": "∂", "nabla": "∇",
    "angle": "∠", "perp": "⊥", "parallel": "∥", "star": "⋆", "ast": "∗",
    "oplus": "⊕", "otimes": "⊗", "circ": "∘", "bullet": "∙",
    "mid": "∣", "vert": "|", "|": "‖", "backslash": "\\",
    "langle": "⟨", "rangle": "⟩", "lfloor": "⌊", "rfloor": "⌋",
    "lceil": "⌈", "rceil": "⌉", "prime": "′", "hbar": "ℏ", "ell": "ℓ",
    "Re": "ℜ", "Im": "ℑ", "aleph": "ℵ", "surd": "√", "therefore": "∴",
    "because": "∵", "qed": "∎", "blacksquare": "∎", "square": "□",
    "triangle": "△", "circ": "∘", "dagger": "†", "top": "⊤", "bot": "⊥",
    "%": "%", "&": "&", "#": "#", "$": "$", "_": "_", "{": "{", "}": "}",
}

LIMLOW = {"max", "min", "lim", "limsup", "liminf", "sup", "inf", "argmax", "argmin"}
FUNCTIONS = {"argmax", "argmin", "kl", 
    "max", "min", "sup", "inf", "lim", "limsup", "liminf", "arg", "log", "ln",
    "exp", "sin", "cos", "tan", "cot", "sec", "csc", "sinh", "cosh", "tanh",
    "det", "dim", "deg", "gcd", "ker", "Pr", "mod", "bmod",
}

FUNCTIONS_ALL = FUNCTIONS | {"arg\u2009max", "arg\u2009min"}

# \hat{x} などのアクセント（OMML の m:acc。結合文字で指定する）
ACCENT = {"hat": "\u0302", "widehat": "\u0302", "tilde": "\u0303", "widetilde": "\u0303",
          "bar": "\u0305", "vec": "\u20D7", "dot": "\u0307", "ddot": "\u0308", "check": "\u030C"}
DOUBLE = {c: chr(0x1D538 + i) for i, c in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ")}
DOUBLE.update({"C": "ℂ", "H": "ℍ", "N": "ℕ", "P": "ℙ", "Q": "ℚ", "R": "ℝ", "Z": "ℤ", "1": "𝟙"})
CALLIG = {"A": "𝒜", "B": "ℬ", "C": "𝒞", "D": "𝒟", "E": "ℰ", "F": "ℱ", "G": "𝒢", "H": "ℋ", "I": "ℐ",
          "J": "𝒥", "K": "𝒦", "L": "ℒ", "M": "ℳ", "N": "𝒩", "O": "𝒪", "P": "𝒫", "Q": "𝒬", "R": "ℛ",
          "S": "𝒮", "T": "𝒯", "U": "𝒰", "V": "𝒱", "W": "𝒲", "X": "𝒳", "Y": "𝒴", "Z": "𝒵"}

NARY = {"sum": "∑", "prod": "∏", "coprod": "∐", "int": "∫", "iint": "∬",
        "oint": "∮", "bigcup": "⋃", "bigcap": "⋂", "bigoplus": "⨁"}

SPACING = {"quad": "\u2003", "qquad": "\u2003\u2003", ",": "\u2009",
           ";": "\u2005", ":": "\u2005", "!": "", " ": " ", "\\": ""}

OPEN = {"(": "(", "[": "[", "\\{": "{", "\\lvert": "|", "\\lVert": "‖",
        "\\langle": "⟨", "\\lfloor": "⌊", "\\lceil": "⌈", "|": "|", ".": ""}
CLOSE = {")": ")", "]": "]", "\\}": "}", "\\rvert": "|", "\\rVert": "‖",
         "\\rangle": "⟩", "\\rfloor": "⌋", "\\rceil": "⌉", "|": "|", ".": ""}


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


# ------------------------------------------------------------------ tokenizer
TOKEN = re.compile(r"""
    \\begin\{(?P<envb>[a-z*]+)\}
  | \\end\{(?P<enve>[a-z*]+)\}
  | \\(?P<cmd>[A-Za-z]+)
  | \\(?P<esc>[^A-Za-z])
  | (?P<brace>[{}])
  | (?P<script>[_^])
  | (?P<amp>&)
  | (?P<num>[0-9]+(?:\.[0-9]+)?)
  | (?P<sp>\s+)
  | (?P<ch>.)
""", re.X)


def tokenize(src):
    out = []
    for m in TOKEN.finditer(src):
        k = m.lastgroup
        out.append((k, m.group(k)))
    return out


class Parser:
    def __init__(self, tokens, style=None):
        self.t = tokens
        self.i = 0
        self.style = style or {}

    def peek(self):
        return self.t[self.i] if self.i < len(self.t) else (None, None)

    def next(self):
        tok = self.peek()
        self.i += 1
        return tok

    # a "group": {...} or a single atom
    def group(self):
        k, v = self.peek()
        if k == "brace" and v == "{":
            self.next()
            nodes = self.sequence(stop="}")
            if self.peek()[0] == "brace":
                self.next()
            return nodes
        node = self.atom()
        return [node] if node else []

    def sequence(self, stop=None, stop_env=None):
        out = []
        while True:
            k, v = self.peek()
            if k is None:
                break
            if stop and k == "brace" and v == stop:
                break
            if stop_env and k == "enve":
                break
            if k == "amp" or (k == "esc" and v == "\\"):
                break
            node = self.atom()
            if node:
                out.append(node)
        return out

    def atom(self):
        k, v = self.next()
        if k is None:
            return None
        if k == "sp":
            return None
        if k == "num":
            return ("run", v, "up")
        if k == "script":
            return ("script", v)
        if k == "brace":
            if v == "{":
                self.i -= 1
                return ("grp", self.group())
            return None
        if k == "esc":
            if v in SPACING:
                return ("run", SPACING[v], "up") if SPACING[v] else None
            return ("run", SYMBOL.get(v, v), "up")
        if k == "envb":
            return self.environment(v)
        if k == "cmd":
            return self.command(v)
        if k == "ch":
            if v in "+-=<>/*,;:.!?()[]|":
                return ("run", v, "up")
            if v.isalpha():
                return ("run", v, "it")
            return ("run", v, "up")
        return ("run", v, "up")

    def command(self, name):
        if name in ("frac", "dfrac", "tfrac", "binom"):
            num, den = self.group(), self.group()
            return ("frac", num, den, name == "binom")
        if name == "sqrt":
            k, v = self.peek()
            deg = None
            if k == "ch" and v == "[":
                self.next()
                deg = []
                while self.peek()[0] is not None and self.peek()[1] != "]":
                    n = self.atom()
                    if n:
                        deg.append(n)
                self.next()
            return ("sqrt", deg, self.group())
        if name in NARY:
            return ("nary", NARY[name], name == "int")
        if name in GREEK:
            return ("run", GREEK[name], "it" if name[0].islower() else "up")
        if name in FUNCTIONS:
            return ("run", name, "up")
        if name in ("text", "textrm", "mathrm", "mbox", "operatorname"):
            return ("txt", self.raw_group(), False)
        if name in ("mathbf", "bm", "boldsymbol", "textbf"):
            return ("style", self.group(), "bd")
        if name in ("mathcal", "mathscr"):
            return ("style", self.group(), "cal")
        if name in ("mathbb",):
            return ("style", self.group(), "bb")
        if name in ACCENT:
            return ("acc", ACCENT[name], self.group())
        if name in ("overline",):
            return ("bar", "top", self.group())
        if name in ("underline",):
            return ("bar", "bot", self.group())
        if name in ("underbrace", "overbrace"):
            return ("brace", name, self.group())
        if name in ("left",):
            return self.delimited()
        if name in ("right",):
            return None
        if name in ("big", "Big", "bigg", "Bigg", "biggl", "biggr",
                    "displaystyle", "textstyle", "limits", "nolimits"):
            return None
        if name in SYMBOL:
            return ("run", SYMBOL[name], "up")
        if name in SPACING:
            return ("run", SPACING[name], "up") if SPACING[name] else None
        # unknown: keep it visible rather than dropping it
        return ("run", name, "up")

    def raw_group(self):
        """Collect a {...} verbatim, for \\text{...}."""
        k, v = self.peek()
        if not (k == "brace" and v == "{"):
            _, val = self.next()
            return val or ""
        self.next()
        depth, buf = 1, []
        while self.i < len(self.t):
            k, v = self.next()
            if k == "brace":
                depth += 1 if v == "{" else -1
                if depth == 0:
                    break
                buf.append(v)
            elif k == "cmd":
                buf.append(SYMBOL.get(v, GREEK.get(v, v)))
            elif k == "esc":
                buf.append(SPACING.get(v, SYMBOL.get(v, v)))
            else:
                buf.append(v)
        return "".join(buf)

    def delimited(self):
        op = self.read_delim(OPEN)
        body = self.sequence_until_right()
        cl = self.read_delim(CLOSE)
        return ("delim", op, cl, body)

    def read_delim(self, table):
        k, v = self.peek()
        if k == "cmd" and ("\\" + v) in table:
            self.next()
            return table["\\" + v]
        if k == "esc" and ("\\" + v) in table:
            self.next()
            return table["\\" + v]
        if k == "ch" and v in table:
            self.next()
            return table[v]
        return ""

    def sequence_until_right(self):
        # 入れ子の \left...\right は atom() → delimited() が対応する \right まで丸ごと読むので、
        # ここで最初に出会う \right が自分の閉じ記号になる（深さを数えると二重に数えてしまう）。
        out = []
        while self.i < len(self.t):
            k, v = self.peek()
            if k == "cmd" and v == "right":
                self.next()
                break
            node = self.atom()
            if node:
                out.append(node)
        return out

    def environment(self, env):
        rows, row, cell = [], [], []
        while self.i < len(self.t):
            k, v = self.peek()
            if k == "enve":
                self.next()
                break
            if k == "amp":
                self.next()
                row.append(cell)
                cell = []
                continue
            if k == "esc" and v == "\\":
                self.next()
                row.append(cell)
                rows.append(row)
                row, cell = [], []
                continue
            node = self.atom()
            if node:
                cell.append(node)
        if cell or row:
            row.append(cell)
            rows.append(row)
        return ("env", env, rows)


# -------------------------------------------------------------------- emitter
def _rpr(size, color, italic, bold, math=True):
    return ('<a:rPr kumimoji="1" lang="en-US" altLang="ja-JP" sz="%d" b="%d" '
            'i="%d" smtClean="0"><a:solidFill><a:srgbClr val="%s"/></a:solidFill>'
            '<a:latin typeface="%s" %s/></a:rPr>'
            % (size * 100, 1 if bold else 0, 1 if italic else 0, color,
               "Cambria Math" if math else "Segoe UI", MATH_FONT if math else ""))


def _ctrl(size, color):
    return "<m:ctrlPr>%s</m:ctrlPr>" % _rpr(size, color, True, False)


class Emitter:
    def __init__(self, size, color):
        self.size, self.color = size, color

    def run(self, text, mode):
        """One maths run.

        Inside <m:oMath> the renderer italicises Latin letters on its own, so
        `i="0"` on the drawing properties is not enough to make a function name
        upright -- that needs OMML's own <m:sty m:val="p">. Without it `\\max`
        comes out looking like the product of m, a and x.
        """
        italic = mode == "it"
        bold = mode == "bd"
        if text == "-":
            text = "−"
        mpr = ""
        if mode == "tx":
            mpr = "<m:rPr><m:nor/></m:rPr>"
        elif mode in ("up", "bd") and any(c.isalpha() for c in text):
            mpr = '<m:rPr><m:sty m:val="%s"/></m:rPr>' % ("b" if bold else "p")
        return "<m:r>%s%s<m:t>%s</m:t></m:r>" % (
            mpr, _rpr(self.size, self.color, italic, bold), esc(text))

    # Σ の本体・関数の引数を切る記号（括弧の外にあるときだけ）
    STOP = {"+", "-", "−", "=", "≤", "≥", "<", ">", ",", "≈", "∈", "→", "≠", "∼", ":", ";",
            "\u2003", "\u2003\u2003", "∣", "⟹", "⇒"}

    def _take(self, nodes, i):
        """nodes[i] とその後ろの _ ^ を 1 つの項として取り出す。(base, sub, sup, 次の位置)"""
        base, i = nodes[i], i + 1
        sub = sup = None
        while i < len(nodes) and nodes[i][0] == "script":
            which = nodes[i][1]
            arg = nodes[i + 1] if i + 1 < len(nodes) else ("run", "", "up")
            i += 2
            if which == "_":
                sub = arg
            else:
                sup = arg
        return base, sub, sup, i

    def _operand(self, nodes, i):
        """Σ の本体：次の二項演算子・関係記号（括弧の外）までを取る。"""
        depth, j = 0, i
        while j < len(nodes):
            n = nodes[j]
            if n[0] == "run":
                t = n[1]
                if t in ("(", "[", "{", "⟨", "⌈", "⌊"):
                    depth += 1
                elif t in (")", "]", "}", "⟩", "⌉", "⌋"):
                    if depth == 0:
                        break
                    depth -= 1
                elif depth == 0 and t in self.STOP:
                    break
            if n[0] == "nary" and depth == 0 and j > i:
                break
            j += 1
        return nodes[i:j], j

    def _arg(self, nodes, i):
        """関数の引数：直後の 1 項（とその添字）。\\log\\log t のように関数が続くときは入れ子にする。
        直後が裸の括弧なら、対応する閉じ括弧まで。"""
        if i >= len(nodes):
            return [], i
        n = nodes[i]
        if n[0] == "run" and n[1] in ("(", "[", "{"):
            close = {"(": ")", "[": "]", "{": "}"}[n[1]]
            depth, j = 0, i
            while j < len(nodes):
                t = nodes[j]
                if t[0] == "run" and t[1] == n[1]:
                    depth += 1
                elif t[0] == "run" and t[1] == close:
                    depth -= 1
                    if depth == 0:
                        j += 1
                        break
                j += 1
            return nodes[i:j], j
        if n[0] == "run" and n[2] == "up" and n[1] in FUNCTIONS_ALL:
            base, sub, sup, j = self._take(nodes, i)
            inner, k = self._arg(nodes, j)
            return nodes[i:k], k
        if n[0] == "run" and n[1] in self.STOP:
            return [], i
        base, sub, sup, j = self._take(nodes, i)
        # 1 文字の変数に続く (…) は引数ごと取る（例 \\log f(t)）
        return nodes[i:j], j

    def nodes(self, nodes):
        out, i = [], 0
        while i < len(nodes):
            n = nodes[i]
            if n[0] == "run" and n[1] == "arg" and i + 1 < len(nodes) and nodes[i + 1][0] == "run" \
                    and nodes[i + 1][1] in ("max", "min"):
                nodes = nodes[:i] + [("run", "arg\u2009" + nodes[i + 1][1], "up")] + nodes[i + 2:]
                n = nodes[i]
            if n[0] == "nary":
                base, sub, sup, j = self._take(nodes, i)
                body, k = self._operand(nodes, j)
                out.append(self.nary(base, sub, sup, body))
                i = k
                continue
            if n[0] == "run" and n[2] == "up" and n[1] in FUNCTIONS_ALL:
                base, sub, sup, j = self._take(nodes, i)
                arg, k = self._arg(nodes, j)
                out.append(self.func(base, sub, sup, arg))
                i = k
                continue
            # gather trailing _ / ^ into a script node
            if i + 1 < len(nodes) and nodes[i + 1][0] == "script":
                base, sub, sup, i = self._take(nodes, i)
                out.append(self.script(base, sub, sup))
                continue
            out.append(self.node(n))
            i += 1
        return "".join(out)

    def nary(self, base, sub, sup, body):
        return ('<m:nary><m:naryPr><m:chr m:val="%s"/><m:limLoc m:val="%s"/>'
                '%s%s%s</m:naryPr><m:sub>%s</m:sub><m:sup>%s</m:sup>'
                '<m:e>%s</m:e></m:nary>'
                % (esc(base[1]), "subSup" if base[2] else "undOvr",
                   "" if sub else '<m:subHide m:val="1"/>',
                   "" if sup else '<m:supHide m:val="1"/>',
                   _ctrl(self.size, self.color),
                   self.nodes([sub]) if sub else "",
                   self.nodes([sup]) if sup else "",
                   self.nodes(body)))

    def func(self, base, sub, sup, arg):
        """log, ln, max, lim sup などを m:func にする（関数名と引数の間に正しい空きが入る）。
        max/min/lim の添字は真下（m:limLow）、log^2 の肩は関数名に付ける。"""
        name = self.run(base[1].replace("limsup", "lim\u2009sup").replace("liminf", "lim\u2009inf"), "up")
        if sub is not None and base[1].replace("arg\u2009", "") in LIMLOW:
            name = ('<m:limLow><m:limLowPr>%s</m:limLowPr><m:e>%s</m:e><m:lim>%s</m:lim></m:limLow>'
                    % (_ctrl(self.size, self.color), name, self.nodes([sub])))
        elif sub is not None or sup is not None:
            if sub is not None and sup is not None:
                name = ('<m:sSubSup><m:sSubSupPr>%s</m:sSubSupPr><m:e>%s</m:e><m:sub>%s</m:sub>'
                        '<m:sup>%s</m:sup></m:sSubSup>' % (_ctrl(self.size, self.color), name,
                                                           self.nodes([sub]), self.nodes([sup])))
            elif sup is not None:
                name = ('<m:sSup><m:sSupPr>%s</m:sSupPr><m:e>%s</m:e><m:sup>%s</m:sup></m:sSup>'
                        % (_ctrl(self.size, self.color), name, self.nodes([sup])))
            else:
                name = ('<m:sSub><m:sSubPr>%s</m:sSubPr><m:e>%s</m:e><m:sub>%s</m:sub></m:sSub>'
                        % (_ctrl(self.size, self.color), name, self.nodes([sub])))
        if not arg:
            return name
        return ('<m:func><m:funcPr>%s</m:funcPr><m:fName>%s</m:fName><m:e>%s</m:e></m:func>'
                % (_ctrl(self.size, self.color), name, self.nodes(arg)))

    def node(self, n):
        kind = n[0]
        if kind == "run":
            return self.run(n[1], n[2])
        if kind == "grp":
            return self.nodes(n[1])
        if kind == "txt":
            return self.run(n[1], "tx")
        if kind == "style":
            mode = {"bd": "bd", "cal": "up", "bb": "up"}[n[2]]
            table = {"bb": DOUBLE, "cal": CALLIG}.get(n[2], {})
            return "".join(self.node(("run", "".join(table.get(ch, ch) for ch in c[1]), mode))
                           if c[0] == "run" else self.node(c) for c in n[1])
        if kind == "acc":
            return ('<m:acc><m:accPr><m:chr m:val="%s"/>%s</m:accPr><m:e>%s</m:e></m:acc>'
                    % (n[1], _ctrl(self.size, self.color), self.nodes(n[2])))
        if kind == "bar":
            return ('<m:bar><m:barPr><m:pos m:val="%s"/>%s</m:barPr><m:e>%s</m:e></m:bar>'
                    % (n[1], _ctrl(self.size, self.color), self.nodes(n[2])))
        if kind == "brace":
            under = n[1] == "underbrace"
            return ('<m:groupChr><m:groupChrPr><m:chr m:val="%s"/><m:pos m:val="%s"/>'
                    '<m:vertJc m:val="%s"/>%s</m:groupChrPr><m:e>%s</m:e></m:groupChr>'
                    % ("⏟" if under else "⏞", "bot" if under else "top", "top" if under else "bot",
                       _ctrl(self.size, self.color), self.nodes(n[2])))
        if kind == "frac":
            return ('<m:f><m:fPr>%s%s</m:fPr><m:num>%s</m:num><m:den>%s</m:den></m:f>'
                    % ('<m:type m:val="noBar"/>' if n[3] else "",
                       _ctrl(self.size, self.color),
                       self.nodes(n[1]), self.nodes(n[2])))
        if kind == "sqrt":
            if n[1]:
                return ('<m:rad><m:radPr>%s</m:radPr><m:deg>%s</m:deg>'
                        '<m:e>%s</m:e></m:rad>'
                        % (_ctrl(self.size, self.color),
                           self.nodes(n[1]), self.nodes(n[2])))
            return ('<m:rad><m:radPr><m:degHide m:val="1"/>%s</m:radPr>'
                    '<m:deg/><m:e>%s</m:e></m:rad>'
                    % (_ctrl(self.size, self.color), self.nodes(n[2])))
        if kind == "delim":
            return ('<m:d><m:dPr><m:begChr m:val="%s"/><m:endChr m:val="%s"/>%s'
                    '</m:dPr><m:e>%s</m:e></m:d>'
                    % (esc(n[1]), esc(n[2]), _ctrl(self.size, self.color),
                       self.nodes(n[3])))
        if kind == "nary":
            return self.run(n[1], "up")
        if kind == "env":
            return self.env(n[1], n[2])
        if kind == "script":
            return ""
        return ""

    def script(self, base, sub, sup):
        if base[0] == "nary":
            # Sums and products carry their limits above and below; integrals
            # keep them beside the sign, which is the usual typographic rule.
            return ('<m:nary><m:naryPr><m:chr m:val="%s"/><m:limLoc m:val="%s"/>'
                    '%s%s</m:naryPr><m:sub>%s</m:sub><m:sup>%s</m:sup>'
                    '<m:e></m:e></m:nary>'
                    % (esc(base[1]), "subSup" if base[2] else "undOvr",
                       "" if sub else '<m:subHide m:val="1"/>',
                       "" if sup else '<m:supHide m:val="1"/>',
                       self.nodes([sub]) if sub else "",
                       self.nodes([sup]) if sup else "",
                       ))
        b = self.nodes([base])
        # 下かっこの注記、max/min/lim の下の添字は真下に置く（m:limLow）
        if sub is not None and sup is None and (
                base[0] == "brace" or (base[0] == "run" and base[1] in ("max", "min", "lim", "sup", "inf", "argmax", "argmin"))):
            return ('<m:limLow><m:limLowPr>%s</m:limLowPr><m:e>%s</m:e><m:lim>%s</m:lim></m:limLow>'
                    % (_ctrl(self.size, self.color), b, self.nodes([sub])))
        if sub is not None and sup is not None:
            return ('<m:sSubSup><m:sSubSupPr>%s</m:sSubSupPr><m:e>%s</m:e>'
                    '<m:sub>%s</m:sub><m:sup>%s</m:sup></m:sSubSup>'
                    % (_ctrl(self.size, self.color), b,
                       self.nodes([sub]), self.nodes([sup])))
        if sub is not None:
            return ('<m:sSub><m:sSubPr>%s</m:sSubPr><m:e>%s</m:e>'
                    '<m:sub>%s</m:sub></m:sSub>'
                    % (_ctrl(self.size, self.color), b, self.nodes([sub])))
        return ('<m:sSup><m:sSupPr>%s</m:sSupPr><m:e>%s</m:e>'
                '<m:sup>%s</m:sup></m:sSup>'
                % (_ctrl(self.size, self.color), b, self.nodes([sup])))

    def env(self, name, rows):
        if name.startswith("cases"):
            # `&` separates the value from its condition. OMML has no column
            # alignment inside a cases brace, so the columns are joined with an
            # em space -- without it the condition runs straight into the value.
            gap = ("run", " ", "up")
            body = "".join(
                "<m:e>%s</m:e>" % self.nodes(
                    [n for k, cell in enumerate(row)
                     for n in (([gap] + cell) if k else cell)])
                for row in rows)
            return ('<m:d><m:dPr><m:begChr m:val="{"/><m:endChr m:val=""/>%s</m:dPr>'
                    '<m:e><m:eqArr><m:eqArrPr>%s</m:eqArrPr>%s</m:eqArr></m:e></m:d>'
                    % (_ctrl(self.size, self.color), _ctrl(self.size, self.color),
                       body))
        if name.startswith(("align", "gather", "split")):
            body = "".join("<m:e>%s</m:e>" % self.nodes(
                [c for cell in row for c in cell]) for row in rows)
            return ('<m:eqArr><m:eqArrPr>%s</m:eqArrPr>%s</m:eqArr>'
                    % (_ctrl(self.size, self.color), body))
        cols = max((len(r) for r in rows), default=1)
        mr = "".join("<m:mr>%s</m:mr>" % "".join(
            "<m:e>%s</m:e>" % self.nodes(c) for c in row) for row in rows)
        beg, end = ("[", "]") if name.startswith("b") else (
            ("(", ")") if name.startswith("p") else ("", ""))
        m = ('<m:m><m:mPr><m:mcs><m:mc><m:mcPr><m:count m:val="%d"/>'
             '<m:mcJc m:val="center"/></m:mcPr></m:mc></m:mcs>%s</m:mPr>%s</m:m>'
             % (cols, _ctrl(self.size, self.color), mr))
        if beg:
            return ('<m:d><m:dPr><m:begChr m:val="%s"/><m:endChr m:val="%s"/>%s'
                    '</m:dPr><m:e>%s</m:e></m:d>'
                    % (beg, end, _ctrl(self.size, self.color), m))
        return m


def latex_to_omml(src, size=24, color="0D114A"):
    """Convert a LaTeX math body to the inner content of <m:oMath>."""
    p = Parser(tokenize(src))
    nodes = p.sequence()
    return Emitter(size, color).nodes(nodes)


M_NS = 'xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"'
# The a14 prefix must be declared on the element itself. The slide root does not
# carry it (PowerPoint declares it on each <mc:AlternateContent> instead), and an
# undeclared prefix makes the element unparseable -- readers drop the equation
# and leave a blank gap on the slide rather than reporting an error.
A14_NS = 'xmlns:a14="http://schemas.microsoft.com/office/drawing/2010/main"'


def block_math(src, size=24, color="0D114A", align="centerGroup"):
    """A display equation: the full <a:p> content for a maths-only paragraph."""
    return ('<a14:m %s><m:oMathPara %s><m:oMathParaPr><m:jc m:val="%s"/>'
            '</m:oMathParaPr><m:oMath %s>%s</m:oMath></m:oMathPara></a14:m>'
            % (A14_NS, M_NS, align, M_NS, latex_to_omml(src, size, color)))


def inline_math(src, size=20, color="0D114A"):
    """An equation sitting inside a line of prose."""
    return '<a14:m %s><m:oMath %s>%s</m:oMath></a14:m>' % (
        A14_NS, M_NS, latex_to_omml(src, size, color))


if __name__ == "__main__":
    import sys
    for s in sys.argv[1:]:
        print(latex_to_omml(s)[:4000])
