#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import defaultdict
import json
import pandas
import sqlite3
import subprocess

conn = sqlite3.connect('docs/data.sqlite3')
cur = conn.cursor()

def build_map_1():
	f = open('js/map1.js', 'w')

	f.write('var 韻到韻賅上去=')
	韻到韻賅上去 = pandas.read_csv('db/subgroup.csv', na_filter=False)
	韻到韻賅上去_obj = {x: y for x, y in zip(韻到韻賅上去['Rhyme'], 韻到韻賅上去['Subgroup']) if len(x) == 1}
	json.dump(韻到韻賅上去_obj, f, ensure_ascii=False, separators=(',',':'))
	f.write(';\n')

	f.write('var 韻到韻賅上去入=')
	韻到韻賅上去入 = pandas.read_csv('db/YonhMiuk.txt', sep=' ', na_filter=False, usecols=['#韻目', '韻系'])
	韻到韻賅上去入_obj = {x: y for x, y in zip(韻到韻賅上去入['#韻目'], 韻到韻賅上去入['韻系']) if len(x) == 1}
	json.dump(韻到韻賅上去入_obj, f, ensure_ascii=False, separators=(',',':'))
	f.write(';\n')

	f.write('var 韻賅上去入到攝=')
	韻賅上去入到攝 = pandas.read_csv('db/YonhGheh.txt', sep=' ', na_filter=False)
	韻賅上去入到攝_obj = {x: y for x, y in zip(韻賅上去入到攝['#韻系'], 韻賅上去入到攝['攝']) if len(x) == 1}
	json.dump(韻賅上去入到攝_obj, f, ensure_ascii=False, separators=(',',':'))
	f.write(';\n')

	f.close()

build_map_1()

def build_small_rhyme():
	f = open('js/small_rhyme.js', 'w')
	f.write('const small_rhymes=__process_small_rhyme("')
	f.write(''.join(''.join((母, 'O' if 開合 == '開' else 'C', str(等), 韻, 重紐 or '')) \
		for 母, 開合, 等, 韻, 重紐 \
		in cur.execute('SELECT 母, 開合, 等, 韻, 重紐 FROM 廣韻小韻全 ORDER BY 小韻號;')))
	f.write('");\n')  # 母, 開合, 等, 韻, 重紐，且等為數字
	f.close()

build_small_rhyme()

def build_char_entity():
	f = open('js/char_entity.js', 'w')
	f.write('const char_entities=__process_char_entities("')
	f.write(''.join(''.join((str(小韻號), 字頭, 解釋)) \
		for 小韻號, 字頭, 解釋
		in cur.execute('SELECT 小韻號, 字頭, 解釋 FROM 廣韻字頭 WHERE length(字頭) = 1;')))
	f.write('");\n')
	f.close()

build_char_entity()

cur.close()
conn.close()

def minify_brogue2():
	with open('js/brogue2.min.js', 'w') as fout:
		subprocess.call(['minify', 'js/brogue2.js'], stdout=fout, shell=True)

minify_brogue2()

def concat_files(l, s):
	fout = open(s, 'w')
	for i in l:
		f = open(i)
		fout.write(f.read())
		f.close()
		fout.write('\n')
	fout.close()

concat_files(('js/map.js', 'js/map1.js', 'js/char_entity.js', 'js/small_rhyme.js', 'js/brogue2.min.js'), 'docs/brogue2.js')
