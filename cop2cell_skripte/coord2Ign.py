# dobim tri koordinate in ncols in nrows in vrnem
import csv

def coord2Ign(maxX: int, minY: int, minX: int, maxY: int, tockaX: int, tockaY: int,  nrow: int, ncol: int):
    x_ratio = (maxX - tockaX) / (maxX - minX)
    y_ratio = (maxY - tockaY) / (maxY - minY) 
    row = x_ratio * nrow
    col = y_ratio * ncol

    row = min(max(row, 0), nrow - 1)
    col = min(max(col, 0), ncol - 1)
    # return row * ncol + col

    print(row, col)

    with open("cop2cell_skripte/results/Ignitions.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Year", "Ncell"])
        writer.writerow([1, int(row * ncol + (ncol - col))])

def main():
    print(coord2Ign(460000, 140000, 450000, 150000, 455000, 145000, 100, 100))


if __name__ == "__main__":
    main()
