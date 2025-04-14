# !!!NAHAJATI SE MORA V ISTI MAPI KOT Forest.asc in {ime}.geojson!!!
# GLEJ KOMENTARJE V MAIN, ZA UPORABO
# VERZIJA: 0.0.1
#
# requirements, ce kej nimas:
# pip install rasterio shapely geojson

import json
import requests
import rasterio
from rasterio.merge import merge
import os
import math
from uuid import uuid4
import argparse
import numpy as np
from scipy.ndimage import zoom
from shapely.geometry import shape

def read_forest_metadata(forest_file):
    # prebere metadata iz Forest.asc datoteke
    metadata = {}
    with open(forest_file, 'r') as f:
        for _ in range(6):  # prvih 6 vrstic vsebuje metapodatke
            key, value = f.readline().strip().split()
            metadata[key] = float(value) if '.' in value else int(value)
    return metadata

def replace_negatives(mosaic):
    band = mosaic[0]
    flat = band.flatten()

    # najdi prvo nenegativno vrednost
    valid_mask = flat >= 0
    first_valid = flat[valid_mask][0]

    # zamenjaj prve negativne
    first_valid_idx = np.argmax(valid_mask)
    flat[:first_valid_idx] = first_valid

    # zamenjaj vse negativne
    last_valid_indices = np.where(valid_mask, np.arange(len(flat)), 0)
    np.maximum.accumulate(last_valid_indices, out=last_valid_indices)

    filled = flat[last_valid_indices]

    band[:, :] = filled.reshape(band.shape)
    return mosaic

def download_geotiff(bbox_left, bbox_right, bbox_bottom, bbox_top, res_m, output_tiff):

    API_KEY = "KLJUC_API_VSTAVI"
    url = "https://api.gpxz.io/v1/elevation/hires-raster"

    # aproksimiraj velikost ene stopinje
    deg_per_meter = 1 / 111_320

    max_area_km2 = 10
    max_side_deg = math.sqrt(max_area_km2 * 1_000_000) * deg_per_meter

    lon = bbox_left
    temp_files = []

    while lon < bbox_right:
        next_lon = min(lon + max_side_deg, bbox_right)
        lat = bbox_bottom

        while lat < bbox_top:
            next_lat = min(lat + max_side_deg, bbox_top)

            params = {
                "bbox_left": lon,
                "bbox_right": next_lon,
                "bbox_bottom": lat,
                "bbox_top": next_lat,
                "res_m": res_m / 10,
                "api-key": API_KEY
            }

            temp_file = f"tile_{uuid4().hex}.tiff"
            print(f"Prenašanje: {temp_file}")
            response = requests.get(url, params=params, stream=True)

            if response.status_code == 200:
                with open(temp_file, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                temp_files.append(temp_file)
            else:
                raise Exception(f"Napaka API-ja za območje {lon}, {lat}, {next_lon}, {next_lat}: {response.status_code}, {response.text}")

            lat = next_lat
        lon = next_lon

    # Združi vse ploščice v en GeoTIFF
    print("Združevanje .tiff datotek...")
    src_files_to_mosaic = [rasterio.open(fp) for fp in temp_files]
    mosaic, out_trans = merge(src_files_to_mosaic)

    out_meta = src_files_to_mosaic[0].meta.copy()
    out_meta.update({
        "height": mosaic.shape[1],
        "width": mosaic.shape[2],
        "transform": out_trans
    })

    mosaic = replace_negatives(mosaic)

    with rasterio.open(output_tiff, "w", **out_meta) as dest:
        dest.write(mosaic)

    print(f"GeoTIFF končan: {output_tiff}")

    # Počisti začasne datoteke
    for fp in temp_files:
        os.remove(fp)

def extract_elevation_from_tiff(tiff_file, nrows, ncols):
    # prebere podatke GeoTIFF in da v array
    with rasterio.open(tiff_file) as dataset:
        elevation_data = dataset.read(1)


    original_shape = elevation_data.shape

    # izracunaj zoom faktor
    zoom_factor = (nrows / original_shape[0], ncols / original_shape[1])
    # bilinear interpolation - karkol to pomen
    resampled_elevation_data = zoom(elevation_data, zoom_factor, order=1)
    resampled_elevation_data_INT = np.round(resampled_elevation_data).astype(int)
    resampled_elevation_data_INT = resampled_elevation_data_INT * 3

    os.remove("cop2cell_skripte/results/Elevation.tif")
    return resampled_elevation_data_INT

def write_elevation_asc(metadata, elevation_data, output_file):
    # prepise podatke o visinah v Elevation.asc datoteko
    nrows, ncols = metadata["nrows"], metadata["ncols"]
    xllcorner, yllcorner = metadata["xllcorner"], metadata["yllcorner"]
    cellsize, nodata_value = metadata["cellsize"], -9999

    with open(output_file, 'w') as f:
        f.write(f"ncols {ncols}\n")
        f.write(f"nrows {nrows}\n")
        f.write(f"xllcorner {xllcorner}\n")
        f.write(f"yllcorner {yllcorner}\n")
        f.write(f"cellsize {cellsize}\n")
        f.write(f"NODATA_value {nodata_value}\n")

        for row in elevation_data:
            f.write(" ".join(map(str, row)) + "\n")

def main():

    # ZAZENI TAKO:
    # python api2elevation.py {ime.geojson}
    parser = argparse.ArgumentParser(description="Generiraj Elevation.asc datoteko s pomočjo API in .geojson datoteke")
    parser.add_argument("geojson", help="Pot do geojson datoteke.")
    args = parser.parse_args()

    forest_file = "Forest.asc"
    output_tiff = "Elevation.tif"
    output_asc = "elevation.asc"

    # prebere metapodatke iz Forest.asc
    metadata = read_forest_metadata(forest_file)

    # PREBERI PODATKE IZ GEOJSON
    with open(args.geojson, "r") as f:
        geojson_data = json.load(f)

    polygon = shape(geojson_data["geometry"])
    minx, miny, maxx, maxy = polygon.bounds

    # definiram zemljepisne meje za API klic
    # TOLE POGLEJ ČE LAHKO ZE V FOREST DOBIS V PRAVIH PODATKIH!!!
    bbox_left = minx # najzahodnejša dolžina
    bbox_bottom = miny # najjužnejša širina
    bbox_right = maxx # najvzhodnejša dolžina
    bbox_top = maxy # najsevernejša širina

    res_m = metadata["cellsize"]  # med 1 in 30 - mora biti že v Forest.asc pravi

    # prejmi GeoTIFF iz API
    download_geotiff(bbox_left, bbox_right, bbox_bottom, bbox_top, res_m, output_tiff)

    # prejmi podatke o visinah iz GeoTIFF
    elevation_data = extract_elevation_from_tiff(output_tiff, metadata["nrows"], metadata["ncols"])

    # prepisi v Elevation.asc
    write_elevation_asc(metadata, elevation_data, output_asc)
    print(f"{output_asc} je generiran. Verzija 0.0.1")

if __name__ == "__main__":
    main()
