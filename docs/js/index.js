'use strict';

/* CodeMirror - codeInputArea */

let codeInputArea;

document.addEventListener('DOMContentLoaded', () => {
	codeInputArea = CodeMirror(scriptInput, {
		value: 'const is = s => check小韻(小韻號, s);\n\n// Your script goes here\n',
		mode: 'javascript',
		theme: 'blackboard-modified',
		lineNumbers: true
	});
});

/* Predefined Scripts */

async function selectPredefinedScripts() {
	const v = predefinedScripts.value;

	let url;
	if (v == 'kuxyonh')
		url = 'high_level/kuxyonh.js';
	else if (v == 'ayaka2019')
		url = 'high_level/ayaka2019.js';
	else if (v == 'kuxyonh-ll')
		url = 'low_level/kuxyonh.js';
	else if (v == 'ayaka2019-ll')
		url = 'low_level/ayaka2019.js';
	else
		return;

	const response = await fetch('example/' + url);
	const text = await response.text();
	codeInputArea.setValue(text);
	handleDefineScript();
}

/* Brogue2 function */

let brogue2;

function handleDefineScript() {
	try {
		brogue2 = new Function('小韻號', codeInputArea.getValue());
	} catch (err) {
		notify(err.message);
	}
}

/* Predefined Options */

function handlePredefinedOptions() {
	try {
		if (predefinedOptions.value == 'exportAllSmallRhymes') {
			outputArea.innerText = [...Array(3874).keys()].map(i => {
				const [小韻名, 韻, 母, 開合, 等] = small_rhymes[i];
				return (i + 1) + ' ' + 小韻名 + ' ' + 韻 + 母 + 開合 + 等 + ' ' + brogue2(i + 1);
			}).join('\n');
			outputArea.handleArticle = null;
		} else if (predefinedOptions.value == 'exportAllSyllables') {
			outputArea.innerText = [...new Set([...Array(3874).keys()].map(i => {
				const [小韻名, 韻, 母, 開合, 等] = small_rhymes[i];
				return brogue2(i + 1);
			}))].join(', ');
			outputArea.handleArticle = null;
		} else if (predefinedOptions.value == 'convertArticle')
			handleArticle();
		else
			outputArea.innerHTML = '';
	} catch (err) {
		notify(err.message);
	}
}

/* Converter */

function makeLongStr(sr) {
	const [小韻名, 韻, 母, 開合, 等] = small_rhymes[sr - 1];
	return 韻 + 開合 + 等 + 母;
}

function makeTooltip(ch, pronunciation, sr, expl) {
	const div = document.createElement('div');
	div.classList.add('tooltip-item');
	div.innerText = ch + ' ' + pronunciation + ' ' + makeLongStr(sr) + ' ' + expl;
	return div;
}

function makeNoEntry(ch) {
	const outerContainer = document.createElement('div');
	outerContainer.classList.add('entry');
	outerContainer.classList.add('entry-no');
	outerContainer.innerText = ch;
	outerContainer.handleExport = () => ch;

	return outerContainer;
}

function makeSingleEntry(ch, res) {
	const [sr, expl] = res;
	const pronunciation = brogue2(sr);

	const outerContainer = document.createElement('div');
	outerContainer.classList.add('entry');
	outerContainer.classList.add('entry-single');

	const ruby = document.createElement('ruby');
	const rb = document.createElement('rb');
	rb.innerText = ch;
	ruby.appendChild(rb);

	const tooltipContainer = document.createElement('div');
	tooltipContainer.classList.add('tooltip-container');

	const rt = document.createElement('rt');
	rt.lang = 'zh-Latn';
	rt.setAttribute('xml:lang', 'zh-Latn');
	rt.innerText = pronunciation;
	ruby.appendChild(rt);

	const tooltip = makeTooltip(ch, pronunciation, sr, expl);
	tooltipContainer.appendChild(tooltip);

	outerContainer.appendChild(ruby);
	outerContainer.appendChild(tooltipContainer);
	const exportText = ch + '(' + pronunciation + ')';
	outerContainer.handleExport = () => exportText;

	return outerContainer;
}

function makeMultipleEntry(ch, ress) {
	const outerContainer = document.createElement('div');
	outerContainer.classList.add('entry');
	outerContainer.classList.add('entry-multiple');
	outerContainer.classList.add('unresolved');

	const ruby = document.createElement('ruby');
	const rb = document.createElement('rb');
	rb.innerText = ch;
	ruby.appendChild(rb);

	const tooltipContainer = document.createElement('div');
	tooltipContainer.classList.add('tooltip-container');

	let rtArray = [];
	let tooltipArray = [];

	for (let i = 0, len = ress.length; i < len; i++) {
		const res = ress[i];
		const [sr, expl] = res;
		const pronunciation = brogue2(sr);

		const rt = document.createElement('rt');
		rt.lang = 'zh-Latn';
		rt.setAttribute('xml:lang', 'zh-Latn');
		rt.innerText = pronunciation;

		ruby.appendChild(rt);
		rtArray.push(rt);

		const tooltip = makeTooltip(ch, pronunciation, sr, expl);
		tooltip.addEventListener('click', () => {
			rtArray.map(rt => rt.classList.add('hidden'));
			rt.classList.remove('hidden');

			outerContainer.currentSelection = pronunciation;
			outerContainer.classList.remove('unresolved');

			tooltipArray.map(tooltip => tooltip.classList.remove('selected'));
			tooltip.classList.add('selected');
		});
		tooltipContainer.appendChild(tooltip);
		tooltipArray.push(tooltip);

		if (i == 0) {
			outerContainer.currentSelection = pronunciation;
			tooltip.classList.add('selected');
		} else {
			rt.classList.add('hidden');
		}
	}

	outerContainer.appendChild(ruby);
	outerContainer.appendChild(tooltipContainer);
	outerContainer.handleExport = () => ch + '(' + outerContainer.currentSelection + ')';

	return outerContainer;
}

function makeConversion(c) {
	const res = char_entities[c];
	if (!res)
		return makeNoEntry(c);
	else if (res.length == 1)
		return makeSingleEntry(c, res[0]);
	else
		return makeMultipleEntry(c, res);
}

function handleArticle() {
	outputArea.innerHTML = '';

	const convertText = articleInput.value;
	if (convertText.length == 0) {
		;
	} else {
		const newOutputArea = document.createElement('div');
		convertText.split('').map(n => {
			newOutputArea.appendChild(makeConversion(n));
			newOutputArea.appendChild((() => { const n = document.createTextNode(' '); n.handleExport = () => ''; return n; })());
		});
		newOutputArea.handleExport = () => [...newOutputArea.childNodes].map(node => node.handleExport()).join('');
		const oldOutputArea = outputArea;
		outputArea.id = '';
		newOutputArea.id = 'outputArea';
		oldOutputArea.replaceWith(newOutputArea);
	}
}

function handleCopy() {
	const text = !outputArea.handleExport ? outputArea.innerText : outputArea.handleExport();

	navigator.clipboard.writeText(text).then(() => {
		notify('已成功匯出至剪貼簿。');
	}, () => {
		notify('匯出至剪貼簿失敗。');
	});
}
