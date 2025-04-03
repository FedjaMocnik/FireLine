import warnings
warnings.filterwarnings("ignore", message="Signature .* does not match any known type") # To filter warning from numpy

from coord2img.utils.geojson_tools import *
from coord2img.obdelava.data_generation import get_data
from cop2cell_skripte.png2Forest import *
from cop2cell_skripte.api2Weather import *

# Creates .geojson file from coordinates
# SMALL AREAS ONLY as too many requests are rejected
# koordinate tivoli:(456231.740204,5102686.348333),(461467.877750,5099408.768305)
latitude1 = 456231.740204
longitude1 = 5102686.348333
latitude2 = 461467.877750
longitude2 = 5099408.768305
create_geojson_rectangle((latitude1,longitude1),(latitude2, longitude2))

# Gets data form setelites and saves it to coord2img/results
get_data()


# PREBERI PODATKE IZ GEOJSON
with open("coord2img/results/new_area.geojson", "r") as f:
    geojson_data = json.load(f)

polygon = shape(geojson_data["geometry"])
minx, miny, maxx, maxy = polygon.bounds 

# parametri za Forest.asc (treba pravilno nastavit)
xllcorner = 1
yllcorner = 1 
cellsize = 100
# naredi Forest.asc iz slik iz satelita in shrani v cop2cell_skripte/results datoteko Forest.asc
generate_forest_asc("coord2img/results/forest.png", "coord2img/results/water.png", "cop2cell_skripte/results/Forest.asc", xllcorner, yllcorner, cellsize)

# parametri za Weather.csv
wlat = (miny + maxy) / 2
wlong = (minx + maxx) / 2
start_date = "2024-06-14"
end_date = "2024-06-16"
scenario = "S1"
# naredi Weather.csv in shrani v cop2cell_skripte/results datoteko Weather.csv
fetch_weather_data(wlat, wlong, start_date, end_date, scenario, "cop2cell_skripte/results/Weather.csv")