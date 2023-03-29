# flysight

# Trash functions

def divide_dataset(l, n):
        for i in range(0, len(l), n):
            yield l[i:i + n]

def request_earth_elevation(x):
    s = "https://api.open-elevation.com/api/v1/lookup?locations="
    for i in range(x.index.start, x.index.stop): 
        s += str(x.lat[i]) + "," + str(x.lon[i]) + "|"
    r = requests.get(s[:-1])  
    if r.status_code == 200:
        elevation = pd.json_normalize(r.json(), 'results')['elevation']
        return elevation
    else:
        print(r)
        
def get_earth_elevation():
    l = []
    divided_dataset = list(divide_dataset(dataset, 120))
    for i in range(0, len(divided_dataset)):
        l.append(request_earth_elevation(divided_dataset[i]).values)
        time.sleep(0.07)
    return list(itertools.chain(*l))

def get_dynamic_elevation():
    ground_elevation = meters_to_feet(dataset.hMSL.iloc[-1])
    earth_elevation = [meters_to_feet(e) for e in get_earth_elevation()]
    l = []
    for i in range(0, len(dataset.hMSL)):
        l.append(meters_to_feet(dataset.hMSL[i]) - ground_elevation - earth_elevation[i])
    return l

---

@app.get("/measurements/{tag_key}/{tag_value}")
async def get_measurements(tag_key: str, tag_value: str):
    query_api = client.query_api()
    query = f'from(bucket:"your-bucket") |> range(start: -1h) |> filter(fn: (r) => r._field == "{tag_key}" and r._value == "{tag_value}") |> group(columns: ["_measurement"])'
    result = query_api.query(query)
    measurements = [m["_value"] for m in result[0].records]
    return {"measurements": measurements}

@app.put("/data/{measurement}")
async def update_data(measurement: str, value: float):
    write_api = client.write_api()
    point = Point(measurement).field("value", value).time(datetime.utcnow())
    write_api.write(bucket="your-bucket", record=point)
    return {"message": "Data updated successfully"}



give me a Dockerfile with build and dev stage for a fastapi with the following requirements:

SQLAlchemy==1.3.22
uvicorn==0.21.1
influxdb-client==1.36.1
pandas==1.5.2
geopy==2.3.0
peakutils==1.3.4
pyproj==3.4.1
python-dotenv==0.21.1
utm==0.7.0
bcrypt==4.0.1

FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

COPY requirements.txt ./

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./ ./

CMD ["uvicorn", "app.main:app", "--host=0.0.0.0", "--port=80"]


the following dockerfile is about 434MB. Can you reduce it, but not change the multistage images?

# Stage 1: build environment
FROM python:3.10-slim AS build-env

WORKDIR /app

COPY requirements.txt ./
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get -y install --no-install-recommends libpq-dev build-essential && \
    pip install --no-cache-dir --prefix=/install -r requirements.txt && \
    rm -rf /root/.cache /usr/local/lib/python3.10/site-packages/__pycache__

COPY ./ ./

# Stage 2: production environment
FROM python:3.10-slim

RUN apt-get update && \
    apt-get -y install --no-install-recommends libpq5 && \
    rm -rf /var/lib/apt/lists/*

COPY --from=build-env /install /usr/local
COPY --from=build-env /app ./

CMD ["uvicorn", "app.main:app", "--host=0.0.0.0", "--port=80"]

fastapi==0.95.0
psycopg2==2.9.5
sqlalchemy==1.3.22
uvicorn==0.21.1
influxdb-client==1.36.1
pandas==1.5.3
numpy==1.23.5
geopy==2.3.0
peakutils==1.3.4
pyproj==3.4.1
python-dotenv==0.21.1
utm==0.7.0
bcrypt==4.0.1
python-multipart==0.0.6



the following dockerfile gives me the following error can you fix it? requirements.txt us also given

from . import _bcrypt  # noqa: I100
ImportError: Error loading shared library ld-linux-x86-64.so.2: No such file or directory (needed by /opt/venv/lib/python3.10/site-packages/bcrypt/_bcrypt.abi3.so)

# Stage 1: build environment
FROM python:3.10-slim AS build-env

WORKDIR /app

COPY requirements.txt ./

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get -y install --no-install-recommends libpq-dev build-essential && \
    python -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt && \
    rm -rf /root/.cache /opt/venv/lib/python*/site-packages/__pycache__

COPY ./ ./

# Stage 2: production environment
FROM python:3.10-alpine

RUN apk add --no-cache libpq libgcc && \
    addgroup -S appgroup && \
    adduser -S appuser -G appgroup && \
    apk add --no-cache libc6-compat

WORKDIR /app

COPY --from=build-env /opt/venv /opt/venv
COPY --from=build-env /app ./

USER appuser

CMD ["/opt/venv/bin/uvicorn", "app.main:app", "--host=0.0.0.0", "--port=80"]

# Angular

npm install -g @angular/cli
ng new my-app
