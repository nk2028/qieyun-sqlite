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

wget -nc -P build https://cdn.jsdelivr.net/gh/nk2028/qieyun-examples@20200908/unt.js

echo 'const Qieyun = require("qieyun");

function unt(音韻地位) {' > build/unt_modified.js

cat build/unt.js >> build/unt_modified.js

echo '}

console.log("小韻號,unt切韻朗讀音");
for (let sr = 1; sr <= 3874; sr++) {
	const res = unt(Qieyun.get音韻地位(sr));
	console.log(sr + "," + res);
}' >> build/unt_modified.js

# Build unt 切韻朗讀音

node build/unt_modified.js > build/unt.txt

# Remove old artifact

rm -rf qieyun.sqlite3
