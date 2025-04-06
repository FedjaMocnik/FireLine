import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import KDTree
from typing import Tuple

#nardi graf map.pdf
def plotCSV(result, edge_points: np.ndarray, pomtoc:np.ndarray, midmap, save_path:str):
    rows, cols = result.shape
    points = []
    for y in range(rows):
        for x in range(cols):
            if result.iloc[y, x] == 1:
                points.append((x, y))  # (x, y) coordinates
    x_coords, y_coords = zip(*points) if points else ([], [])

    rows2, cols2 = midmap.shape
    points2 = []
    for y in range(rows2):
        for x in range(cols2):
            if midmap.iloc[y, x] == 1:
                points2.append((x, y))
    x_coords2, y_coords2 = zip(*points2) if points2 else ([], [])

    # Plot the points
    plt.figure(figsize=(8, 6))
    plt.scatter(x_coords, y_coords, color='red', marker='s', s=10)  # 's' for square markers
    plt.scatter(x_coords2, y_coords2, color='firebrick', marker='s', s=10)

    plt.title("FireLine Map")
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.xlim(-0.5, cols - 0.5)
    plt.ylim(-0.5, rows - 0.5)
    plt.gca().invert_yaxis()
    plt.scatter(edge_points[:, 0], edge_points[:, 1], color='dimgray', s=5)


    lables = np.array(["Start", "Najdle", "Prececisce T", "NajblizjaT"])
    for tocka in pomtoc:
        plt.scatter(tocka[0], tocka[1], color='blue', s=15)

    plt.plot([pomtoc[0,0],pomtoc[1,0]],[pomtoc[0,1],pomtoc[1,1]], "navy")

    for i, (x, y) in enumerate(pomtoc):
        if i == 2:
            plt.text(x, y, lables[i],
            ha='center', va='top',  # Alignment
            fontsize=9, color='black')
        else:
            plt.text(x, y, lables[i],
            ha='center', va='bottom',  # Alignment
            fontsize=9, color='black')


    plt.savefig(f"{save_path}map.pdf")

#generira tocke na zunaji strani pozara
def gen_tocke(file)->np.ndarray:
    file = file.to_numpy()
    edge_mask = np.zeros_like(file, dtype=bool)
    padded = np.pad(file, pad_width=1, mode='constant', constant_values=0)
    rows, cols = file.shape

    for i in range(rows):
        for j in range(cols):
            if file[i, j]== 1:
                neighborhood = padded[i:i+3, j:j+3]
                if np.any(neighborhood == 0):
                    edge_mask[i, j] = True
    y_coords, x_coords = np.where(edge_mask)
    edge_points = np.column_stack((x_coords, y_coords))

    return edge_points


def further_most_point(zac:np.ndarray, tocke:np.ndarray)-> np.ndarray:

    squared_dists = np.sum((tocke - zac)**2, axis=1)
    max_idx = np.argmax(squared_dists)
    return tocke[max_idx]

def prececisce_z_daljico(daljica:np.ndarray, tocke:np.ndarray, epsilon: float=0.5) -> np.ndarray:
    A, B = daljica[0], daljica[1]
    AB = B - A

    if np.allclose(A, B):
        distances = np.linalg.norm(tocke - A, axis=1)
        return tocke[distances <= epsilon]

    AP = tocke - A
    t = np.dot(AP, AB) / np.dot(AB, AB)
    t_clamped = np.clip(t, 0.0, 1.0)
    projections = A + t_clamped[:, None] * AB
    distances = np.linalg.norm(tocke - projections, axis=1)

    return tocke[distances <= epsilon]


def closest_point_indx(T:np.ndarray, tocke:np.ndarray)-> Tuple[int,np.ndarray]:
    min_raz=10000000
    indx=0
    nova_t=np.ndarray
    for i in range(len(tocke)):
        raz = np.linalg.norm(T-tocke[i])
        if raz < min_raz:
            min_raz = raz
            indx = i
            nova_t=tocke[i]
    nova_t=np.array(nova_t)
    return indx,nova_t


def order_points_along_curve(points: np.ndarray) -> np.ndarray:
    start_idx = np.argmin(points[:, 0])
    ordered = [points[start_idx]]
    visited = set([start_idx])
    tree = KDTree(points)

    while len(visited) < len(points):

        distances, indices = tree.query(ordered[-1], k=len(points))

        for idx in indices:
            if idx not in visited:
                ordered.append(points[idx])
                visited.add(idx)
                break

    ordered = np.array(ordered)

    for i in range(len(ordered)):
        if not i == 0:
            dist = np.linalg.norm(ordered[i]-ordered[i-1])
            if dist > 3.0:
                ordered = np.delete(ordered,i, axis=0)
    return np.array(ordered)

def check_barrier(arr: np.ndarray, map:np.ndarray)->np.ndarray:

    #NE DELA KOT BI SI ZELEL
    newPoints = []
    padded = np.pad(map, pad_width=1, mode='constant', constant_values=0)
    for point in arr:
        i,j = point
        neighborhood = padded[i:i+3, j:j+3]
        zero_count = np.sum(neighborhood == 0)

        if zero_count <= 4:
            newPoints.append(point)

    return np.array(newPoints)
