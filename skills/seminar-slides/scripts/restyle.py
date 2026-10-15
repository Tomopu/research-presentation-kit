#!/usr/bin/env python3
"""出来上がった .pptx の「色・表のデザイン・切り替え効果」だけを書き換える後処理。

    python restyle.py in.pptx out.pptx

図形の位置・大きさ・文字の大きさには触れない（本人が手で直した資料にも使える）。

1. 色の置き換え（RECOLOR）：リード帯・箱の淡い面などの色を本人の指定色にする
2. 表：泉知成_修論中間発表スライド_完成.pptx の表のデザインにする
   - 見出し行：塗りなし、文字は紺 0D114A の太字、下に紺 2pt の線
   - 本文の行：塗りなし（強調の黄色などは残す）、文字は 404040、行の上下に BFBFBF 0.75pt の線
   - 縦線なし
3. 切り替え効果：スライド・レイアウト・マスターの <p:transition>（変形 morph を含む）をすべて外す
"""
import re
import sys
import zipfile

from lxml import etree

A = "http://schemas.openxmlformats.org/drawingml/2006/main"
P = "http://schemas.openxmlformats.org/presentationml/2006/main"
MC = "http://schemas.openxmlformats.org/markup-compatibility/2006"
M = "http://schemas.openxmlformats.org/officeDocument/2006/math"

# 2026-10-14 本人の指定
RECOLOR = {"EEF1F9": "D9DBE8",   # リード帯・角丸の箱の淡い紺
           "FFF1C8": "F6EAC3",   # 薄い黄色
           "FDEDEC": "FFCEC6",   # 薄い赤
           "FDECEC": "FFCEC6"}

NAVY, BODY_TXT, GRID = "0D114A", "404040", "BFBFBF"
TABLE_STYLE = "{2D5ABB26-0587-4C30-8999-92F81FD0307C}"   # No Style, No Grid（完成版と同じ）
KEEP_FILLS = {"F6EAC3", "FFF1C8", "FFF3C4", "FFCEC6", "FDECEC", "FDEDEC", "E4F6DD", "D1E1EA"}   # 強調の塗りは残す


def q(ns, tag):
    return "{%s}%s" % (ns, tag)


def recolor(xml):
    for old, new in RECOLOR.items():
        xml = re.sub(r'val="%s"' % old, 'val="%s"' % new, xml, flags=re.I)
    return xml


def strip_transitions(xml):
    # PowerPoint は変形を mc:AlternateContent（Choice: p159:morph / Fallback: fade）で包んで書く
    xml = re.sub(r"<mc:AlternateContent[^>]*>\s*<mc:Choice[^>]*>\s*<p:transition.*?</mc:AlternateContent>", "", xml, flags=re.S)
    xml = re.sub(r"<p:transition\b[^>]*/>", "", xml)
    xml = re.sub(r"<p:transition\b.*?</p:transition>", "", xml, flags=re.S)
    return xml


def _line(tag, w=None, color=None):
    el = etree.Element(q(A, tag))
    if w is None:
        etree.SubElement(el, q(A, "noFill"))
        return el
    el.set("w", str(w)), el.set("cap", "flat"), el.set("cmpd", "sng"), el.set("algn", "ctr")
    sf = etree.SubElement(el, q(A, "solidFill"))
    etree.SubElement(sf, q(A, "srgbClr")).set("val", color)
    etree.SubElement(el, q(A, "prstDash")).set("val", "solid")
    return el


def _set_text_color(tc, header):
    for rpr in tc.iter(q(A, "rPr"), q(A, "endParaRPr")):
        clr = rpr.find("%s/%s" % (q(A, "solidFill"), q(A, "srgbClr")))
        if clr is None:
            continue
        v = clr.get("val", "").upper()
        if header and v in ("FFFFFF", "FFFEFF"):
            clr.set("val", NAVY)
        elif not header and v in ("1C1F28", "222224", "000000"):
            clr.set("val", BODY_TXT)


def restyle_table(tbl):
    tblPr = tbl.find(q(A, "tblPr"))
    if tblPr is None:
        tblPr = etree.Element(q(A, "tblPr"))
        tbl.insert(0, tblPr)
    tblPr.set("firstRow", "1")
    sid = tblPr.find(q(A, "tableStyleId"))
    if sid is None:
        sid = etree.SubElement(tblPr, q(A, "tableStyleId"))
    sid.text = TABLE_STYLE
    for r, tr in enumerate(tbl.findall(q(A, "tr"))):
        header = r == 0
        for tc in tr.findall(q(A, "tc")):
            tcPr = tc.find(q(A, "tcPr"))
            if tcPr is None:
                tcPr = etree.SubElement(tc, q(A, "tcPr"))
            fill = None
            for ch in list(tcPr):
                name = etree.QName(ch).localname
                if name == "solidFill":
                    c = ch.find(q(A, "srgbClr"))
                    if c is not None and not header and c.get("val", "").upper() in KEEP_FILLS:
                        fill = ch
                if name in ("lnL", "lnR", "lnT", "lnB", "solidFill", "noFill", "gradFill", "blipFill", "pattFill", "grpFill"):
                    tcPr.remove(ch)
            new = [_line("lnL"), _line("lnR"),
                   _line("lnT") if header else (_line("lnT", 25400, NAVY) if r == 1 else _line("lnT", 9525, GRID)),
                   _line("lnB", 25400, NAVY) if header else _line("lnB", 9525, GRID)]
            new.append(fill if fill is not None else etree.Element(q(A, "noFill")))
            for i, el in enumerate(new):
                tcPr.insert(i, el)
            _set_text_color(tc, header)


def restyle_slide(xml):
    root = etree.fromstring(xml.encode("utf-8"))
    for tbl in root.iter(q(A, "tbl")):
        restyle_table(tbl)
    return etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True).decode("utf-8")


def run(src, dst):
    n_tbl = n_tr = 0
    with zipfile.ZipFile(src) as zin, zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zout:
        for info in zin.infolist():
            data = zin.read(info.filename)
            name = info.filename
            if name.endswith(".xml") and (name.startswith("ppt/slides/slide") or name.startswith("ppt/slideLayouts/")
                                          or name.startswith("ppt/slideMasters/") or name.startswith("ppt/charts/chart")):
                xml = data.decode("utf-8")
                before = xml.count("<p:transition")
                xml = strip_transitions(xml)
                n_tr += before
                xml = recolor(xml)
                if name.startswith("ppt/slides/slide") and "<a:tbl>" in xml:
                    n_tbl += xml.count("<a:tbl>")
                    xml = restyle_slide(xml)
                data = xml.encode("utf-8")
            zout.writestr(info, data)
    print("restyled %s -> %s: %d table(s), %d transition(s) removed" % (src, dst, n_tbl, n_tr))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    run(sys.argv[1], sys.argv[2])
