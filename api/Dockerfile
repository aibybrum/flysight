FROM python:3.10-slim-buster AS build

RUN python3 -m venv /opt/.venv
ENV PATH="/opt/.venv/bin:$PATH"

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get -y install --no-install-recommends libpq-dev build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install -r requirements.txt

FROM python:3.10-slim-buster AS dev

WORKDIR /app
ENV PATH="/opt/.venv/bin:$PATH"
COPY --from=build /opt/.venv /opt/.venv
COPY app/ ./

CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--port=80"]