# 作例：論文ゼミ（Trinh & Combes 2021、90 分、43 枚）

本人が 2026-10-14 に発表した資料の生成スクリプト。型に迷ったら、ここの `parts/` を見る。

```bash
PY=~/.claude/skills/seminar-slides/.venv/bin/python
$PY build_1014.py <図のフォルダ> out.pptx
```

動かすには次の 2 つが要る（どちらもリポジトリには入れていない）。

- `<図のフォルダ>`：原論文（arXiv:2102.10200）の図と、実験の図（本人の手元では `~/reserch/03_slides/02_論文ゼミ/wip_trinh2021/fig/`）
- `assets/reference/` の過去資料（`paper0421`・`thesis`）。`RTH` の図形の番号は旧版の修論スライドのもので、
  完成版では番号がずれている可能性がある。使う前に `scripts/xdump.py` で確かめ直す

本人はこの生成物を手で直してから発表した（色・表・切り替え効果は `scripts/restyle.py`、
図と箇条書きの直しは `assets/reference/スライドデザイン変更点まとめ.pptx`）。仕上がりは `gallery/slides/`。
