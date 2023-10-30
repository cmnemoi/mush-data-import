FROM python:3.11

ARG POETRY_VERSION=1.6.1

WORKDIR /www

RUN curl -sSL https://install.python-poetry.org | python3 - --version ${POETRY_VERSION}

COPY poetry.lock pyproject.toml ./

ENV PATH="${PATH}:/root/.local/bin"

RUN poetry config virtualenvs.create true \
    && poetry install --no-dev --no-interaction --no-ansi

EXPOSE 80

CMD ["poetry", "run", "streamlit", "run", "app.py", "--server.port", "80"]