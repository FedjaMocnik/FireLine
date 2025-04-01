# !!!NAHAJATI SE MORA V ISTI MAPI KOT elevation.asc!!!
# VERZIJA: 0.0.1

import numpy as np

def load_asc(filename):
    with open(filename, 'r') as f:
        header = [next(f) for _ in range(6)]
        data = np.loadtxt(f)
    return header, data

def save_asc(filename, header, data):
    with open(filename, 'w') as f:
        f.writelines(header)
        np.savetxt(f, data, fmt='%.6f')

def compute_slope_aspect(elevation, cellsize):
    rows, cols = elevation.shape
    slope = np.full((rows, cols), 0)
    aspect = np.full((rows, cols), 0)

    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            dzdx = ((elevation[i-1, j+1] + 2*elevation[i, j+1] + elevation[i+1, j+1]) -
                    (elevation[i-1, j-1] + 2*elevation[i, j-1] + elevation[i+1, j-1])) / (8 * cellsize)

            dzdy = ((elevation[i+1, j-1] + 2*elevation[i+1, j] + elevation[i+1, j+1]) -
                    (elevation[i-1, j-1] + 2*elevation[i-1, j] + elevation[i-1, j+1])) / (8 * cellsize)

            slope[i, j] = np.arctan(np.sqrt(dzdx**2 + dzdy**2)) * (180 / np.pi)
            aspect[i, j] = (np.arctan2(dzdy, -dzdx) * (180 / np.pi)) % 360

    slope = np.round(slope).astype(int)
    aspect = np.round(slope).astype(int)

    return slope, aspect

def main():
    header, elevation = load_asc('elevation.asc')
    cellsize = float(header[4].split()[1])

    slope, aspect = compute_slope_aspect(elevation, cellsize)

    save_asc('slope.asc', header, slope)
    save_asc('saz.asc', header, aspect)
    print("slope.asc in saz.asc sta generirana. Verzija 0.0.1")

if __name__ == "__main__":
    main()
