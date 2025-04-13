# GLEJ KOMENTARJE V MAIN, ZA UPORABO
# VERZIJA: 0.0.2

import numpy as np
import argparse
from PIL import Image

def generate_forest_asc(vegetation_path: str, water_path: str, output_path: str, xllcorner: int, yllcorner: int, cellsize: int):
    # nalozi sliki v greyscale
    veg_img = Image.open(vegetation_path).convert('L')
    water_img = Image.open(water_path).convert('L')

    # spremeni sliki v array
    veg_array = np.array(veg_img)
    water_array = np.array(water_img)

    # prever da imata enaki dimenziji
    if veg_array.shape != water_array.shape:
        raise ValueError("Sliki nista enakih dimenzij!")

    nrows, ncols = veg_array.shape
    nodata_value = -9999

    # inicializacija izhodnega arraya
    forest_grid = np.full((nrows, ncols), nodata_value)

    # procesiranje, glede na vrednosti posameznih pikslov
    for i in range(nrows):
        for j in range(ncols):
            veg_val = veg_array[i, j]
            water_val = water_array[i, j]

            # nastavi vrednost
            if water_val < 245:
                forest_grid[i, j] = 101  # nastavi stavbe, ceste, reke
            elif veg_val < 62:
                forest_grid[i, j] = 2  # nastavi gozd
            elif veg_val < 100:
                forest_grid[i, j] = 32  # nastavi travo
            else:
                forest_grid[i, j] = 101 # se ostale stavbe, ceste

    # pisanje v izhodno datoteko
    with open(output_path, 'w') as f:
        f.write(f"ncols {ncols}\n")
        f.write(f"nrows {nrows}\n")
        f.write(f"xllcorner {xllcorner}\n")
        f.write(f"yllcorner {yllcorner}\n")
        f.write(f"cellsize {cellsize}\n")
        f.write(f"NODATA_value {nodata_value}\n")

        for row in forest_grid:
            f.write(" ".join(map(str, row)) + "\n")

    return ncols, nrows

"""
    with open(output_ignitions, 'w') as f2:
        f2.write("Year,Ncell\n")
        f2.write(f"1,{int((ncols * nrows) / 2)}\n")
"""

def main():

    # PARSANJE ARGUMENTOV V FUNKCIJO
    # ZAZENI TAKO: python png2Forest.py {IME_SLIKE_NVID} {IME_SLIKE_VODA} {XLL_KOORDINATE} {YLL_KOORDINATE} {CELLSIZE} --output Forest.asc --output_ignitions Ignitions.csv
    # NPR: python png2Forest.py vhodTestNDIV.png vhodTestNDIV.png 457900 5716800 100 --output Forest.asc
    parser = argparse.ArgumentParser(description="Generiraj .asc datoteko iz NDVI in vode.")
    parser.add_argument("vegetation", help="Pot do NDVI slike")
    parser.add_argument("water", help="Pot do vode slike")
    parser.add_argument("xllcorner", help="XLLCORNER")
    parser.add_argument("yllcorner", help="YLLCORNER")
    parser.add_argument("cellsize", help="CELLSIZE")
    parser.add_argument("--output", default="Forest.asc", help="Izhodna .asc datoteka (privzeto: Forest.asc)")
    parser.add_argument("--output_ignitions", help="IGNITION")

    args = parser.parse_args()

    # XLLCORNER, YLLCORNER 457900 5716800, CELLSIZE NUJNO 100 (glede na to kako trenutno delamo)
    generate_forest_asc(args.vegetation, args.water, args.output, args.xllcorner, args.yllcorner, args.cellsize)
    print(f"{args.output} je generiran. Verzija 0.0.2")

if __name__ == "__main__":
    main()
