FROM python:3.10-slim-buster as build-image

WORKDIR /app
RUN pip install --upgrade pip

COPY app/requirements.txt ./
RUN pip install -r requirements.txt
COPY app/ ./
  
CMD [ "gunicorn", "--workers=5", "--threads=1", "-b 0.0.0.0:80", "app:server"]