from math import sqrt, degrees, atan
import geopy.distance
import pyproj
import utm


def meters_to_feet(meters):
    return meters * 3.280839895


def feet_to_meters(feet):
    return feet / 3.280839895


def meter_per_second_to_miles_per_hour(meter_per_second):
    return meter_per_second * 2.236936


def meter_per_second_to_kilometers_per_hour(meter_per_second):
    return meter_per_second * 3.6


def calc_horizontal_speed(n, e):
    return sqrt((n**2) + (e**2))


def calc_dive_angle(v_speed, h_speed):
    try:
        return degrees(atan(v_speed/h_speed))
    except ZeroDivisionError:
        return 0


def calc_distance_geo(metric, lat1, lat2, lon1, lon2):
    coordinates_1 = (lat1, lon1)
    coordinates_2 = (lat2, lon2)
    if metric == 'ft':
        return geopy.distance.geodesic(coordinates_1, coordinates_2).miles * 5280
    elif metric == 'm':
        return geopy.distance.geodesic(coordinates_1, coordinates_2).kilometers * 1000


def to_utm(lat, lon):
    zone = utm.from_latlon(lat[0], lon[0])[2]
    p = pyproj.Proj(proj='utm', zone=zone, ellps='WGS84')
    return p(lon, lat)


def calc_axis_distance(metric, lat, lon):
    x, y = to_utm(lat, lon)
    if metric == 'ft':
        return [meters_to_feet(x_cor) for x_cor in x], [meters_to_feet(y_cor) for y_cor in y]
    elif metric == 'm':
        return x, y
        