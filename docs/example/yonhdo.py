#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import defaultdict
import sqlite3

conn = sqlite3.connect('docs/data.sqlite3')
cur = conn.cursor()

d = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(dict))))

for 韻, 聲, 開合, 等, 母, 小韻, 小韻號 in cur.execute( \
'''
SELECT rhyme_group, tone, rounding,
division, initial, small_rhyme, id
FROM core_rhymes AS A
INNER JOIN full_small_rhymes AS B
INNER JOIN extd_rhymes AS C
INNER JOIN extd_subgroups AS D
ON A.name = B.of_rhyme
AND B.of_rhyme = C.of_rhyme
AND C.subgroup = D.of_subgroup;
'''):
	d[韻][聲][開合][等][母] = 小韻, 小韻號

格式化小韻小韻號 = lambda 小韻, 小韻號: f'<a href="https://ytenx.org/kyonh/sieux/{小韻號}/">{小韻}</a>'

with open('docs/example/yonhdo.html', 'w') as f:
	f.write( \
'''
<html lang="zh-Hant-HK" xml:lang="zh-Hant-HK" dir="ltr">
<head>
  <meta charset="utf-8"/>
  <title>現代廣韻等韻圖</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no"/>
  <style>
  body { margin: 2em auto; max-width: 50em; }
  h1 { text-align: center; }
  p { text-indent: 2em; }
  a { text-decoration: none; }
  table { border-collapse: collapse; }
  th, td { border: 1px solid black; vertical-align: top; }
  </style>
</head>
<body>
<h1>現代廣韻等韻圖</h1>
<p>重紐單立韻目。韻目順序：東、冬、鍾、江、支、支A、支B、脂、脂A、脂B、之、微、魚、虞、模、齊、佳、皆、灰、咍、眞、眞A、眞B、諄、諄A、臻、文、欣、元、魂、痕、寒、桓、刪、山、先、仙、仙A、仙B、蕭、宵、宵A、宵B、肴、豪、歌、戈、麻、陽、唐、庚、耕、清、清A、青、蒸、登、尤、侯、幽、侵、侵A、侵B、覃、談、鹽、鹽A、鹽B、添、咸、銜、嚴、凡、祭、祭A、祭B、泰、夬、廢。</p>
<table>
''')
	f.write('<tr><th colspan="4"></th><th>幫</th><th>滂</th><th>並</th><th>明</th><th>端</th><th>透</th><th>定</th><th>泥</th><th>知</th><th>徹</th><th>澄</th><th>孃</th><th>精</th><th>清</th><th>從</th><th>心</th><th>邪</th><th>莊</th><th>初</th><th>崇</th><th>生</th><th>俟</th><th>章</th><th>昌</th><th>船</th><th>書</th><th>常</th><th>見</th><th>溪</th><th>羣</th><th>疑</th><th>影</th><th>曉</th><th>匣</th><th>云</th><th>以</th><th>來</th><th>日</th></tr>')
	for 韻 in ('東','冬','鍾','江','支','支A','支B','脂','脂A','脂B','之','微','魚','虞','模','齊','佳','皆','灰','咍','眞','眞A','眞B','諄','諄A','臻','文','欣','元','魂','痕','寒','桓','刪','山','先','仙','仙A','仙B','蕭','宵','宵A','宵B','肴','豪','歌','戈','麻','陽','唐','庚','耕','清','清A','青','蒸','登','尤','侯','幽','侵','侵A','侵B','覃','談','鹽','鹽A','鹽B','添','咸','銜','嚴','凡','祭','祭A','祭B','泰','夬','廢'):
		韻printed = False
		for 聲 in '平上去入':
			聲printed = False
			for 開合 in '開合':
				開合printed = False
				for 等 in range(1, 5):
					幫 = (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda x: '◯' if x is None else 格式化小韻小韻號(*x))(d.get('幫')))(d.get(等)))(d.get(開合)))(d.get(聲)))(d.get(韻))
					滂 = (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda x: '◯' if x is None else 格式化小韻小韻號(*x))(d.get('滂')))(d.get(等)))(d.get(開合)))(d.get(聲)))(d.get(韻))
					並 = (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda x: '◯' if x is None else 格式化小韻小韻號(*x))(d.get('並')))(d.get(等)))(d.get(開合)))(d.get(聲)))(d.get(韻))
					明 = (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda x: '◯' if x is None else 格式化小韻小韻號(*x))(d.get('明')))(d.get(等)))(d.get(開合)))(d.get(聲)))(d.get(韻))
					端 = (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda x: '◯' if x is None else 格式化小韻小韻號(*x))(d.get('端')))(d.get(等)))(d.get(開合)))(d.get(聲)))(d.get(韻))
					透 = (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda x: '◯' if x is None else 格式化小韻小韻號(*x))(d.get('透')))(d.get(等)))(d.get(開合)))(d.get(聲)))(d.get(韻))
					定 = (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda x: '◯' if x is None else 格式化小韻小韻號(*x))(d.get('定')))(d.get(等)))(d.get(開合)))(d.get(聲)))(d.get(韻))
					泥 = (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda x: '◯' if x is None else 格式化小韻小韻號(*x))(d.get('泥')))(d.get(等)))(d.get(開合)))(d.get(聲)))(d.get(韻))
					知 = (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda x: '◯' if x is None else 格式化小韻小韻號(*x))(d.get('知')))(d.get(等)))(d.get(開合)))(d.get(聲)))(d.get(韻))
					徹 = (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda x: '◯' if x is None else 格式化小韻小韻號(*x))(d.get('徹')))(d.get(等)))(d.get(開合)))(d.get(聲)))(d.get(韻))
					澄 = (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda x: '◯' if x is None else 格式化小韻小韻號(*x))(d.get('澄')))(d.get(等)))(d.get(開合)))(d.get(聲)))(d.get(韻))
					孃 = (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda x: '◯' if x is None else 格式化小韻小韻號(*x))(d.get('孃')))(d.get(等)))(d.get(開合)))(d.get(聲)))(d.get(韻))
					精 = (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda x: '◯' if x is None else 格式化小韻小韻號(*x))(d.get('精')))(d.get(等)))(d.get(開合)))(d.get(聲)))(d.get(韻))
					清 = (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda x: '◯' if x is None else 格式化小韻小韻號(*x))(d.get('清')))(d.get(等)))(d.get(開合)))(d.get(聲)))(d.get(韻))
					從 = (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda x: '◯' if x is None else 格式化小韻小韻號(*x))(d.get('從')))(d.get(等)))(d.get(開合)))(d.get(聲)))(d.get(韻))
					心 = (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda x: '◯' if x is None else 格式化小韻小韻號(*x))(d.get('心')))(d.get(等)))(d.get(開合)))(d.get(聲)))(d.get(韻))
					邪 = (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda x: '◯' if x is None else 格式化小韻小韻號(*x))(d.get('邪')))(d.get(等)))(d.get(開合)))(d.get(聲)))(d.get(韻))
					莊 = (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda x: '◯' if x is None else 格式化小韻小韻號(*x))(d.get('莊')))(d.get(等)))(d.get(開合)))(d.get(聲)))(d.get(韻))
					初 = (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda x: '◯' if x is None else 格式化小韻小韻號(*x))(d.get('初')))(d.get(等)))(d.get(開合)))(d.get(聲)))(d.get(韻))
					崇 = (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda x: '◯' if x is None else 格式化小韻小韻號(*x))(d.get('崇')))(d.get(等)))(d.get(開合)))(d.get(聲)))(d.get(韻))
					生 = (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda x: '◯' if x is None else 格式化小韻小韻號(*x))(d.get('生')))(d.get(等)))(d.get(開合)))(d.get(聲)))(d.get(韻))
					俟 = (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda x: '◯' if x is None else 格式化小韻小韻號(*x))(d.get('俟')))(d.get(等)))(d.get(開合)))(d.get(聲)))(d.get(韻))
					章 = (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda x: '◯' if x is None else 格式化小韻小韻號(*x))(d.get('章')))(d.get(等)))(d.get(開合)))(d.get(聲)))(d.get(韻))
					昌 = (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda x: '◯' if x is None else 格式化小韻小韻號(*x))(d.get('昌')))(d.get(等)))(d.get(開合)))(d.get(聲)))(d.get(韻))
					船 = (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda x: '◯' if x is None else 格式化小韻小韻號(*x))(d.get('船')))(d.get(等)))(d.get(開合)))(d.get(聲)))(d.get(韻))
					書 = (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda x: '◯' if x is None else 格式化小韻小韻號(*x))(d.get('書')))(d.get(等)))(d.get(開合)))(d.get(聲)))(d.get(韻))
					常 = (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda x: '◯' if x is None else 格式化小韻小韻號(*x))(d.get('常')))(d.get(等)))(d.get(開合)))(d.get(聲)))(d.get(韻))
					見 = (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda x: '◯' if x is None else 格式化小韻小韻號(*x))(d.get('見')))(d.get(等)))(d.get(開合)))(d.get(聲)))(d.get(韻))
					溪 = (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda x: '◯' if x is None else 格式化小韻小韻號(*x))(d.get('溪')))(d.get(等)))(d.get(開合)))(d.get(聲)))(d.get(韻))
					羣 = (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda x: '◯' if x is None else 格式化小韻小韻號(*x))(d.get('羣')))(d.get(等)))(d.get(開合)))(d.get(聲)))(d.get(韻))
					疑 = (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda x: '◯' if x is None else 格式化小韻小韻號(*x))(d.get('疑')))(d.get(等)))(d.get(開合)))(d.get(聲)))(d.get(韻))
					影 = (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda x: '◯' if x is None else 格式化小韻小韻號(*x))(d.get('影')))(d.get(等)))(d.get(開合)))(d.get(聲)))(d.get(韻))
					曉 = (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda x: '◯' if x is None else 格式化小韻小韻號(*x))(d.get('曉')))(d.get(等)))(d.get(開合)))(d.get(聲)))(d.get(韻))
					匣 = (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda x: '◯' if x is None else 格式化小韻小韻號(*x))(d.get('匣')))(d.get(等)))(d.get(開合)))(d.get(聲)))(d.get(韻))
					云 = (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda x: '◯' if x is None else 格式化小韻小韻號(*x))(d.get('云')))(d.get(等)))(d.get(開合)))(d.get(聲)))(d.get(韻))
					以 = (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda x: '◯' if x is None else 格式化小韻小韻號(*x))(d.get('以')))(d.get(等)))(d.get(開合)))(d.get(聲)))(d.get(韻))
					來 = (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda x: '◯' if x is None else 格式化小韻小韻號(*x))(d.get('來')))(d.get(等)))(d.get(開合)))(d.get(聲)))(d.get(韻))
					日 = (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda d: '◯' if d is None else (lambda x: '◯' if x is None else 格式化小韻小韻號(*x))(d.get('日')))(d.get(等)))(d.get(開合)))(d.get(聲)))(d.get(韻))
					f.write( \
f'''
<tr>
  {f'<td rowspan="32">{韻}</td>' if not 韻printed else ''}<!-- 韻 -->
  {f'<td rowspan="8">{聲}</td>' if not 聲printed else ''}<!-- 聲 -->
  {f'<td rowspan="4">{開合}</td>' if not 開合printed else ''}<!-- 開合 -->
  <td>{'一' if 等 == 1 else '二' if 等 == 2 else '三' if 等 == 3 else '四'}</td><!-- 等 -->
  <td>{幫}</td><!-- 幫 -->
  <td>{滂}</td><!-- 滂 -->
  <td>{並}</td><!-- 並 -->
  <td>{明}</td><!-- 明 -->
  <td>{端}</td><!-- 端 -->
  <td>{透}</td><!-- 透 -->
  <td>{定}</td><!-- 定 -->
  <td>{泥}</td><!-- 泥 -->
  <td>{知}</td><!-- 知 -->
  <td>{徹}</td><!-- 徹 -->
  <td>{澄}</td><!-- 澄 -->
  <td>{孃}</td><!-- 孃 -->
  <td>{精}</td><!-- 精 -->
  <td>{清}</td><!-- 清 -->
  <td>{從}</td><!-- 從 -->
  <td>{心}</td><!-- 心 -->
  <td>{邪}</td><!-- 邪 -->
  <td>{莊}</td><!-- 莊 -->
  <td>{初}</td><!-- 初 -->
  <td>{崇}</td><!-- 崇 -->
  <td>{生}</td><!-- 生 -->
  <td>{俟}</td><!-- 俟 -->
  <td>{章}</td><!-- 章 -->
  <td>{昌}</td><!-- 昌 -->
  <td>{船}</td><!-- 船 -->
  <td>{書}</td><!-- 書 -->
  <td>{常}</td><!-- 常 -->
  <td>{見}</td><!-- 見 -->
  <td>{溪}</td><!-- 溪 -->
  <td>{羣}</td><!-- 羣 -->
  <td>{疑}</td><!-- 疑 -->
  <td>{影}</td><!-- 影 -->
  <td>{曉}</td><!-- 曉 -->
  <td>{匣}</td><!-- 匣 -->
  <td>{云}</td><!-- 云 -->
  <td>{以}</td><!-- 以 -->
  <td>{來}</td><!-- 來 -->
  <td>{日}</td><!-- 日 -->
</tr>
''')
					韻printed = True
					聲printed = True
					開合printed = True
	f.write( \
'''
</table>
<!-- GitHub Corners from http://tholman.com/github-corners/ -->
<a href="https://github.com/sgalal/Guangyun" class="github-corner" aria-label="View source on GitHub"><svg width="80" height="80" viewBox="0 0 250 250" style="fill:#151513; color:#aaa; position: absolute; top: 0; border: 0; right: 0;" aria-hidden="true"><path d="M0,0 L115,115 L130,115 L142,142 L250,250 L250,0 Z"></path><path d="M128.3,109.0 C113.8,99.7 119.0,89.6 119.0,89.6 C122.0,82.7 120.5,78.6 120.5,78.6 C119.2,72.0 123.4,76.3 123.4,76.3 C127.3,80.9 125.5,87.3 125.5,87.3 C122.9,97.6 130.6,101.9 134.4,103.2" fill="currentColor" style="transform-origin: 130px 106px;" class="octo-arm"></path><path d="M115.0,115.0 C114.9,115.1 118.7,116.5 119.8,115.4 L133.7,101.6 C136.9,99.2 139.9,98.4 142.2,98.6 C133.8,88.0 127.5,74.4 143.8,58.0 C148.5,53.4 154.0,51.2 159.7,51.0 C160.3,49.4 163.2,43.6 171.4,40.1 C171.4,40.1 176.1,42.5 178.8,56.2 C183.1,58.6 187.2,61.8 190.9,65.4 C194.5,69.0 197.7,73.2 200.1,77.6 C213.8,80.2 216.3,84.9 216.3,84.9 C212.7,93.1 206.9,96.0 205.4,96.6 C205.1,102.4 203.0,107.8 198.3,112.5 C181.9,128.9 168.3,122.5 157.7,114.1 C157.9,116.9 156.7,120.9 152.7,124.9 L141.0,136.5 C139.8,137.7 141.6,141.9 141.8,141.8 Z" fill="currentColor" class="octo-body"></path></svg></a><style>.github-corner:hover .octo-arm{animation:octocat-wave 560ms ease-in-out}@keyframes octocat-wave{0%,100%{transform:rotate(0)}20%,60%{transform:rotate(-25deg)}40%,80%{transform:rotate(10deg)}}@media (max-width:500px){.github-corner:hover .octo-arm{animation:none}.github-corner .octo-arm{animation:octocat-wave 560ms ease-in-out}}</style>
</body>
</html>
''')
