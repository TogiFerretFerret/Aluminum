uv:
	PORT=8000 npm start
brom:
	cd bromine && python3 t.py
install:
	npm install && cd Ultraviolet-Static && npm install && cd .. && npm install ./Ultraviolet-Static && pip3 install -r requirements.txt
uvkill:
	lsof -ti:8000 | xargs kill -9 2>/dev/null || true
ckill:
	lsof -ti:5050 | xargs kill -9 2>/dev/null || true
bkill:
	lsof -ti:5420 | xargs kill -9 2>/dev/null || true
linuxbuild:
	node --experimental-sea-config sea-config.json && cd dist && cp $(command -v node) finalapp && npx postject finalapp NODE_SEA_BLOB uv-app --sentinel-fuse NODE_SEA_FUSE_fce680ab2cc467b6e072b8b5df1996b2