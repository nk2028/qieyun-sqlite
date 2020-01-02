# _Guangyun_

SQLite database and JavaScript APIs for traditional Chinese phonology

## Usage

### SQLite Database (in `db` folder)

Find the small rhymes without _fanqie_:

```sql
SELECT 小韻號, 音韻地位, 反切,
group_concat(字頭, '') AS 字頭
FROM 廣韻字頭全
WHERE 反切 IS NULL
GROUP BY 小韻號;
```

| 小韻號 | 音韻地位 | 反切 | 字頭 |
| - | - | - | - |
| 1919 | 章開三蒸上 | _NULL_ | 拯抍撜𨋬氶 |
| 3177 | 影開二銜去 | _NULL_ | 𪒠 |

### JavaScript Library (in `js` folder)

```javascript
char_entities['拯'];  // [["1919", "救也助也無韻切音蒸上聲五"]]
let 小韻號 = 1919;  // 選擇第 1919 小韻（拯小韻）
const is = s => check小韻(小韻號, s);
is('章母');  // true, 拯小韻是章母
is('曉匣母');  // false, 拯小韻不是曉匣母
is('重紐A類 或 以母 或 端精章組 或 日母');  // true, 拯小韻是章組
```

See <https://sgalal.github.io/Guangyun/> for details.

## Build

**Prerequisite**

```sh
$ npm install -g minify
```

**CodeMirror Files**

Download prefix: <https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.48.4/>

* `codemirror.min.js`
* `codemirror.min.css`
* `mode/javascript/javascript.min.js`
* `mode/sql/sql.min.js`

**Build**

```sh
$ python db/build.py
$ python db/yonhdo.py
$ python js/build.py
```

## License

_Guangyun_ data is in the public domain.

Codes from the CodeMirror project (`/docs/codemirror`) is distributed under MIT license.

Other codes and web pages are distributed under MIT license.
