import os
from PIL import Image, ImageDraw, ImageFont
from PIL.ExifTags import TAGS, GPSTAGS

def get_exif_data(image):
    try:
        exif = image._getexif()
        if exif is not None:
            exif_data = {TAGS.get(tag): value for tag, value in exif.items() if tag in TAGS}
            return exif_data
    except (AttributeError, KeyError, IndexError):
        pass
    return None

def get_geotagging(exif_data):
    if 'GPSInfo' in exif_data:
        gps_info = exif_data['GPSInfo']
        for key in list(gps_info.keys()):
            name = GPSTAGS.get(key, key)
            gps_info[name] = gps_info.pop(key)
        return gps_info

def format_coordinates(coordinates):
    latitude = [str(coord) for coord in coordinates['GPSLatitude']]
    longitude = [str(coord) for coord in coordinates['GPSLongitude']]
    return f"Latitude: {' '.join(latitude)}, Longitude: {' '.join(longitude)}"

directory = "C:/Users/admin/Desktop/autoGPS"
files = os.listdir(directory)

for file in files:
    if file.lower().endswith((".jpg", ".png")):
        try:
            image = Image.open(os.path.join(directory, file))
            exif_data = get_exif_data(image)
            if exif_data:
                geotags = get_geotagging(exif_data)
                if geotags:
                    gps_info = format_coordinates(geotags)
                    draw = ImageDraw.Draw(image)
                    text = gps_info
                    position = (10, 10)
                    font = ImageFont.truetype("arial.ttf", 100)
                    draw.text(position, text, fill="black", font=font)
                    image.save(os.path.join(directory, "output_" + file))
            else:
                print(f"No GPS data found in {file}")
        except Exception as e:
            print(f"An error occurred with file {file}: {e}")

print("Processing complete.")
