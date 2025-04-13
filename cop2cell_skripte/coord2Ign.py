# dobim tri koordinate in ncols in nrows in vrnem
import csv

def coord2Ign(maxX: int, minY: int, minX: int, maxY: int, tockaX: int, tockaY: int,  nrow: int, ncol: int):
    lat_ratio = (maxX - tockaX) / (maxX - minX)
    lon_ratio = (maxY - tockaY) / (maxY - minY)
    row = int(lat_ratio * nrow)
    col = int(lon_ratio * ncol)

    row = min(max(row, 0), nrow - 1)
    col = min(max(col, 0), ncol - 1)
    return row * ncol + col


    with open("cop2cell_skripte/results/Ignitions.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Year", "Ncell"])
        writer.writerow([1, row * ncol + col])

def main():
    print(coord2Ign(460000, 140000, 450000, 150000, 455000, 145000, 100, 100))


if __name__ == "__main__":
    main()
