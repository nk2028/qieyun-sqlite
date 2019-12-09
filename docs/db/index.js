'use strict';

/* Global Utilities */

const escapeHTML = str => {
	const elem = document.createElement('p');
	elem.innerText = str;
	return elem.innerHTML;
}

const mkTable = (xs, yss) => {
	const mkTh = str => '<th>' + escapeHTML(str) + '</th>'
		, mkThead = xs => '<thead><tr>' + xs.map(mkTh).join('') + '</tr></thead>'
		, mkTd = str => '<td>' + escapeHTML(str) + '</td>'
		, mkTr = ys => '<tr>' + ys.map(mkTd).join('') + '</tr>'
		, mkTbody = yss => '<tbody>' + yss.map(mkTr).join('') + '</tbody>';
	return '<div class="table-wrapper"><table>'
		+ mkThead(xs) + mkTbody(yss)
		+ '</table></div>';
}

const mkTableFromSqlResult = xs => mkTable(xs.columns, xs.values);  // Handle data from sql.js

const mkTablesFromSqlResult = xss => !xss.length
	? '<p>The query produces no result.</p>'
	: xss.map(mkTableFromSqlResult).join('');

/* Query handler */

const handleCustomQuery = () => {
	let res;
	try {
		res = db.exec(myCodeMirror.getValue());
	} catch (error) {
		errorOutput.innerText = error;
		wrapperOutput.innerText = '';
		return;
	}
	errorOutput.innerText = '';
	wrapperOutput.innerHTML = mkTablesFromSqlResult(res);
}

/* Load sql.js and initialize data table */

let db;

const databaseLoaded = (async () => {
	// Fetch Guangyun database
	const databaseFileLoaded = fetch('../data.sqlite3');

	// Wait for sql.js loaded
	await initSqlJs({ locateFile: url => 'https://kripken.github.io/sql.js/dist/sql-wasm.wasm' });

	// Wait for Guangyun database loaded
	const response = await databaseFileLoaded;
	if (!response.ok)
		alert(`Failed to load database.`);
	else {
		// Write database to the global variable
		db = new SQL.Database(new Uint8Array(await response.arrayBuffer()));
	}
})()

/* Page Loaded Event */

let myCodeMirror;

document.addEventListener('DOMContentLoaded', () => {
	myCodeMirror = CodeMirror(customSqlInput, {
		value: `-- Your code goes here

SELECT name, type
FROM sqlite_master
WHERE type IN ('table', 'view');

-- Examples

-- 找出沒有反切的小韻

SELECT 小韻號, 音韻地位, 上字, 下字,
group_concat(字頭, '') AS 字頭
FROM 廣韻字頭全
WHERE 上字 IS NULL
OR 下字 IS NULL
GROUP BY 小韻號;

-- 找出前 5 組具有相同名字的小韻

SELECT 小韻, group_concat(小韻全名) AS 小韻全名
FROM 廣韻小韻全
GROUP BY 小韻
HAVING count(*) > 1
ORDER BY 小韻號
LIMIT 5;		
`,
		mode: 'sql',
		theme: 'blackboard-modified',
		lineNumbers: true
	});
});

window.addEventListener('load', async e => {
	await databaseLoaded;

	// Unblur the page
	document.body.classList.add('unblur');
})
