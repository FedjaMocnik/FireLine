import warnings
warnings.filterwarnings("ignore", message="Signature .* does not match any known type") # To filter warning from numpy

import time
from coord2img.utils.geojson_tools import *
from coord2img.obdelava.data_generation import get_data
from cop2cell_skripte.png2Forest import *
from cop2cell_skripte.api2Weather import *
from cop2cell_skripte.api2elevation import *
from cop2cell_skripte.ele2slope import *
from cop2cell_skripte.runC2F import *
from cop2cell_skripte.coord2Ign import *
import math


def generate(coordinates,selectedDate):
    #number of km form selected point to the edge of the area
    coordinates = coordinates[0]
    latOfPoint = coordinates[0]
    lonOfPoint = coordinates[1]

    areaSize = 3 #km
    deltaLon = areaSize / (111.32 * math.cos(math.radians(latOfPoint)))
    deltaLat = areaSize / 111.32


    latitude1 = latOfPoint + deltaLat
    longitude1 = lonOfPoint - deltaLon
    latitude2 = latOfPoint - deltaLat
    longitude2 = lonOfPoint + deltaLon

    #upper left, bottom rigth and selected point coordinates in utm 33 N
    latitude1,longitude1 = latlon_to_utm33n(latitude1,longitude1)
    latitude2,longitude2 = latlon_to_utm33n(latitude2,longitude2)
    latOfPoint,lonOfPoint = latlon_to_utm33n(latOfPoint,lonOfPoint)


    create_geojson_rectangle((latitude1,longitude1),(latitude2, longitude2))

    # Gets data form setelites and saves it to coord2img/results
    get_data()

    # PREBERI PODATKE IZ GEOJSON
    with open("coord2img/results/new_area.geojson", "r") as f:
        geojson_data = json.load(f)

    polygon = shape(geojson_data["geometry"])
    minx, miny, maxx, maxy = polygon.bounds

    # parametri za Forest.asc (treba pravilno nastavit)
    xllcorner = minx
    yllcorner = miny
    cellsize = 100
    # naredi Forest.asc iz slik iz satelita in shrani v cop2cell_skripte/results datoteko Forest.asc
    ncols, nrows = generate_forest_asc("coord2img/results/forest.png", "coord2img/results/water.png", "cop2cell_skripte/results/Forest.asc", xllcorner, yllcorner, cellsize)
    print("Forest.asc je generiran. Verzija 0.0.2")

    # parametri za Weather.csv
    wlat = (miny + maxy) / 2
    wlong = (minx + maxx) / 2
    start_date = selectedDate
    scenario = "S1"
    # naredi Weather.csv in shrani v cop2cell_skripte/results datoteko Weather.csv
    #fetch_weather_data(wlat, wlong, start_date, scenario, "cop2cell_skripte/results/Weather.csv")

    # naredi Ignitions.csv datoteko
    coord2Ign(int (xllcorner), int(yllcorner), lonOfPoint, latOfPoint, nrows, ncols, cellsize)

    # klic api2elevation.py - cakam se da mi un model poveca iz 10km^2 na vec
    # forest_file = "cop2cell_skripte/results/Forest.asc"
    # output_tiff = "cop2cell_skripte/results/Elevation.tif"
    # output_asc = "cop2cell_skripte/results/elevation.asc"
    # res_m = 10 # na koliko metrov natancno se dobi elevation.asc (med 1 in 30)
    # metadata = read_forest_metadata(forest_file)
    # download_geotiff(minx, maxx, miny, maxy, res_m, output_tiff)
    # elevation_data = extract_elevation_from_tiff(output_tiff, metadata["nrows"], metadata["ncols"])
    # write_elevation_asc(metadata, elevation_data, output_asc)
    # print(f"{output_asc} je generiran. Verzija 0.1.0")

    # # klic ele2slope.py
    # header, elevation = load_asc(output_asc)
    # # cellsize je ze definiran
    # slope, aspect = compute_slope_aspect(elevation, cellsize)
    # save_asc('cop2cell_skripte/results/slope.asc', header, slope)
    # save_asc('cop2cell_skripte/results/saz.asc', header, aspect)
    # print("slope.asc in saz.asc sta generirana. Verzija 0.0.1")
    # print("Weather.csv je generiran. Verzija 0.1.0")

    # za"zeni Cell2Fire
    #run_cell2fire("../../FireLine/cop2cell_skripte/results/", "../../FireLine/rezultati_cell2fire/")

    # copies files to site directory to be displayed on a page
    copy_file("forest.png", "./coord2img/results", "./spletna_stran/react/fireLine/public")
    return 0

if __name__=="__main__":
    latitude1 = 456231.740204
    longitude1 = 5102686.348333
    latitude2 = 461467.877750
    longitude2 = 5099408.768305
    coordinates_test = ((latitude1,longitude1),(latitude2,longitude2))
    generate(coordinates_test, "2024-01-01")