from dotenv import load_dotenv
from fastapi import FastAPI, Request, UploadFile
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import logging
import magic
import os
from scrape import get_exif, get_geo
from maths import dms_to_dd
from openlocationcode import encode
import urllib.parse


app = FastAPI()
load_dotenv()
templates = Jinja2Templates(directory="templates/")
app.mount("/static", StaticFiles(directory="static"), name="static")
favicon_path = "favicon.ico"
logging.getLogger().setLevel(logging.INFO)


@app.get("/")
def get_main(request: Request):
    return templates.TemplateResponse(
        "index.html",
        context={"request": request},
    )


@app.post("/")
async def post_main(request: Request, filename: UploadFile, webpage="result.html"):
    data = ""
    url = ""

    # Write the uploaded file to the local filesystem
    with open("/app/static/image.jpg", "wb") as image:
        image.write(await filename.read())

    # Here we are checking if we have an image with Exif data. If not, display the nodata.html site
    # and pass along a message.
    if "image" and "Exif" not in magic.from_file("/app/static/image.jpg"):
        logging.error("This aint compatible dog")
        logging.info(f'Image type: {magic.from_file("/app/static/image.jpg")}')
        data = "Sorry, no EXIF data was found."
        webpage = "nodata.html"
    else:
        # Main workflow. Extract Exif data, then extract GPS data. Check for scrubbed GPS data.
        # If valid GPS data, convert from Degree Minute Second to Direct Decimal
        # Then convert Direct Decimal to PlusCode, and encode it.
        # Construct IFrame URL and pass to Jinja template as url variable.
        logging.info(f'Image type: {magic.from_file("/app/static/image.jpg")}')
        exif = get_exif()
        data = get_geo(exif)
        logging.info(data)
        if "GPSLatitude" in data.keys():
            a, b, c = data["GPSLatitude"]
            if str(a) == "nan":
                logging.info("nan detected")
                data = "Sorry, no GPS data was found."
                webpage = "nodata.html"
            else:
                lat, long = dms_to_dd(data)
                logging.info(f"Coords: {lat}, {long}")
                plus_code = encode(lat, long)
                encoded_pc = urllib.parse.quote(plus_code)
                logging.info(f"Encoded PlusCode: {encoded_pc}")
                url = f"https://www.google.com/maps/embed/v1/place?key={os.environ['API_KEY']}&q={encoded_pc}&maptype=satellite"
        else:
            data = "Sorry, no GPS data was found."
            webpage = "nodata.html"

    return templates.TemplateResponse(
        webpage,
        context={"request": request, "data": data, "url": url},
    )
