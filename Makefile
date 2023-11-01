all: install run

docker-bash:
	docker exec -it mush-import-app bash

docker-build:
	docker build -t mush-import-app:latest .

docker-remove: docker-stop
	docker rm mush-import-app

docker-run:
	docker run \
	--name mush-import-app \
	--publish 80:80 \
	--volume .:/www \
	--add-host mush.twinoid.es:178.32.123.64 \
	--add-host data.mush.twinoid.es:178.32.123.64 \
	mush-import-app:latest

docker-start:
	docker start mush-import-app

docker-stop:
	docker stop mush-import-app

install: setup-env-variables
	poetry install

run:
	poetry run streamlit run app.py

setup-env-variables:
	cp .streamlit/secrets.example.toml .streamlit/secrets.toml
