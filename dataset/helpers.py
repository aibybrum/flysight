from math import radians, cos, sin, asin, sqrt, degrees, atan

def divide_dataset(l, n):
        for i in range(0, len(l), n):
            yield l[i:i + n]

def meters_to_feet(meters):
    return meters * 3.280839895

def feet_to_meters(feet):
    return feet / 3.280839895

def meterpersecond_to_milesperhour(meterpersecond):
    return meterpersecond * 2.236936

def meterpersecond_to_kilometersperhour(meterpersecond):
    return meterpersecond * 3.6

def calc_horizontal_speed(n, e):
        return sqrt((n**2) + (e**2))

def calc_dive_angle(v_speed, h_speed):
        return degrees(atan(v_speed/h_speed))

def calc_distance(lat1, lat2, lon1, lon2):
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)
        
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    
    c = 2 * asin(sqrt(a))
        
    # Radius of earth in kilometers. Use 3956 for miles
    r = 6371
    
    # calculate the result
    return meters_to_feet((c * r) * 1000)