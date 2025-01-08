uv:
	cd ultraviolet-app && npm start
brom:
	cd bromine && python3 t.py
run:
	make uv & make brom
install:
	npm install && cd Ultraviolet-Static && npm install && cd .. && npm install ./Ultraviolet-Static && pip3 install -r requirements.txt