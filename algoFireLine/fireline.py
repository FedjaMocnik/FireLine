# VERZIJA: 0.2.0 - pregrada je pravokotnica na dalico
# REQUIREMENTS: numpy, pandas, matplotlib, scipy, PIL
# RUN: python3 fireline.py {path do HourlyStats.csv} {path do .../Grids/Grids1/} {path do mape kjer shran rezultate} {path do pngs}

import pandas as pd
import numpy as np
from utils import gen_tocke, plotCSV, further_most_point,bresenham_line,podalsaj_pregrado
from utils import prececisce_z_daljico,closest_point_indx,order_points_along_curve,plot_differences,pravokotnica_na_tocko
from PIL import Image, ImageDraw
import sys
#from utils import check_barrier #odkometirej ko bo delal

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
    diff_of_burned_area.pop()

    i=1
    diff_diff.append(diff_of_burned_area[0])
    while i < len(diff_of_burned_area):
        diff_diff.append(diff_of_burned_area[i] - diff_of_burned_area[i-1])
        i += 1

    # najdi minimum povprecja n zaporednih razlik
    n = 8
    current_sum = 100000000
    min_sum = current_sum
    start_idx=0
    ignore_first = 0.2*len(diff_diff)
    ignore_first=int(ignore_first)

    for i in range(n+ignore_first, int(len(diff_diff)*0.8)):
        current_sum = current_sum - diff_diff[i - n] + diff_diff[i]
        if current_sum < min_sum:
            min_sum = current_sum
            start_idx = i - n + 1

    if start_idx==0:
        start_idx=len(diff_diff)/2
        start_idx=int(start_idx)
    plot_differences(diff_of_burned_area, diff_diff, start_idx, n, SAVE_PATH)

    # XOR med zadnjo in izracunanim_min mapami
    if start_idx < 10:
        start_idx = "0"+str(start_idx)
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
    #indeksi = np.arange(indx - 20, indx + 20 + 1) % len(urejeneT)

    #nardi pravokotnico na tocko T
    ortoline = pravokotnica_na_tocko(zac[0],najdle,najblizT)
    tocke2 = gen_tocke(map_fin)
    prececisca = prececisce_z_daljico(ortoline,tocke2)
    if len(prececisca) > 2:
        prvaT = prececisca[0]
        diffs = prececisca[1:] - prvaT
        distances = np.linalg.norm(diffs, axis=1)
        furthest_index = np.argmax(distances)
        furthest_point = prececisca[1:][furthest_index]
        prececisca = np.array([prvaT,furthest_point])

    #pregrada_og = urejeneT[indeksi]
    pregrada = podalsaj_pregrado(prececisca)
    pregrada = bresenham_line(pregrada[0,0],pregrada[0,1],pregrada[1,0],pregrada[1,1])

    # pregrado nared sam tm kjer je na obeh straneh ogenj
    #map_fin = map_fin.to_numpy()
    # check_barrier je zaenkrat useless
    #pregrada = check_barrier(pregrada,map_fin)

    pomembne_tocke = np.vstack([zac,najdle,T, najblizT])
    plotCSV(result, pregrada, pomembne_tocke, map_mid, SAVE_PATH, prececisca)

    voda = Image.open(f"{PATH_TO_PNGS}tolminVoda.png")
    draw_voda = ImageDraw.Draw(voda)
    pregrada[:,1::2]+=1
    prej = pregrada[0]

    for tocka in pregrada[1:]:
        draw_voda.line((tocka[0],tocka[1],prej[0], prej[1]), fill="blue", width=2)
        prej = tocka
    voda.save(f"{SAVE_PATH}pregradaVoda.png")

if __name__ == "__main__":
    main()
