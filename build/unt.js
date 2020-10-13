const Qieyun = require('qieyun');
const QieyunExamples = require('qieyun-examples-node');

console.log('小韻號,unt切韻朗讀音');

for (let sr = 1; sr <= 3874; sr++) {
	const res = QieyunExamples.unt(Qieyun.get音韻地位(sr));
	console.log(sr + ',' + res);
}
