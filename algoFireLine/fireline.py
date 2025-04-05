import pandas as pd
import numpy as np
from utils import gen_tocke, plotCSV, further_most_point, prececisce_z_daljico,closest_point_indx,order_points_along_curve,check_barrier

def main():

    df = pd.read_csv('resultsTolmin/results/Stats/HourlyStats.csv', sep=',')
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
    map_mid = pd.read_csv(f'resultsTolmin/results/Grids/Grids1/ForestGrid{start_idx}.csv')
    map_fin = pd.read_csv(f'resultsTolmin/results/Grids/Grids1/ForestGrid{len(burned)-1}.csv')
    result = map_mid ^ map_fin
    result.to_csv('res/xor_result.csv', index=False, header=False)

    # generiri tocke po zunaji starni mape
    tocke = gen_tocke(result)
    # najdi zacetek pozara
    prva_mapa = pd.read_csv('resultsTolmin/results/Grids/Grids1/ForestGrid00.csv')
    prva_mapa = prva_mapa.to_numpy()
    zac = np.argwhere(prva_mapa == 1)
    zac = zac[:, [1, 0]]

    # najdi najdlje oddaljeno tocko od zacetka in nrdi daljico, pol pa isce prececisce (vzame preceisce
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
    pregrada = check_barrier(pregrada,map_fin)

    print(len(pregrada))
    df = pd.DataFrame(pregrada)
    df.to_csv("res/pregrada.csv",header=False, index=False)
    pomembne_tocke = np.vstack([zac,najdle,T, najblizT])
    plotCSV(result, '_pregrada', pregrada, pomembne_tocke, map_mid)


if __name__ == "__main__":
    main()
