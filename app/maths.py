def dms_to_dd(data):
    a, b, c = data["GPSLatitude"]
    d, e, f = data["GPSLongitude"]
    lat = a + (b / 60) + (c / 3600)
    long = d + (e / 60) + (c / 3600)
    lat_conv = round(float(lat), 6)
    long_conv = round(float(long), 6)
    if data["GPSLongitudeRef"] == "W":
        long_conv = long_conv * -1
    return lat_conv, long_conv
