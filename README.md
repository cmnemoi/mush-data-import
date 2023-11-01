# Mush Data Import

Application to save [Mush](http://mush.twinoid.com/) data before site closure 

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://mush-import-app-5rfxyxktrq-ew.a.run.app/)

## Run locally

### On bare metal
You need [Python 3.11](https://www.python.org/downloads/release/python-3116/) to run this application. Create a virtual environment and install the requirements:

Create a virtual environment and install the requirements:

```bash
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

You can also use [pyenv](https://github.com/pyenv/pyenv#automatic-installer) to install Python and [poetry](https://python-poetry.org/docs/) to install dependencies if that is your thing :

If you have `make` installed, just run `make` to install and start the application.

```bash
pyenv install 3.11
pyenv local 3.11
poetry install
poetry shell
```

Then run the application:

```bash
streamlit run app.py
```

### With Docker

If you have `make` installed :

```bash
make docker-build
make docker-run
```

Otherwise :

Build the image:

```bash
docker build -t mush-import-app .
```

Run the container:

```bash
docker run \
	--name mush-import-app \
	--publish 80:80 \ # Map port 80 of the host to port 80 in the container
	--volume .:/www \ # Mount current directory to /www in the container so that changes are reflected in real time
	--add-host mush.twinoid.es:178.32.123.64 \ # Support Mush Spanish server
	--add-host data.mush.twinoid.es:178.32.123.64 \ # Support Mush Spanish server
	mush-import-app:latest
```

## Extra docs

- Setup your Big Query database with Streamlit https://docs.streamlit.io/knowledge-base/tutorials/databases/bigquery

- You can deploy the app to Cloud Run with the [`Dockerfile_CloudRun`](Dockerfile_CloudRun) file with this tutorial : https://medium.com/@faizififita1/how-to-deploy-your-streamlit-web-app-to-google-cloud-run-ba776487c5fe

- You can alternatively deploy to Streamlit Cloud, which is way easier, but it won't support Spanish server profiles : hhttps://docs.streamlit.io/streamlit-community-cloud/get-started/quickstart