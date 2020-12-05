from itertools import repeat
import pandas
import sqlite3

conn = sqlite3.connect('qieyun.sqlite3')
cur = conn.cursor()

## TEMP 廣韻小韻1

cur.execute('''
CREATE TEMP TABLE '廣韻小韻1'
( '小韻號' INTEGER PRIMARY KEY
, '小韻' TEXT
, '母' TEXT NOT NULL
, '韻1' TEXT NOT NULL
, '韻' TEXT NOT NULL
, '反切' TEXT
);''')

data_small_rhyme_1 = pandas.read_csv(
	'cache/SieuxYonh.txt',
	sep=' ',
	header=None,
	usecols=[0, 1, 2, 3, 4, 5],
	names=['SmallRhymeId', 'SmallRhyme', 'Initial', 'Rhyme1', 'Rhyme', 'Fanqie']
)
cur.executemany('INSERT INTO 廣韻小韻1 VALUES (?, ?, ?, ?, ?, ?)', zip(data_small_rhyme_1['SmallRhymeId'], data_small_rhyme_1['SmallRhyme'], data_small_rhyme_1['Initial'], data_small_rhyme_1['Rhyme1'], data_small_rhyme_1['Rhyme'], data_small_rhyme_1['Fanqie']))

## TEMP 廣韻小韻2

cur.execute('''
CREATE TEMP TABLE '廣韻小韻2'
( 'id' INTEGER PRIMARY KEY
, '韻1' TEXT NOT NULL
, '等' INTEGER NOT NULL
, '開合' TEXT NOT NULL
);''')

data_small_rhyme_2 = pandas.read_csv(
	'cache/YonhMux.txt',
	sep=' ',
	na_filter=False,
	usecols=['#韻母', '等', '呼']
)
cur.executemany('INSERT INTO 廣韻小韻2 VALUES (?, ?, ?, ?)', zip(repeat(None), data_small_rhyme_2['#韻母'], data_small_rhyme_2['等'], data_small_rhyme_2['呼']))

## 廣韻小韻3

cur.execute('''
CREATE TEMP TABLE '廣韻小韻3'
( '小韻號' INTEGER PRIMARY KEY
, '古韻羅馬字' TEXT NOT NULL
, '有女羅馬字' TEXT
, '白一平轉寫' TEXT NOT NULL
, '推導中州音' TEXT NOT NULL
, '推導普通話' TEXT
);''')

data_extd_small_rhyme = pandas.read_csv(
	'cache/PrengQim.txt',
	sep=' ',
	keep_default_na=False,  # https://stackoverflow.com/a/27173640
	na_values=['']
)
data_extd_small_rhyme2 = pandas.read_csv(
	'cache/Dauh.txt',
	sep=' ',
	na_filter=False,
	usecols=['推導中州音', '推導普通話']
)
cur.executemany('INSERT INTO 廣韻小韻3 VALUES (?, ?, ?, ?, ?, ?)', zip(data_extd_small_rhyme['#序號'], data_extd_small_rhyme['古韻'], data_extd_small_rhyme['有女'], data_extd_small_rhyme['Baxter'], data_extd_small_rhyme2['推導中州音'], data_extd_small_rhyme2['推導普通話']))

## 廣韻小韻4

cur.execute('''
CREATE TEMP TABLE '廣韻小韻4'
( '小韻號' INTEGER PRIMARY KEY
, 'unt切韻朗讀音' TEXT NOT NULL
);''')

data_extd_small_rhyme_3 = pandas.read_csv(
	'cache/unt.txt',
	sep=',',
	na_filter=False,
	usecols=['小韻號', 'unt切韻朗讀音']
)
cur.executemany('INSERT INTO 廣韻小韻4 VALUES (?, ?)', zip(data_extd_small_rhyme_3['小韻號'], data_extd_small_rhyme_3['unt切韻朗讀音']))

## 廣韻小韻

cur.execute('''
CREATE TABLE '廣韻小韻'
( '小韻號' INTEGER PRIMARY KEY
, '小韻' TEXT NOT NULL CHECK (length(小韻) = 1)
, '母' TEXT NOT NULL CHECK (length(母) = 1)
, '開合' TEXT NOT NULL CHECK (開合 IN ('開', '合'))
, '等' INTEGER NOT NULL CHECK (等 >= 1 AND 等 <= 4)
, '重紐' TEXT CHECK (重紐 IN ('A', 'B'))
, '韻' TEXT NOT NULL CHECK (length(韻) = 1)
, '上字' TEXT CHECK (length(上字) = 1)
, '下字' TEXT CHECK (length(下字) = 1)
, '古韻羅馬字' TEXT NOT NULL
, '有女羅馬字' TEXT
, '白一平轉寫' TEXT NOT NULL
, 'unt切韻朗讀音' TEXT NOT NULL
, '推導中州音' TEXT NOT NULL
, '推導普通話' TEXT
);''')

cur.execute('''
INSERT INTO 廣韻小韻
SELECT 小韻號, 小韻,
母, 開合, 等,
nullif(substr(韻, 2, 1), '') AS 重紐,
substr(韻, 1, 1) AS 韻,
substr(反切, 1, 1) AS 上字, substr(反切, 2) AS 下字,
古韻羅馬字, 有女羅馬字, 白一平轉寫, unt切韻朗讀音, 推導中州音, 推導普通話
FROM 廣韻小韻1 INNER JOIN 廣韻小韻2
USING (韻1)
INNER JOIN 廣韻小韻3
USING (小韻號)
INNER JOIN 廣韻小韻4
USING (小韻號);''')

## 廣韻字頭

cur.execute('''
CREATE TABLE '廣韻字頭'
( '小韻號' INTEGER NOT NULL REFERENCES '廣韻小韻'
, '小韻內字序' INTEGER NOT NULL
, '字頭' TEXT NOT NULL
, '解釋' TEXT NOT NULL
, PRIMARY KEY ('小韻號', '小韻內字序')
);''')

data_char_entity = pandas.read_csv('cache/Dzih.txt', sep=' ', na_filter=False, header=None, names=['Name', 'SmallRhymeId', 'NumInSmallRhyme', 'Explanation'])
cur.executemany('INSERT INTO 廣韻字頭 VALUES (?, ?, ?, ?)', zip(data_char_entity['SmallRhymeId'], data_char_entity['NumInSmallRhyme'], data_char_entity['Name'], data_char_entity['Explanation']))

# Extra

韻到韻賅上去入 = pandas.read_csv('cache/YonhMiuk.txt', sep=' ', na_filter=False, usecols=['#韻目', '韻系'])
韻到韻賅上去入SQL = '\n'.join(f"WHEN '{x}' THEN '{y}'" for x, y in zip(韻到韻賅上去入['#韻目'], 韻到韻賅上去入['韻系']) if len(x) == 1)  # 重紐AB is removed here

母到母號 = pandas.read_csv('build/initial.csv', dtype=str, na_filter=False)
母到母號SQL = '\n'.join(f"WHEN '{x}' THEN {y}" for x, y in zip(母到母號['Initial'], 母到母號['InitialID']))

cur.execute(f'''
CREATE VIEW '廣韻小韻全' AS
SELECT 小韻號, 小韻,
小韻號 || 小韻 || '小韻' AS 小韻全名,
母 || 開合 || 等漢字 || ifnull(重紐, '') || 韻賅上去入 || 聲 AS 音韻描述,
CASE 母 {母到母號SQL} END AS 母號,
母,
CASE
WHEN 母 IN ('幫', '滂', '並', '明') THEN '幫'
WHEN 母 IN ('端', '透', '定', '泥') THEN '端'
WHEN 母 IN ('知', '徹', '澄', '孃') THEN '知'
WHEN 母 IN ('精', '清', '從', '心', '邪') THEN '精'
WHEN 母 IN ('莊', '初', '崇', '生', '俟') THEN '莊'
WHEN 母 IN ('章', '昌', '常', '書', '船') THEN '章'
WHEN 母 IN ('見', '溪', '羣', '疑') THEN '見'
WHEN 母 IN ('影', '曉', '匣', '云') THEN '影'
WHEN 母 IN ('來', '日', '以') THEN null
END AS 組,
開合, 等, 等漢字, 重紐,
韻,
韻賅上去入,
CASE
WHEN 韻賅上去入 IN ('東', '冬', '鍾') THEN 0
WHEN 韻賅上去入 IN ('江') THEN 1
WHEN 韻賅上去入 IN ('支', '脂', '之', '微') THEN 2
WHEN 韻賅上去入 IN ('魚', '虞', '模') THEN 3
WHEN 韻賅上去入 IN ('齊', '佳', '皆', '灰', '咍', '祭', '泰', '夬', '廢') THEN 4
WHEN 韻賅上去入 IN ('眞', '諄', '臻', '文', '欣', '元', '魂', '痕') THEN 5
WHEN 韻賅上去入 IN ('寒', '桓', '刪', '山', '先', '仙') THEN 6
WHEN 韻賅上去入 IN ('蕭', '宵', '肴', '豪') THEN 7
WHEN 韻賅上去入 IN ('歌', '戈') THEN 8
WHEN 韻賅上去入 IN ('麻') THEN 9
WHEN 韻賅上去入 IN ('唐', '陽') THEN 10
WHEN 韻賅上去入 IN ('庚', '耕', '清', '青') THEN 11
WHEN 韻賅上去入 IN ('登', '蒸') THEN 12
WHEN 韻賅上去入 IN ('侯', '尤', '幽') THEN 13
WHEN 韻賅上去入 IN ('侵') THEN 14
WHEN 韻賅上去入 IN ('覃', '談', '鹽', '添', '咸', '銜', '嚴', '凡') THEN 15
END AS 攝號,
CASE
WHEN 韻賅上去入 IN ('東', '冬', '鍾') THEN '通'
WHEN 韻賅上去入 IN ('江') THEN '江'
WHEN 韻賅上去入 IN ('支', '脂', '之', '微') THEN '止'
WHEN 韻賅上去入 IN ('魚', '虞', '模') THEN '遇'
WHEN 韻賅上去入 IN ('齊', '佳', '皆', '灰', '咍', '祭', '泰', '夬', '廢') THEN '蟹'
WHEN 韻賅上去入 IN ('眞', '諄', '臻', '文', '欣', '元', '魂', '痕') THEN '臻'
WHEN 韻賅上去入 IN ('寒', '桓', '刪', '山', '先', '仙') THEN '山'
WHEN 韻賅上去入 IN ('蕭', '宵', '肴', '豪') THEN '效'
WHEN 韻賅上去入 IN ('歌', '戈') THEN '果'
WHEN 韻賅上去入 IN ('麻') THEN '假'
WHEN 韻賅上去入 IN ('唐', '陽') THEN '宕'
WHEN 韻賅上去入 IN ('庚', '耕', '清', '青') THEN '梗'
WHEN 韻賅上去入 IN ('登', '蒸') THEN '曾'
WHEN 韻賅上去入 IN ('侯', '尤', '幽') THEN '流'
WHEN 韻賅上去入 IN ('侵') THEN '深'
WHEN 韻賅上去入 IN ('覃', '談', '鹽', '添', '咸', '銜', '嚴', '凡') THEN '咸'
END AS 攝,
聲, 上字, 下字,
上字 || 下字 || '切' AS 反切,
古韻羅馬字, 有女羅馬字, 白一平轉寫, unt切韻朗讀音, 推導中州音, 推導普通話
FROM (SELECT 小韻號, 小韻, 母, 開合, 等,
CASE 等
WHEN 1 THEN '一'
WHEN 2 THEN '二'
WHEN 3 THEN '三'
ELSE '四'
END AS 等漢字, 重紐, 韻,
CASE 韻 {韻到韻賅上去入SQL} END AS 韻賅上去入,
CASE
WHEN 小韻號 <= 1156 THEN '平'
WHEN 小韻號 <= 2091 THEN '上'
WHEN 小韻號 <= 3182 THEN '去'
WHEN 小韻號 <= 3874 THEN '入'
END AS 聲,
上字, 下字,
古韻羅馬字, 有女羅馬字, 白一平轉寫, unt切韻朗讀音, 推導中州音, 推導普通話
FROM 廣韻小韻);''')

cur.execute('''
CREATE VIEW '廣韻字頭全' AS
SELECT 字頭號, 字頭, 小韻號, 小韻, 音韻描述, 小韻內字序,
母號, 母, 組, 開合, 等, 等漢字, 重紐, 韻,
韻賅上去入, 攝號, 攝, 聲, 上字, 下字, 反切,
古韻羅馬字, 有女羅馬字, 白一平轉寫, unt切韻朗讀音, 推導中州音, 推導普通話, 解釋
FROM (SELECT row_number() OVER (ORDER BY 小韻號, 小韻內字序) AS 字頭號,
小韻號, 小韻內字序, 字頭, 解釋
FROM 廣韻字頭)
INNER JOIN 廣韻小韻全
USING (小韻號);''')

cur.close()
conn.commit()
conn.execute('VACUUM')
conn.close()
