uv:
	npm start
brom:
	cd bromine && python3 t.py
install:
	npm install && cd Ultraviolet-Static && npm install && cd .. && npm install ./Ultraviolet-Static && pip3 install -r requirements.txt
uvkill:
	fuser -k 8080/tcp
ckill:
	fuser -k 5050/tcp
bkill:
	fuser -k 5000/tcp