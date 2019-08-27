#!/usr/bin/env python3

from itertools import repeat
import os.path
import pandas
import sqlite3
import urllib.request

# Download files

def download_file_if_not_exist(name, download_prefix='https://raw.githubusercontent.com/BYVoid/ytenx/master/ytenx/sync/kyonh/'):
	if not os.path.exists(name):
		urllib.request.urlretrieve(download_prefix + name, name)

download_file_if_not_exist('YonhMiuk.txt')
download_file_if_not_exist('SieuxYonh.txt')
download_file_if_not_exist('Yonhmux.txt')
download_file_if_not_exist('Dzih.txt')

# Emplace data

conn = sqlite3.connect('data.sqlite3')
cur = conn.cursor()

cur.execute('''
	CREATE TABLE 'rhymes'                -- 韻
	( 'name'        VARCHAR PRIMARY KEY  -- 韻母
	, 'rhyme_group' VARCHAR NOT NULL     -- 韻系（舉平以該上去入，以及祭泰夬廢）
	, 'tone'        INTEGER NOT NULL     -- 聲調（1-4）
		CHECK
		(   LENGTH(name) = LENGTH(rhyme_group)
		AND tone >= 1
		AND tone <= 4
		)
	);
	''')

cur.execute('''
	CREATE TABLE 'temp_small_rhyme_1' -- temp_small_rhyme_1
	( 'id'      INTEGER PRIMARY KEY
	, 'name'    VARCHAR               -- 小韻
	, 'initial' VARCHAR NOT NULL      -- 聲母（三十八聲母系統）
	, 'rhyme1'  VARCHAR NOT NULL      -- 對應細分韻
	, 'rhyme'   VARCHAR NOT NULL      -- 對應韻
	, 'fanqie'  VARCHAR               -- 反切
	);
	''')

cur.execute('''
	CREATE TABLE 'temp_small_rhyme_2'   -- temp_small_rhyme_2
	( 'id'         INTEGER PRIMARY KEY
	, 'rhyme1'     VARCHAR NOT NULL     -- 對應細分韻
	, 'division'   INTEGER              -- 等（1-4）
	, 'rounding'   VARCHAR NOT NULL     -- 開合
	  CHECK
		(   division >= 1
		AND division <= 4
		AND rounding IN ('開', '合')
		)
	);
	''')

cur.execute('''
	CREATE TABLE 'small_rhymes'                          -- 小韻
	( 'id'         INTEGER PRIMARY KEY
	, 'of_rhyme'   VARCHAR NOT NULL REFERENCES 'rhymes'  -- 對應韻
	, 'initial'    VARCHAR NOT NULL                      -- 聲母（三十八聲母系統）
	, 'rounding'   VARCHAR NOT NULL                      -- 開合
	, 'division'   INTEGER                               -- 等（1-4）
	, 'upper_char' VARCHAR                               -- 反切上字
	, 'lower_char' VARCHAR                               -- 反切下字
		CHECK
		(   LENGTH(initial) = 1
		AND rounding IN ('開', '合')
		AND division >= 1
		AND division <= 4
		AND LENGTH(upper_char) = 1
		AND LENGTH(lower_char) = 1
		)
	);
	''')

cur.execute('''
	CREATE TABLE 'char_entities'                                       -- 字頭
	( 'id'                 INTEGER PRIMARY KEY
	, 'name'               VARCHAR NOT NULL                            -- 字
	, 'of_small_rhyme'     INTEGER NOT NULL REFERENCES 'small_rhymes'  -- 對應小韻
	, 'num_in_small_rhyme' INTEGER NOT NULL                            -- 在小韻中的序號
	, 'explanation'        VARCHAR NOT NULL                            -- 解釋
	);
	''')

cur.execute('CREATE INDEX idx_small_rhymes_upper_char on small_rhymes (upper_char);')
cur.execute('CREATE INDEX idx_small_rhymes_lower_char on small_rhymes (lower_char);')

rhyme_data = pandas.read_csv('YonhMiuk.txt', sep=' ', usecols=['#韻目', '韻系', '聲調'])
cur.executemany('INSERT INTO rhymes VALUES (?, ?, ?)', zip(rhyme_data['#韻目'], rhyme_data['韻系'], rhyme_data['聲調']))

small_rhyme_data_1 = pandas.read_csv('SieuxYonh.txt', sep=' ', header=None, usecols=[0, 1, 2, 3, 4, 5], names=['SmallRhymeId', 'SmallRhyme', 'Initial', 'Rhyme1', 'Rhyme', 'Fanqie'])
cur.executemany('INSERT INTO temp_small_rhyme_1 VALUES (?, ?, ?, ?, ?, ?)', zip(small_rhyme_data_1['SmallRhymeId'], small_rhyme_data_1['SmallRhyme'], small_rhyme_data_1['Initial'], small_rhyme_data_1['Rhyme1'], small_rhyme_data_1['Rhyme'], small_rhyme_data_1['Fanqie']))

small_rhyme_data_2 = pandas.read_csv('YonhMux.txt', sep=' ', usecols=['#韻母', '等', '呼'])
cur.executemany('INSERT INTO temp_small_rhyme_2 VALUES (?, ?, ?, ?)', zip(repeat(None), small_rhyme_data_2['#韻母'], small_rhyme_data_2['等'], small_rhyme_data_2['呼']))

char_entity_data = pandas.read_csv('Dzih.txt', sep=' ', header=None, names=['Name', 'SmallRhymeId', 'NumInSmallRhyme', 'Explanation'])
cur.executemany('INSERT INTO char_entities VALUES (?, ?, ?, ?, ?)', zip(repeat(None), char_entity_data['Name'], char_entity_data['SmallRhymeId'], char_entity_data['NumInSmallRhyme'], char_entity_data['Explanation']))

cur.execute('''
	INSERT INTO small_rhymes
		SELECT temp_small_rhyme_1.id, rhyme AS of_rhyme, initial, rounding, division, SUBSTR(fanqie, 1, 1) AS upper_char, SUBSTR(fanqie, 2) AS lower_char
			FROM temp_small_rhyme_1, temp_small_rhyme_2
			WHERE temp_small_rhyme_1.rhyme1 = temp_small_rhyme_2.rhyme1;
	''')

cur.execute('DROP TABLE temp_small_rhyme_1')
cur.execute('DROP TABLE temp_small_rhyme_2')

cur.close()
conn.commit()
conn.close()
