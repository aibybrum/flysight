# Stage 1: build environment
FROM python:3.10-slim-buster AS build-env

WORKDIR /app

COPY requirements.txt ./
RUN apt-get update && apt-get upgrade -y && \
    apt-get -y install --no-install-recommends libpq-dev build-essential && \
    pip install --no-cache-dir --prefix=/install -r requirements.txt && \
    rm -rf /root/.cache /usr/local/lib/python3.10/site-packages/__pycache__

COPY ./ ./

# Stage 2: production environment
FROM python:3.10-slim-buster AS dev-env

WORKDIR /app

RUN apt-get update && \
    apt-get -y install --no-install-recommends libpq5 && \
    rm -rf /var/lib/apt/lists/*

COPY --from=build-env /install /usr/local
COPY --from=build-env /app ./

CMD ["uvicorn", "app.main:app", "--host=0.0.0.0", "--port=80"]