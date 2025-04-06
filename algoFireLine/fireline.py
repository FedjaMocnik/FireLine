# VERZIJA: 0.1.3 - zamik za ena na png-jih, path nastavljen iz argsov
# REQUIREMENTS: numpy, pandas, matplotlib, scipy, PIL
# RUN: python3 fireline.py {path do HourlyStats.csv} {path do .../Grids/Grids1/} {path do mape kjer shran rezultate} {path do pngs}

import pandas as pd
import numpy as np
from utils import gen_tocke, plotCSV, further_most_point
from utils import prececisce_z_daljico,closest_point_indx,order_points_along_curve
from PIL import Image, ImageDraw
import sys
#from utils import check_barrier #odkometirej ko bo delal

# PATH_TO_HOURLY_STATS = "resultsTolmin/results/Stats/HourlyStats.csv"
# PATH_TO_GRIDS = "resultsTolmin/results/Grids/Grids1/"
# SAVE_PATH = "res/"
# PATH_TO_PNGS = "testni_primer/"

PATH_TO_HOURLY_STATS = sys.argv[1]
PATH_TO_GRIDS = sys.argv[2]
SAVE_PATH = sys.argv[3]
PATH_TO_PNGS = sys.argv[4]


def main():

    df = pd.read_csv(PATH_TO_HOURLY_STATS, sep=',')
    burned = df['Burned'].tolist()

    # zracuni razlike med velikostjo pozara
    i = 1
    diff_of_burned_area = []
    diff_of_burned_area.append(int(burned[0]))
    while i < len(burned):
        diff_of_burned_area.append(int(burned[i])-int(burned[i-1]))
        i += 1

    # zracuni razlike med razlikami
    diff_diff = []
    i=1
    diff_diff.append(diff_of_burned_area[0])
    while i < len(diff_of_burned_area):
        diff_diff.append(abs(diff_of_burned_area[i] - diff_of_burned_area[i-1]))
        i += 1

    # najdi minimum povprecja n zaporednih razlik
    n = 5
    current_sum = sum(diff_diff[:n])
    min_sum = current_sum
    start_idx=0
    for i in range(n, len(diff_diff)):
        current_sum = current_sum - diff_diff[i - n] + diff_diff[i]
        if current_sum < min_sum:
            min_sum = current_sum
            start_idx = i - n + 1

    # XOR med zadnjo in izracunanim_min mapami
    map_mid = pd.read_csv(f'{PATH_TO_GRIDS}ForestGrid{start_idx}.csv')
    map_fin = pd.read_csv(f'{PATH_TO_GRIDS}ForestGrid{len(burned)-1}.csv')
    #map_fin.info()
    result = map_mid ^ map_fin
    #result.to_csv(f'{SAVE_PATH}xor_result.csv', index=False, header=False)

    # generiri tocke po zunaji starni mape
    tocke = gen_tocke(result)
    # najdi zacetek pozara
    prva_mapa = pd.read_csv(f'{PATH_TO_GRIDS}ForestGrid00.csv')
    prva_mapa = prva_mapa.to_numpy()
    zac = np.argwhere(prva_mapa == 1)
    zac = zac[:, [1, 0]]

    # najdi najdlje oddaljeno tocko od zacetka in nrdi daljico,
    # pol pa isce prececisce (vzame preceisce
    # ki je najblizje startu)
    najdle = further_most_point(zac, tocke)
    daljica = np.vstack([zac, najdle])
    prececisca = prececisce_z_daljico(daljica, tocke)
    razdalje = np.linalg.norm(prececisca - najdle, axis=1)
    T = prececisca[np.argmax(razdalje)]

    # nared se tocke za minmum_mapo in najd najblizjo tocko od prececisca premice
    midTocke = []
    midTocke = gen_tocke(map_mid)
    urejeneT =order_points_along_curve(midTocke)
    indx, najblizT = closest_point_indx(T,urejeneT)

    # vzem 20 +- tock od najblizjeT = pregrada
    indeksi = np.arange(indx - 20, indx + 20 + 1) % len(urejeneT)
    pregrada = urejeneT[indeksi]

    # pregrado nared sam tm kjer je na obeh straneh ogenj
    map_fin = map_fin.to_numpy()
    # check_barrier je zaenkrat useless
    #pregrada = check_barrier(pregrada,map_fin)

    df = pd.DataFrame(pregrada)
    #df.to_csv(f"{SAVE_PATH}pregrada.csv",header=False, index=False)
    pomembne_tocke = np.vstack([zac,najdle,T, najblizT])
    plotCSV(result, pregrada, pomembne_tocke, map_mid, SAVE_PATH)

    ndiv = Image.open(f"{PATH_TO_PNGS}tolminNDIV.png")
    voda = Image.open(f"{PATH_TO_PNGS}tolminVoda.png")

    draw_ndiv = ImageDraw.Draw(ndiv)
    draw_voda = ImageDraw.Draw(voda)

    #pomoje se nekje zamaknejo kordinate vse za +1 - tukaj popravek
    #pregrada+=1
    #csv ma 99 namest 100 dolzino maybe je to problem :/
    pregrada[:,1::2]+=1
    prej = pregrada[0]

    for tocka in pregrada[1:]:
        draw_ndiv.line((tocka[0],tocka[1],prej[0], prej[1]), fill="white", width=1)
        draw_voda.line((tocka[0],tocka[1],prej[0], prej[1]), fill="blue", width=1)
        prej = tocka

    ndiv.save(f"{SAVE_PATH}pregradaNDIV.png")
    voda.save(f"{SAVE_PATH}pregradaVoda.png")

if __name__ == "__main__":
    main()
