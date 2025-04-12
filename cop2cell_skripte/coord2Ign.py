# dobim tri koordinate in ncols in nrows in vrnem

def coord2Ign(xllcorner: int, yllcorner: int, tockaX: int, tockaY: int,  nrow: int, ncol: int, cellsize: int):
    # Calculate column (X direction)
    col = int((tockaX - xllcorner) / cellsize)

    # Calculate row (Y direction, flipped vertically)
    row = int((tockaY - yllcorner) / cellsize)
    row = nrow - 1 - row

    # Convert to flat index
    return row * ncol + col

def main():
    print(coord2Ign(0, 0, 0, 0, 0, 0, 0))


if __name__ == "__main__":
    main()
