FROM python:3.11-slim

ARG UID=1000
ARG GID=1000

RUN groupadd dev -g $GID && useradd dev -u $UID -g dev -d /home/dev -m

WORKDIR /www

COPY . .

RUN pip install -r requirements.txt

EXPOSE 80

CMD ["streamlit", "run", "app.py", "--server.port", "80"]