#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# For /docs/db/example/yonhdo.html

from collections import defaultdict
import sqlite3

conn = sqlite3.connect('docs/data.sqlite3')
cur = conn.cursor()

d = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(dict))))

for 韻, 聲, 開合, 等, 母, 小韻, 小韻號 in cur.execute('SELECT 韻賅上去入, 聲, 開合, 等漢字, 母, 小韻, 小韻號 FROM 廣韻小韻全;'):
	d[韻][聲][開合][等][母] = 小韻, 小韻號

格式化小韻小韻號 = lambda 小韻, 小韻號: f'<a href="https://ytenx.org/kyonh/sieux/{小韻號}/">{小韻}</a>'

with open('docs/db/example/yonhdo.html', 'w') as f:
	f.write('''<!DOCTYPE html>
<html lang="zh-Hant-HK" xml:lang="zh-Hant-HK" dir="ltr">
<head>
  <meta charset="utf-8"/>
  <title>現代廣韻等韻圖</title>
  <meta name="author" content="sgalal"/>
  <meta name="keywords" content="廣韻, 切韻音系, 韻圖, 等韻圖, 漢語音韻學, 中古漢語, Guangyun, rime table, historical Chinese phonology, traditional Chinese phonology, Middle Chinese"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <style>
  body { margin: 2em auto; max-width: 50em; }
  h1 { text-align: center; }
  p { line-height: 1.5; text-align: justify; text-indent: 2em; }
  a { text-decoration: none; }
  table { border-collapse: collapse; }
  th, td { border: 1px solid black; vertical-align: top; }
  td:empty::before { content: "◯"; }
  </style>
  <!-- GitHub Corner from http://tholman.com/github-corners/ -->
  <style>.github-corner:hover .octo-arm{animation:octocat-wave 560ms ease-in-out}@keyframes octocat-wave{0%,100%{transform:rotate(0)}20%,60%{transform:rotate(-25deg)}40%,80%{transform:rotate(10deg)}}@media (max-width:500px){.github-corner:hover .octo-arm{animation:none}.github-corner .octo-arm{animation:octocat-wave 560ms ease-in-out}}</style>
</head>
<body>
<h1>現代廣韻等韻圖</h1>
<p>重紐單立韻目。韻目順序：東、冬、鍾、江、支、支A、支B、脂、脂A、脂B、之、微、魚、虞、模、齊、佳、皆、灰、咍、眞、眞A、眞B、諄、諄A、臻、文、欣、元、魂、痕、寒、桓、刪、山、先、仙、仙A、仙B、蕭、宵、宵A、宵B、肴、豪、歌、戈、麻、陽、唐、庚、耕、清、清A、青、蒸、登、尤、侯、幽、侵、侵A、侵B、覃、談、鹽、鹽A、鹽B、添、咸、銜、嚴、凡、祭、祭A、祭B、泰、夬、廢。</p>
<table><tr><th colspan="4"></th><th>幫</th><th>滂</th><th>並</th><th>明</th><th>端</th><th>透</th><th>定</th><th>泥</th><th>知</th><th>徹</th><th>澄</th><th>孃</th><th>精</th><th>清</th><th>從</th><th>心</th><th>邪</th><th>莊</th><th>初</th><th>崇</th><th>生</th><th>俟</th><th>章</th><th>昌</th><th>船</th><th>書</th><th>常</th><th>見</th><th>溪</th><th>羣</th><th>疑</th><th>影</th><th>曉</th><th>匣</th><th>云</th><th>以</th><th>來</th><th>日</th></tr>''')
	for 韻 in ('東','冬','鍾','江','支','支A','支B','脂','脂A','脂B','之','微','魚','虞','模','齊','佳','皆','灰','咍','眞','眞A','眞B','諄','諄A','臻','文','欣','元','魂','痕','寒','桓','刪','山','先','仙','仙A','仙B','蕭','宵','宵A','宵B','肴','豪','歌','戈','麻','陽','唐','庚','耕','清','清A','青','蒸','登','尤','侯','幽','侵','侵A','侵B','覃','談','鹽','鹽A','鹽B','添','咸','銜','嚴','凡','祭','祭A','祭B','泰','夬','廢'):
		韻之代碼 = '<td rowspan="32">' + 韻 + '</td>'
		for 聲 in '平上去入':
			聲之代碼 = '<td rowspan="8">' + 聲 + '</td>'
			for 開合 in '開合':
				開合之代碼 = '<td rowspan="4">' + 開合 + '</td>'
				for 等 in '一二三四':
					等之代碼 = '<td>' + 等 + '</td>'
					f.write('<tr>')
					f.write(韻之代碼)
					f.write(聲之代碼)
					f.write(開合之代碼)
					f.write(等之代碼)
					for 母 in '幫滂並明端透定泥知徹澄孃精清從心邪莊初崇生俟章昌船書常見溪羣疑影曉匣云以來日':
						f.write('<td>')
						f.write((lambda d: '' if d is None else (lambda d: '' if d is None else (lambda d: '' if d is None else (lambda d: '' if d is None else (lambda x: '' if x is None else 格式化小韻小韻號(*x))(d.get(母)))(d.get(等)))(d.get(開合)))(d.get(聲)))(d.get(韻)))
						f.write('</td>')
					f.write('</tr>\n')
					韻之代碼 = ''
					聲之代碼 = ''
					開合之代碼 = ''
	f.write('''</table>
<!-- GitHub Corner from http://tholman.com/github-corners/ -->
<a href="https://github.com/sgalal/Guangyun" class="github-corner" aria-label="View source on GitHub"><svg width="80" height="80" viewBox="0 0 250 250" style="fill:#151513; color:#aaa; position: absolute; top: 0; border: 0; right: 0;" aria-hidden="true"><path d="M0,0 L115,115 L130,115 L142,142 L250,250 L250,0 Z"></path><path d="M128.3,109.0 C113.8,99.7 119.0,89.6 119.0,89.6 C122.0,82.7 120.5,78.6 120.5,78.6 C119.2,72.0 123.4,76.3 123.4,76.3 C127.3,80.9 125.5,87.3 125.5,87.3 C122.9,97.6 130.6,101.9 134.4,103.2" fill="currentColor" style="transform-origin: 130px 106px;" class="octo-arm"></path><path d="M115.0,115.0 C114.9,115.1 118.7,116.5 119.8,115.4 L133.7,101.6 C136.9,99.2 139.9,98.4 142.2,98.6 C133.8,88.0 127.5,74.4 143.8,58.0 C148.5,53.4 154.0,51.2 159.7,51.0 C160.3,49.4 163.2,43.6 171.4,40.1 C171.4,40.1 176.1,42.5 178.8,56.2 C183.1,58.6 187.2,61.8 190.9,65.4 C194.5,69.0 197.7,73.2 200.1,77.6 C213.8,80.2 216.3,84.9 216.3,84.9 C212.7,93.1 206.9,96.0 205.4,96.6 C205.1,102.4 203.0,107.8 198.3,112.5 C181.9,128.9 168.3,122.5 157.7,114.1 C157.9,116.9 156.7,120.9 152.7,124.9 L141.0,136.5 C139.8,137.7 141.6,141.9 141.8,141.8 Z" fill="currentColor" class="octo-body"></path></svg></a>
</body>
</html>
''')
