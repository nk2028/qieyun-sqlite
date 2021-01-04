import os
import sqlite3

os.system('curl -LsSo 字頭表.csv https://raw.githubusercontent.com/nk2028/qieyun-data/9849852/%E5%AD%97%E9%A0%AD%E8%A1%A8.csv')
os.system('curl -LsSo 小韻表.csv https://raw.githubusercontent.com/nk2028/qieyun-data/9849852/%E5%B0%8F%E9%9F%BB%E8%A1%A8.csv')

conn = sqlite3.connect('qieyun.sqlite3')
cur = conn.cursor()

def 生成號SQL(s):
	return '\n'.join(f"WHEN '{c}' THEN {i}" for i, c in enumerate(s, 1))

母號SQL = 生成號SQL('幫滂並明端透定泥來知徹澄孃精清從心邪莊初崇生俟章昌常書船日見溪羣疑影曉匣云以')
韻號SQL = 生成號SQL('東冬鍾江支脂之微魚虞模齊祭泰佳皆夬灰咍廢眞臻文欣元魂痕寒刪山仙先蕭宵肴豪歌麻陽唐庚耕清青蒸登尤侯幽侵覃談鹽添咸銜嚴凡')

攝順序 = [
	('通', '東冬鍾'),
	('江', '江'),
	('止', '支脂之微'),
	('遇', '魚虞模'),
	('蟹', '齊佳皆灰咍祭泰夬廢'),
	('臻', '眞諄臻文欣元魂痕'),
	('山', '寒桓刪山先仙'),
	('效', '蕭宵肴豪'),
	('果', '歌戈'),
	('假', '麻'),
	('宕', '唐陽'),
	('梗', '庚耕清青'),
	('曾', '登蒸'),
	('流', '侯尤幽'),
	('深', '侵'),
	('咸', '覃談鹽添咸銜嚴凡'),
]

清濁列表 = [
	('全清', '幫端知精心莊生章書見影曉'),
	('次清', '滂透徹清初昌溪'),
	('全濁', '並定澄從邪崇俟常船羣匣'),
	('次濁', '明泥孃來日疑云以'),
]

音列表 = [
	('脣', '幫滂並明'),
	('舌', '端透定泥知徹澄孃來'),
	('齒', '精清從心邪莊初崇生俟章昌常書船日'),
	('牙', '見溪羣疑'),
	('喉', '影曉匣云以'),
]

組列表 = [
	('幫', '幫滂並明'),
	('端', '端透定泥'),
	('知', '知徹澄孃'),
	('精', '精清從心邪'),
	('莊', '莊初崇生俟'),
	('章', '章昌常書船'),
	('見', '見溪羣疑'),
	('影', '影曉匣云'),
]

攝號SQL = '\n'.join(f"""WHEN 韻 IN ({','.join(f"'{韻}'" for 韻 in 韻們)}) THEN {攝號}""" for 攝號, (_, 韻們) in enumerate(攝順序, 1))
攝SQL = '\n'.join(f"""WHEN 韻 IN ({','.join(f"'{韻}'" for 韻 in 韻們)}) THEN '{攝}'""" for 攝, 韻們 in 攝順序)
清濁SQL = '\n'.join(f"""WHEN 母 IN ({','.join(f"'{母}'" for 母 in 母們)}) THEN '{清濁}'""" for 清濁, 母們 in 清濁列表)
音SQL = '\n'.join(f"""WHEN 母 IN ({','.join(f"'{母}'" for 母 in 母們)}) THEN '{音}'""" for 音, 母們 in 音列表)
組SQL = '\n'.join(f"""WHEN 母 IN ({','.join(f"'{母}'" for 母 in 母們)}) THEN '{組}'""" for 組, 母們 in 組列表)
等數字SQL = "WHEN 1 THEN '一' WHEN 2 THEN '二' WHEN 3 THEN '三' WHEN 4 THEN '四'"

## 小韻

cur.execute('''
CREATE TABLE '小韻'
( '小韻號' INTEGER PRIMARY KEY
, '母' TEXT NOT NULL CHECK (length(母) = 1)
, '呼' TEXT CHECK (呼 IN ('開', '合'))
, '等數字' INTEGER NOT NULL CHECK (等數字 >= 1 AND 等數字 <= 4)
, '重紐' TEXT CHECK (重紐 IN ('A', 'B'))
, '韻' TEXT NOT NULL CHECK (length(韻) = 1)
, '聲' TEXT NOT NULL CHECK (length(韻) = 1)
, '上字' TEXT CHECK (length(上字) = 1)
, '下字' TEXT CHECK (length(下字) = 1)
);''')

def 小韻資料():
	with open('小韻表.csv') as f:
		next(f) # skip header
		for line in f:
			小韻號, 母, 呼, 等, 重紐, 韻, 聲, 反切 = line.rstrip('\n').split(',')
			小韻號 = int(小韻號)
			呼 = None if 呼 == '' else 呼
			等數字 = '〇一二三四'.index(等)
			重紐 = None if 重紐 == '' else 重紐
			上字 = None if 反切 == '' else 反切[0]
			下字 = None if 反切 == '' else 反切[1]
			yield 小韻號, 母, 呼, 等數字, 重紐, 韻, 聲, 上字, 下字

cur.executemany('INSERT INTO 小韻 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', 小韻資料())

## 字頭

cur.execute('''
CREATE TABLE '字頭'
( '字頭號' INTEGER PRIMARY KEY
, '小韻號' INTEGER NOT NULL REFERENCES '小韻'
, '字頭' TEXT NOT NULL
, '解釋' TEXT NOT NULL
);''')

def 字頭資料():
	with open('字頭表.csv') as f:
		next(f) # skip header
		for line in f:
			小韻號, 字頭, 釋義 = line.rstrip('\n').split(',')
			字頭號 = None
			小韻號 = int(小韻號)
			yield 字頭號, 小韻號, 字頭, 釋義

cur.executemany('INSERT INTO 字頭 VALUES (?, ?, ?, ?)', 字頭資料())

# Extra

cur.execute(f'''
CREATE VIEW '小韻全' AS
SELECT 小韻號,
母 ||
ifnull(呼, '') ||
CASE 等數字 {等數字SQL} END ||
ifnull(重紐, '') ||
韻 ||
聲 AS 音韻描述,
母,
呼,
CASE 等數字 {等數字SQL} END AS 等,
重紐,
韻,
聲,
CASE {清濁SQL} END AS 清濁,
CASE {音SQL} END AS 音,
CASE {組SQL} END AS 組,
CASE {攝SQL} END AS 攝,
CASE 母 {母號SQL} END AS 母號,
CASE {攝號SQL} END AS 攝號,
等數字,
CASE 韻 {韻號SQL} END AS 韻號,
上字, 下字
FROM 小韻;''')

cur.execute('''
CREATE VIEW '字頭全' AS
SELECT 字頭號, 字頭, 音韻描述,
母, 呼, 等, 重紐, 韻, 聲,
清濁, 音, 組, 攝,
小韻號,
母號, 攝號, 等數字, 韻號,
上字, 下字,
解釋
FROM 字頭
INNER JOIN 小韻全
USING (小韻號);''')

cur.close()
conn.commit()
conn.execute('VACUUM')
conn.close()
