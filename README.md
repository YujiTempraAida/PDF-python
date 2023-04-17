# add-text-to-pdf
複数ページにわたるPDFファイルに同じテキストを書き加えるプログラム。
Start.ggからダウンロードしたブラケットpdfファイルに対し、どの順で試合を消化すべきかの案内などを載せるために作成。
出力イメージ
![追記されたPDF](https://cdn.discordapp.com/attachments/806732246806954005/1097430573246599189/image.png)

# 使い方
1. main.pyのパラメタを変更する。
  PAGE_X: テキストボックスのX座標
  PAGE_Y: テキストボックスのY座標
  PAGE_INPUTTEXT: 入力したいテキスト

2. 追記したいpdfファイルの名前を"input.pdf"に変更してmain.pyと同階層に配置する

3. main.pyを実行する
