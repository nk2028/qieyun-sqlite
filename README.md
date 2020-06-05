# qieyun-sqlite

《切韻》音系 SQLite 資料庫

關聯項目：《切韻》音系 JavaScript 函式庫 \([nk2028/qieyun-js](https://github.com/nk2028/qieyun-js)\)。

## 用法

下載連結：See [releases](https://github.com/nk2028/qieyun-sqlite/releases).

推薦使用 [DB Browser for SQLite](https://sqlitebrowser.org/) 開啓本資料庫。

![Screenshot of DB Browser for SQLite showing the qieyun-sqlite database](screenshot.png)

## 示例

Examples on Google Colab:

- [廣韻聲類與等配合表](https://colab.research.google.com/drive/12QmUVy8xdb_Uyh562UfF0HRibJfxg7Nu)
- [廣韻韻等與開合配合表](https://colab.research.google.com/drive/1VDJJ2N4jjZZ4FsAK_bGPS5m8mIUKzhfM)
- [廣韻的例外](https://colab.research.google.com/drive/1hmCivFJ2ZWDm8b9Oyk34g-VTFYkd7BJf)

## 介紹

目前，使用電子資料瞭解《切韻》音系的方法主要有三類。一是查看 PDF 格式的影印古籍，二是使用[廣韻全字表](https://zhuanlan.zhihu.com/p/20430939)，三是使用工具網站或軟件，如[韻典網](https://ytenx.org/)、古音小鏡與漢字古今中外讀音查詢 APP。

而若要深入地探索《切韻》音系，還需要對資料進行編程，探索其中隱藏的關係。[《切韻》音系 SQLite 資料庫](https://github.com/nk2028/qieyun-sqlite)不但能實現上述三類方法的功能，還能使用 SQL 語言構建複雜的查詢，並透過編程語言執行更加複雜的操作，達到探索《切韻》音系的目的。

另外，資料庫中的資料與韻典網資料同步。如果韻典網資料有修正，只需要簡單地運行腳本，就可以生成新版本的《切韻》音系 SQLite 資料庫。

## Build

```sh
$ pip install -r requirements.txt
$ npm install qieyun
$ python build.py
```

## License

Dictionary data is in the public domain.

Python code are distributed under MIT license.
