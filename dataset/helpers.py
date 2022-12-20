from math import radians, cos, sin, asin, sqrt, degrees, atan
import geopy.distance

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
    try:
        return degrees(atan(v_speed/h_speed))
    except ZeroDivisionError:
        return 0   

def cal_distance_geo(lat1, lat2, lon1, lon2):
    coords_1 = (lat1, lon1)
    coords_2 = (lat2, lon2)
    return geopy.distance.geodesic(coords_1, coords_2).miles