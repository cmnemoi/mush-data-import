all: install run

install: setup-env-variables
	poetry install

docker-build:
	docker build -t mush-import-app:latest .

docker-remove: docker-stop
	docker rm mush-import-app

docker-run:
	docker run \
	--name mush-import-app \
	--publish 80:8501 \
	--volume .:/www \
	mush-import-app:latest

docker-start:
	docker start mush-import-app

docker-stop:
	docker stop mush-import-app

run: run-app

run-api:
	poetry run uvicorn api:api --reload

run-app:
	poetry run streamlit run app.py

setup-env-variables:
	cp .streamlit/secrets.example.toml .streamlit/secrets.toml
