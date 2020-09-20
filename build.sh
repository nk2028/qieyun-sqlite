#!/bin/sh

# Prepare ytenx data

wget -nc -P build https://raw.githubusercontent.com/BYVoid/ytenx/master/ytenx/sync/kyonh/YonhMiuk.txt
wget -nc -P build https://raw.githubusercontent.com/BYVoid/ytenx/master/ytenx/sync/kyonh/SieuxYonh.txt
wget -nc -P build https://raw.githubusercontent.com/BYVoid/ytenx/master/ytenx/sync/kyonh/YonhMux.txt
wget -nc -P build https://raw.githubusercontent.com/BYVoid/ytenx/master/ytenx/sync/kyonh/Dzih.txt
wget -nc -P build https://raw.githubusercontent.com/BYVoid/ytenx/master/ytenx/sync/kyonh/YonhGheh.txt
wget -nc -P build https://raw.githubusercontent.com/BYVoid/ytenx/master/ytenx/sync/kyonh/PrengQim.txt
wget -nc -P build https://raw.githubusercontent.com/BYVoid/ytenx/master/ytenx/sync/kyonh/Dauh.txt

# Prepare unt 切韻朗讀音

wget -nc -P build https://raw.githubusercontent.com/nk2028/qieyun-examples/master/unt.js

echo 'const Qieyun = require("qieyun");

function unt(音韻地位) {' > build/unt_modified.js

cat build/unt.js >> build/unt_modified.js

echo '}

console.log("小韻號,unt切韻朗讀音");
[...Array(3874).keys()].map(i => {
	const sr = i + 1;
	const res = unt(Qieyun.get音韻地位(sr));
	console.log(sr + "," + res);
});' >> build/unt_modified.js

# Build unt 切韻朗讀音

node build/unt_modified.js > build/unt.txt

# Remove old artifact

rm -rf data.sqlite3
