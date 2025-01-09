uv:
	npm start
brom:
	cd bromine && python3 t.py
install:
	npm install && cd Ultraviolet-Static && npm install && cd .. && npm install ./Ultraviolet-Static && pip3 install -r requirements.txt
uvkill:
	lsof -ti:8080 | xargs kill -9 2>/dev/null || true
ckill:
	lsof -ti:5050 | xargs kill -9 2>/dev/null || true
bkill:
	lsof -ti:5420 | xargs kill -9 2>/dev/null || true
