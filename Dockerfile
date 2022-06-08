FROM python:3.9-slim

ENV POETRY_HOME="/opt/poetry" \
    POETRY_NO_INTERACTION=1 

ENV PATH="$POETRY_HOME/bin:$SRC_PATH/.venv/bin:$PATH"

RUN apt-get update && \
    apt-get -y install curl libmagic-dev

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

COPY ./poetry.lock ./pyproject.toml ./

RUN POETRY_VIRTUALENVS_CREATE=false poetry install

WORKDIR /app

COPY . .

RUN useradd appuser
RUN chown -R appuser:appuser /app/static/
USER appuser

CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--port=8080", "--app-dir=app"]