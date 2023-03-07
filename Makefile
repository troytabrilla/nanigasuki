init:
	pip install -r requirements.txt

test:
	python3 -m pytest tests

docker-build:
	docker build -t troytabrilla/nanigasuki:latest --target build .

docker-run:
	docker run --name ngs --network host --rm -it troytabrilla/nanigasuki:latest /bin/bash
