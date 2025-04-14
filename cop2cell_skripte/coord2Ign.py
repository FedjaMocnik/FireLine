
import csv

def coord2Ign(maxX: int, minY: int, minX: int, maxY: int, tockaX: int, tockaY: int, nrow: int, ncol: int):
    x_ratio = (tockaX - minX) / (maxX - minX)
    y_ratio = (maxY - tockaY) / (maxY - minY)  # because Y increases upwards, but rows go downward

    col = min(max(int((1 - y_ratio) * ncol), 0), ncol - 1)
    row = min(max(int((1 - x_ratio) * nrow), 0), nrow - 1)


    with open("cop2cell_skripte/results/Ignitions.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Year", "Ncell"])
        writer.writerow([1, row * ncol + col])

def main():
    print(coord2Ign(460000, 140000, 450000, 150000, 455000, 145000, 100, 100))


if __name__ == "__main__":
    main()