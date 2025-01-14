uv:
	PORT=8000 npm start
brom:
	cd bromine && python3 t.py
install:
	npm install && cd Ultraviolet-Static && npm install && cd .. && npm install ./Ultraviolet-Static && pip3 install -r requirements.txt
uvkill:
	lsof -ti:8000 | xargs kill -9 2>/dev/null || true
ckill:
	lsof -ti:7272 | xargs kill -9 2>/dev/null || true
bkill:
	lsof -ti:7420 | xargs kill -9 2>/dev/null || true
nodeclean:
	rm -rf node
npmclean:
	rm -rf node_modules && rm -rf Ultraviolet-Static/node_modules