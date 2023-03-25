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



how to send a dataframe in response by using fastapi schema

can you give me a fastapi response schema for dataframe with to_json
