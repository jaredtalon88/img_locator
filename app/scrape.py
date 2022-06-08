from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS


def get_exif():
    with open("/app/static/image.jpg", "rb") as src:
        img = Image.open(src)
        return img.getexif()


def get_geo(exif):
    for key, value in TAGS.items():
        if value == "GPSInfo":
            break
    gps_info = exif.get_ifd(key)
    return {GPSTAGS.get(key, key): value for key, value in gps_info.items()}
