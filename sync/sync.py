#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from itertools import repeat
import os
import pandas
import sqlite3
import urllib.request

# Prepare files

def download_file_if_not_exist(name, download_prefix='https://raw.githubusercontent.com/sgalal/ytenx/patch-1/ytenx/sync/kyonh/'):
	if not os.path.exists(name):
		urllib.request.urlretrieve(download_prefix + name, name)

## Data files

download_file_if_not_exist('sync/YonhMiuk.txt')
download_file_if_not_exist('sync/SieuxYonh.txt')
download_file_if_not_exist('sync/Yonhmux.txt')
download_file_if_not_exist('sync/Dzih.txt')

## Knowledge files

download_file_if_not_exist('sync/YonhGheh.txt')
download_file_if_not_exist('sync/PrengQim.txt')
download_file_if_not_exist('sync/Dauh.txt')

## Database

if os.path.exists('docs/data.sqlite3'):
	os.remove('docs/data.sqlite3')

# Emplace data

## Connect to database

conn = sqlite3.connect('docs/data.sqlite3')
cur = conn.cursor()

## Emplace core_rhymes

cur.execute('''
CREATE TABLE 'core_rhymes'        -- 韻
( 'name' TEXT PRIMARY KEY         -- 韻
, 'tone' INTEGER NOT NULL         -- 聲調（1-4）
CHECK
(   tone >= 1
AND tone <= 4
)
);
''')

data_rhyme = pandas.read_csv('sync/YonhMiuk.txt', sep=' ', na_filter=False, usecols=['#韻目', '聲調'])
cur.executemany('INSERT INTO core_rhymes VALUES (?, ?)', zip(data_rhyme['#韻目'], data_rhyme['聲調']))

## Emplace TEMP core_small_rhyme_1

cur.execute('''
CREATE TEMP TABLE 'core_small_rhyme_1' -- core_small_rhyme_1
( 'id'      INTEGER PRIMARY KEY
, 'name'    TEXT                       -- 小韻
, 'initial' TEXT NOT NULL              -- 聲母（三十八聲母系統）
, 'rhyme1'  TEXT NOT NULL              -- 對應細分韻
, 'rhyme'   TEXT NOT NULL              -- 對應韻
, 'fanqie'  TEXT                       -- 反切
);
''')

data_small_rhyme_1 = pandas.read_csv('sync/SieuxYonh.txt', sep=' ', header=None, usecols=[0, 1, 2, 3, 4, 5], names=['SmallRhymeId', 'SmallRhyme', 'Initial', 'Rhyme1', 'Rhyme', 'Fanqie'])
cur.executemany('INSERT INTO core_small_rhyme_1 VALUES (?, ?, ?, ?, ?, ?)', zip(data_small_rhyme_1['SmallRhymeId'], data_small_rhyme_1['SmallRhyme'], data_small_rhyme_1['Initial'], data_small_rhyme_1['Rhyme1'], data_small_rhyme_1['Rhyme'], data_small_rhyme_1['Fanqie']))

## Emplace TEMP core_small_rhyme_2

cur.execute('''
CREATE TEMP TABLE 'core_small_rhyme_2'  -- core_small_rhyme_2
( 'id'         INTEGER PRIMARY KEY
, 'rhyme1'     TEXT NOT NULL            -- 對應細分韻
, 'division'   INTEGER NOT NULL         -- 等（1-4）
, 'rounding'   TEXT NOT NULL            -- 開合
CHECK
(   division >= 1
AND division <= 4
AND rounding IN ('開', '合')
)
);
''')

data_small_rhyme_2 = pandas.read_csv('sync/YonhMux.txt', sep=' ', na_filter=False, usecols=['#韻母', '等', '呼'])
cur.executemany('INSERT INTO core_small_rhyme_2 VALUES (?, ?, ?, ?)', zip(repeat(None), data_small_rhyme_2['#韻母'], data_small_rhyme_2['等'], data_small_rhyme_2['呼']))

## Emplace core_small_rhymes

cur.execute('''
CREATE TABLE 'core_small_rhymes'                       -- 小韻
( 'id'         INTEGER PRIMARY KEY
, 'name'       TEXT NOT NULL                           -- 小韻
, 'of_rhyme'   TEXT NOT NULL REFERENCES 'core_rhymes'  -- 對應韻
, 'initial'    TEXT NOT NULL                           -- 聲母（三十八聲母系統）
, 'rounding'   TEXT NOT NULL                           -- 開合
, 'division'   INTEGER NOT NULL                        -- 等（1-4）
, 'upper_char' TEXT                                    -- 反切上字
, 'lower_char' TEXT                                    -- 反切下字
CHECK
(   LENGTH(name) = 1
AND LENGTH(initial) = 1
AND rounding IN ('開', '合')
AND division >= 1
AND division <= 4
AND LENGTH(upper_char) = 1
AND LENGTH(lower_char) = 1
)
);
''')

cur.execute('''
INSERT INTO core_small_rhymes
SELECT core_small_rhyme_1.id, name, rhyme AS of_rhyme, initial, rounding, division, SUBSTR(fanqie, 1, 1) AS upper_char, SUBSTR(fanqie, 2) AS lower_char
FROM core_small_rhyme_1, core_small_rhyme_2
WHERE core_small_rhyme_1.rhyme1 = core_small_rhyme_2.rhyme1;
''')

## Emplace core_char_entities

cur.execute('''
CREATE TABLE 'core_char_entities'                                       -- 字頭
( 'of_small_rhyme'     INTEGER NOT NULL REFERENCES 'core_small_rhymes'  -- 對應小韻
, 'num_in_small_rhyme' INTEGER NOT NULL                                 -- 在小韻中的序號
, 'name'               TEXT NOT NULL                                    -- 字頭
, 'explanation'        TEXT NOT NULL                                    -- 解釋
, PRIMARY KEY (of_small_rhyme, num_in_small_rhyme)
);
''')

data_char_entity = pandas.read_csv('sync/Dzih.txt', sep=' ', na_filter=False, header=None, names=['Name', 'SmallRhymeId', 'NumInSmallRhyme', 'Explanation'])
cur.executemany('INSERT INTO core_char_entities VALUES (?, ?, ?, ?)', zip(data_char_entity['SmallRhymeId'], data_char_entity['NumInSmallRhyme'], data_char_entity['Name'], data_char_entity['Explanation']))

cur.execute('CREATE INDEX idx_core_small_rhymes_upper_char on core_small_rhymes (upper_char);')
cur.execute('CREATE INDEX idx_core_small_rhymes_lower_char on core_small_rhymes (lower_char);')

# Emplace knowledge

## Emplace extd_rhymes

cur.execute('''
CREATE TABLE 'extd_rhymes'
( 'of_rhyme' TEXT PRIMARY KEY REFERENCES 'core_rhymes'  -- 韻
, 'subgroup' TEXT NOT NULL                              -- 韻系（平入）
CHECK ( LENGTH(of_rhyme) = LENGTH(subgroup) )
);
''')

data_extd_rhyme = pandas.read_csv('sync/subgroup.csv', na_filter=False)
cur.executemany('INSERT INTO extd_rhymes VALUES (?, ?)', zip(data_extd_rhyme['Rhyme'], data_extd_rhyme['Subgroup']))

## Emplace extd_subgroups

cur.execute('''
CREATE TABLE 'extd_subgroups'
( 'of_subgroup' TEXT PRIMARY KEY REFERENCES 'extd_rhymes'  -- 韻系（平入）
, 'rhyme_group' TEXT NOT NULL                              -- 韻系（平）
CHECK ( LENGTH(of_subgroup) = LENGTH(rhyme_group) )
);
''')

data_rhyme_group = pandas.read_csv('sync/group.csv', na_filter=False)
cur.executemany('INSERT INTO extd_subgroups VALUES (?, ?)', zip(data_rhyme_group['Subgroup'], data_rhyme_group['Group']))

## Emplace extd_classes

cur.execute('''
CREATE TABLE 'extd_classes'
( 'of_rhyme_group' TEXT PRIMARY KEY REFERENCES 'extd_subgroups'  -- 韻系（平）
, 'class'          TEXT NOT NULL                                 -- 攝
CHECK ( LENGTH(class) = 1 )
);
''')

data_class = pandas.read_csv('sync/YonhGheh.txt', sep=' ', na_filter=False)
cur.executemany('INSERT INTO extd_classes VALUES (?, ?)', zip(data_class['#韻系'], data_class['攝']))

## Emplace extd_small_rhymes

cur.execute('''
CREATE TABLE 'extd_small_rhymes'
( 'of_small_rhyme' INTEGER PRIMARY KEY REFERENCES 'core_small_rhymes' -- 小韻
, 'guyun'          TEXT NOT NULL                                      -- 古韻羅馬字
, 'younu'          TEXT                                               -- 有女羅馬字
, 'baxter'         TEXT NOT NULL                                      -- Baxter
, 'zhongzhou'      TEXT NOT NULL                                      -- 推導中州音
, 'putonghua'      TEXT                                               -- 推導普通話
);
''')

data_extd_small_rhyme = pandas.read_csv('sync/PrengQim.txt', sep=' ', keep_default_na=False, na_values=[''])  # https://stackoverflow.com/a/27173640
data_extd_small_rhyme2 = pandas.read_csv('sync/Dauh.txt', sep=' ', na_filter=False, usecols=['推導中州音', '推導普通話'])
cur.executemany('INSERT INTO extd_small_rhymes VALUES (?, ?, ?, ?, ?, ?)', zip(data_extd_small_rhyme['#序號'], data_extd_small_rhyme['古韻'], data_extd_small_rhyme['有女'], data_extd_small_rhyme['Baxter'], data_extd_small_rhyme2['推導中州音'], data_extd_small_rhyme2['推導普通話']))

# Create views

## full_rhymes

cur.execute('''
CREATE VIEW full_rhymes AS
SELECT name AS rhyme, tone, subgroup, rhyme_group, class
FROM core_rhymes, extd_rhymes, extd_subgroups, extd_classes
WHERE name = of_rhyme
AND subgroup = of_subgroup
AND rhyme_group = of_rhyme_group;
''')

## full_small_rhymes

cur.execute('''
CREATE VIEW full_small_rhymes AS
SELECT id, name AS small_rhyme, of_rhyme, initial, rounding, division,
upper_char, lower_char, guyun, younu, baxter, zhongzhou, putonghua
FROM core_small_rhymes, extd_small_rhymes
WHERE id = of_small_rhyme;
''')

## full_char_entities

cur.execute('''
CREATE VIEW full_char_entities AS
SELECT *
FROM core_char_entities;
''')

## full_guangyun

cur.execute('''
CREATE VIEW full_guangyun AS
SELECT rhyme, tone, subgroup, rhyme_group, class, id as 'small_rhyme_id', small_rhyme,
initial, rounding, division, upper_char, lower_char, guyun, younu, baxter,
zhongzhou, putonghua, num_in_small_rhyme, name, explanation
FROM full_rhymes JOIN full_small_rhymes JOIN full_char_entities
ON rhyme = of_rhyme AND id = of_small_rhyme;
''')

# Close database

cur.close()
conn.commit()
conn.close()
