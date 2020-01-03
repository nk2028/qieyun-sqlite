# qieyun-sqlite

## Usage

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

## License

Dictionary data is in the public domain.

Python code are distributed under MIT license.
