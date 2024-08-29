FROM python:3.9 as requirements-stage

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes --only api


FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

WORKDIR /app/api

COPY --from=requirements-stage /tmp/requirements.txt /app/api/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/api/requirements.txt

COPY ./api /app/api

EXPOSE 80

CMD ["uvicorn", "api.app.main:app", "--host", "0.0.0.0", "--port", "80"]