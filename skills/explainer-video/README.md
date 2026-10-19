# explainer-video

研究の概念を、日本語ナレーション・字幕つきの説明動画（mp4）にする Claude Code スキル。規則と手順は `SKILL.md`。

| パス | 内容 |
|---|---|
| `SKILL.md` | 中身の決め方・台本・画面・確認の手順（Claude が読む本体） |
| `scripts/video.py` | エンジン（台本と描画関数 → 音声・コマ・mp4。色と描画の部品、LaTeX の組版 `tex()`） |
| `scripts/yomi.py` | 字幕（`$数式$`・`{表記\|よみ}` を含む）から読み上げの文を作る |
| `scripts/lexicon.tsv` | 専門用語・人名の読みの辞書 |
| `examples/thompson_sampling/` | 作例 1：Thompson Sampling と Selfish TS（`ts_explainer.py`、2 人の軌跡の再現 `toy.py`、500 試行の集計 `data/`） |
| `examples/ucb_klucb/` | 作例 2：UCB と KL-UCB（`ucb_explainer.py`、比較のシミュレーション `ucb_sim.py`） |

## 作例を作り直す

```bash
PY=~/.claude/skills/explainer-video/.venv/bin/python
cd ~/.claude/skills/explainer-video/examples/thompson_sampling && $PY ts_explainer.py
cd ../ucb_klucb && $PY ucb_sim.py && $PY ucb_explainer.py
```

それぞれ 10〜15 分（Apple M2、5 並列）。出力は同じフォルダの `*.mp4`、途中のファイルは `*_build/`（どちらも git に入れない）。
