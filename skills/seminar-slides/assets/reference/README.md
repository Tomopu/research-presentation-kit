# 本人の過去資料を置く場所

ここに置いた `.pptx` は `Slide.paste()` の複製元になる（`deck.REF`）。リポジトリには入れない（`.gitignore`）。

| ファイル名 | `paste()` での名前 | 中身 |
|---|---|---|
| `論文ゼミ_泉0421.pptx` | `"paper0421"` | 英語の論文ゼミ。MP-MAB の説明（3 枚目 Review、6 枚目 Setup、9 枚目 Regret Definition） |
| `泉知成_修論中間発表スライド_完成.pptx` | `"thesis"` | 日本語の修論中間発表。MP-MAB の図、分類の木、衝突で送る図、フェーズの帯、上界の式、表のデザイン |
| `スライドデザイン変更点まとめ.pptx` | `"fixes"` | 本人が Claude の資料を直した変更前・変更後（3 組） |

本人の手元では `~/reserch/03_slides/02_論文ゼミ/` と `~/reserch/03_slides/03_修論発表/` にある。

```bash
cp ~/reserch/03_slides/02_論文ゼミ/論文ゼミ_泉0421.pptx \
   ~/reserch/03_slides/03_修論発表/泉知成_修論中間発表スライド_完成.pptx \
   ~/reserch/03_slides/02_論文ゼミ/スライドデザイン変更点まとめ.pptx  <このフォルダ>/
```

ない場合は `paste()` が使えない。そのときは同じ図を部品（`player` `slot` `collide` など）で描く。
変更前・変更後の画像は、リポジトリの `gallery/fixes/` にある。
