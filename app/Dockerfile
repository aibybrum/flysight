FROM python:3.10-slim-buster AS build

RUN python3 -m venv /opt/.venv
ENV PATH="/opt/.venv/bin:$PATH"

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get -y install --no-install-recommends libpq-dev build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt ./
RUN pip install -r requirements.txt

FROM python:3.10-slim-buster AS dev

ENV PATH="/opt/.venv/bin:$PATH"
COPY --from=build /opt/.venv /opt/.venv
COPY ./ ./
CMD [ "gunicorn", "--workers=5", "--threads=1", "-b 0.0.0.0:80", "app:server"]