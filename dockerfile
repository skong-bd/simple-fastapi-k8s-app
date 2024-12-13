FROM python:3.12-alpine

# Install Poetry
RUN pip install poetry

WORKDIR /code

COPY pyproject.toml poetry.lock /code/

RUN poetry lock --no-update && poetry install --no-root

COPY src /code/src

EXPOSE 80

CMD ["poetry", "run", "fastapi", "run", "src/main.py", "--port", "80"]
