# _Guangyun_

Database and APIs for traditional Chinese phonology

## Database (in `db` folder)

### Usage

The database could be downloaded from <https://sgalal.github.io/Guangyun/data.sqlite3>.

Or you can access the [web interface](https://sgalal.github.io/Guangyun/db/).

### Structure

廣韻數據庫包括兩張表：`廣韻小韻` (共 3874 行) 與 `廣韻字頭` (共 25333 行)。

`廣韻小韻` 包括：`小韻號`, `小韻`, `韻`, `母`, `開合`, `等`, `上字`, `下字`, `古韻羅馬字`, `有女羅馬字`, `白一平轉寫`, `推導中州音`, `推導普通話`

`廣韻字頭` 包括：`小韻號`, `小韻內字序`, `字頭`, `解釋`

為便於使用，還創建了兩個視圖：`廣韻小韻全` (共 3874 行) 與 `廣韻字頭全` (共 25333 行)。

`廣韻小韻全` 包括：`小韻號`, `小韻`, `小韻全名`, `音韻地位`, `韻`, `韻賅上去`, `韻賅上去入`, `攝`, `母號`, `母`, `開合`, `等`, `等漢字`, `聲`, `上字`, `下字`, `古韻羅馬字`, `有女羅馬字`, `白一平轉寫`, `推導中州音`, `推導普通話`

`廣韻字頭全` 包括：`字頭號`, `字頭`, `解釋`, `小韻號`, `小韻`, `小韻全名`, `音韻地位`, `小韻內字序`, `韻`, `韻賅上去`, `韻賅上去入`, `攝`, `母號`, `母`, `開合`, `等`, `等漢字`, `聲`, `上字`, `下字`, `古韻羅馬字`, `有女羅馬字`, `白一平轉寫`, `推導中州音`, `推導普通話`

### Examples

找出沒有反切的小韻：

```sql
SELECT 小韻號, 音韻地位, 上字, 下字,
group_concat(字頭, '') AS 字頭
FROM 廣韻字頭全
WHERE 上字 IS NULL
OR 下字 IS NULL
GROUP BY 小韻號;
```

| 小韻號 | 音韻地位 | 上字 | 下字 | 字頭 |
| - | - | - | - | - |
| 1919 | 章開三蒸上 | _NULL_ | _NULL_ | 拯抍撜𨋬氶 |
| 3177 | 影開二銜去 | _NULL_ | _NULL_ | 𪒠 |

找出前 5 組具有相同名字的小韻：

```sql
SELECT 小韻, group_concat(小韻全名) AS 小韻全名
FROM 廣韻小韻全
GROUP BY 小韻
HAVING count(*) > 1
ORDER BY 小韻號
LIMIT 5;
```

| 小韻 | 小韻全名 |
| - | - |
| 中 | 3中小韻,2112中小韻 |
| 瞢 | 13瞢小韻,974瞢小韻 |
| 烘 | 32烘小韻,2118烘小韻 |
| 㟅 | 33㟅小韻,85㟅小韻 |
| 䃔 | 40䃔小韻,2123䃔小韻 |

More examples:

* [廣韻的例外](https://sgalal.github.io/Guangyun/db/notebook/廣韻的例外.html)
* [廣韻音節表](https://sgalal.github.io/Guangyun/db/notebook/廣韻音節表.html)
* [廣韻反切上字表](https://sgalal.github.io/Guangyun/db/notebook/廣韻反切上字表.html)
* [廣韻四聲相配表](https://sgalal.github.io/Guangyun/db/notebook/廣韻四聲相配表.html)
* [廣韻反切系聯](https://sgalal.github.io/Guangyun/db/notebook/廣韻反切系聯.html)
* [廣韻聲母與等配合表](https://sgalal.github.io/Guangyun/db/notebook/廣韻聲母與等配合表.html)
* [現代廣韻等韻圖](https://sgalal.github.io/Guangyun/db/example/yonhdo.html)

## JavaScript API (in `js` folder)

### Usage

```html
<script src="https://sgalal.github.io/Guangyun/brogue2.js"></script>
```

The size of the library is less than 1 MB, which is satisfactory for most of the web applications.

The actual transferred size (compressed) is less than 0.5 MB.

```javascript
char_entities['拯'];  // [["1919", "救也助也無韻切音蒸上聲五"]]
let 小韻號 = 1919;  // 選擇第 1919 小韻（拯小韻）
const is = s => check小韻(小韻號, s);
is('章母');  // true, 拯小韻是章母
is('曉匣母');  // false, 拯小韻不是曉匣母
is('重紐A類 或 以母 或 端精章組 或 日母');  // true, 拯小韻是章組
```

function `check小韻`：

參數 1：小韻號 (1 ≤ i ≤ 3874)

參數 2：字符串

字符串格式：先以「或」字分隔，再以空格分隔。

如 `見組 重紐A類 或 以母 四等 去聲` 表示「(見組 且 重紐A類) 或 (以母 且 四等 且 去聲)」。

字符串不支援括號。

支援的音韻屬性如下：

Phonological Attribute | Chinese Name | English Name | Possible Values
:- | :- | :- | :-
韻 | 韻母 | rhyme | 東冬鍾江支支A支B…<br/>董湩腫講紙紙A紙B…<br/>送宋用絳寘寘A寘B…<br/>屋沃燭覺…
韻賅上去 | 韻母（舉平以賅上去） | rhyme (舉平以賅上去) | 東冬鍾江支支A支B…<br/>祭泰夬廢<br/>屋沃燭覺…
韻賅上去入 | 韻母（舉平以賅上去入） | rhyme (舉平以賅上去入) | 東冬鍾江支支A支B…<br/>祭泰夬廢
攝 | 攝 | class | 通江止遇蟹臻山效果假宕梗曾流深咸
母 | 聲母 | initial | 幫滂並明<br/>端透定泥<br/>知徹澄孃<br/>精清從心邪<br/>莊初崇生俟<br/>章昌船書常<br/>見溪羣疑<br/>影曉匣云以來日
組 | 組 | group | 幫端知精莊章見<br/>（未涵蓋「影曉匣云以來日」）
等 | 等 | division | 一二三四<br/>1234
聲 | 聲調 | tone | 平上去入<br/>仄<br/>舒

亦支援「開」、「合」、「重紐A類」、「重紐B類」。

説明：

對重紐的處理：韻賅上去入的「支」就包括了「支、支A、支B」三種情況。

重紐四等（A類）是三等韻。

元韻放在臻攝而不是山攝。

dict `char_entities`:

二維數組，字 -> [(小韻號1, 解釋1), (小韻號2, 解釋2), ...]

### Low-Level API

```javascript
let 小韻號 = 1919;  // 選擇第 1919 小韻（拯小韻）
equal母(小韻號, '章');  // true, 拯小韻是章母
in母(小韻號, ['曉', '匣']);  // false, 拯小韻不是曉匣母
is重紐A類(小韻號) || equal母(小韻號, '以') || in組(小韻號, ['端', '精', '章']) || equal母(小韻號, '日');  // true, 拯小韻是章組
```

#### `equal`, `in` 類

* function `equal韻` `in韻`
* function `equal韻賅上去` `in韻賅上去`
* function `equal韻賅上去入` `in韻賅上去入`
* function `equal攝` `in攝`
* function `equal母` `in母`
* function `equal組` `in組`
* function `equal等` `in等`
* function `equal聲` `in聲`

參數 1：小韻號 (1 ≤ i ≤ 3874)

參數 2：相應音韻屬性的可能取值

#### `is` 類

* function `is開` `is合`
* function `is重紐A類` `is重紐B類`

參數：小韻號 (1 ≤ i ≤ 3874)

#### Map Table

* `韻賅上去到韻`
* `韻賅上去入到韻`
* `攝到韻`
* `韻賅上去入到重紐`
* `組到母`
