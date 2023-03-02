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
