# dobim tri koordinate in ncols in nrows in vrnem
import csv

def coord2Ign(xllcorner: int, yllcorner: int, tockaX: int, tockaY: int,  nrow: int, ncol: int, cellsize: int):
    col = int((tockaX - xllcorner) / cellsize)

    row = int((tockaY - yllcorner) / cellsize)
    row = nrow - 1 - row

    with open("Ignition.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Year", "Ncell"])
        writer.writerow([1, row * ncol + col])

def main():
    print(coord2Ign(1, 1, 1, 1, 1, 1, 1))


if __name__ == "__main__":
    main()
