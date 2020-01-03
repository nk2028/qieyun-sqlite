/* Display a notification box on the screen.
 * Usage: notify(str)
 */

function styleToElement(styleCss) {
	var styleSheet = document.createElement('style');
	styleSheet.innerHTML = styleCss;
	return styleSheet;
}

// https://stackoverflow.com/a/35385518
function htmlToElement(html) {
	var template = document.createElement('template');
	html = html.trim();  // Never return a text node of whitespace as the result
	template.innerHTML = html;
	return template.content.firstChild;
}

document.addEventListener('DOMContentLoaded', () => {
	document.head.appendChild(styleToElement(`#notificationWrapper {
	background-color: rgba(0,0,0,0.5);
	display: none;
	height: 100vh;
	left: 0;
	position: fixed;
	top: 0;
	width: 100vw;
}

#notificationWrapper.notification-flex {
	align-items: center;
	display: flex;
	justify-content: center;
	z-index: 4;
}

.notificationOutput {
	background-color: black;
	border: 1px solid white;
	max-width: 42em;
	padding: 0.5em 1em;
	text-align: center;
	width: 70vw;
}

#notificationText {
	text-align: left;
}
`));

	document.body.appendChild(htmlToElement(`<div id="notificationWrapper" lang="en-HK">
	<div class="notificationOutput">
		<pre id="notificationText"></pre>
		<p><input type="button" value="確定" onclick="handleNotification()"/></p>
	</div>
</div>`));
});

function notify(str) {
	notificationText.innerText = str;
	notificationWrapper.classList.add('notification-flex');
}

function handleNotification() {
	notificationWrapper.classList.remove('notification-flex');
	notificationText.innerText = '';
}
