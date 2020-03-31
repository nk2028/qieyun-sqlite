# qieyun-sqlite [![JSDelivr badge](https://data.jsdelivr.com/v1/package/npm/qieyun-sqlite/badge)](https://www.jsdelivr.com/package/npm/qieyun-sqlite)

《切韻》音系 SQLite 資料庫

姊妹項目：《切韻》音系 JavaScript 函式庫 \([sgalal/qieyun-js](https://github.com/sgalal/qieyun-js)\)。

## 用法

下載連結：<https://cdn.jsdelivr.net/npm/qieyun-sqlite@0.1.30/data.sqlite3> (1.55 MB)。

推薦使用 [DB Browser for SQLite](https://sqlitebrowser.org/) 開啓 [本資料庫](https://sgalal.github.io/qieyun-sqlite/data.sqlite3)。

![Screenshot of DB Browser for SQLite showing the qieyun-sqlite database](screenshot.png)

## 示例

Examples on Google Colab:

- [廣韻聲類與等配合表](https://colab.research.google.com/drive/12QmUVy8xdb_Uyh562UfF0HRibJfxg7Nu)
- [廣韻韻等與開合配合表](https://colab.research.google.com/drive/1VDJJ2N4jjZZ4FsAK_bGPS5m8mIUKzhfM)
- [廣韻的例外](https://colab.research.google.com/drive/1hmCivFJ2ZWDm8b9Oyk34g-VTFYkd7BJf)

## Build

Build:

```sh
$ pip install -r requirements.txt
$ npm install
$ python build.py
```

## License

Dictionary data is in the public domain.

Python code are distributed under MIT license.
