from shapely.geometry import Point, Polygon
restricted_zone = Polygon([
    (-13.25, 8.45),
    (-13.20, 8.45),
    (-13.20, 8.50),
    (-13.25, 8.50)
])
def check_restricted_zone(lat, lon):

    point = Point(lon, lat)

    return restricted_zone.contains(point)
if __name__ == "__main__":

    test_lat = 8.47
    test_lon = -13.23

    result = check_restricted_zone(test_lat, test_lon)

    print("Aircraft in restricted zone:", result)