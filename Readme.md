# 概要

秋月のサイトから価格と通販コードと秋葉原店の部品場所を取得する

# 環境

- linuxmint 19.2
- python3.8
- Baetifulesoap
- duckduckgo_search（インストールが必要そして改造が必要）

#インストール

'''bash
pip3 install duckduckgo_search
'''
duckduckgo_search.pyにおいてsleep(0.75)を削らないと検索時に引っかかってしまう。

# 使い方

商品名のみリストをエクセル等で作成して、akizuki_parts.csvを作成する。
同じディレクトリで、
'''python
python3 main.py
'''
とするれば自動でwebより取得する。
akizuki_parts_list.txtが出力ファイル

# 注意

秋月のサイトの特性上、約5秒間隔で取得を行うためそれなりに時間がかかる。（サーバーの負荷軽減）
取得できない場合は通販コードがおかしい。
# Author
 
* 巳摩
* 令和4年6月22日
 
# License
[MIT license](https://en.wikipedia.org/wiki/MIT_License).

