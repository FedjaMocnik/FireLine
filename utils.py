import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import KDTree
from typing import Tuple

#nardi graf map.pdf
def plotCSV(result, edge_points: np.ndarray, pomtoc: np.ndarray, midmap, save_path: str, ortho):
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

    labels = np.array(["Start", "Najdle", "Prececisce T", "NajblizjaT"])
    for tocka in pomtoc:
        plt.scatter(tocka[0], tocka[1], color='blue', s=15)

    plt.plot([pomtoc[0,0], pomtoc[1,0]], [pomtoc[0,1], pomtoc[1,1]], color="navy")
    plt.plot([ortho[0,0], ortho[1,0]], [ortho[0,1], ortho[1,1]], color="black")

    for i, (x, y) in enumerate(pomtoc):
        if i == 2:
            plt.text(x, y, labels[i],
                     ha='center', va='top',  # Alignment
                     fontsize=9, color='black')
        else:
            plt.text(x, y, labels[i],
                     ha='center', va='bottom',  # Alignment
                     fontsize=9, color='black')

    # Set the aspect ratio so that x and y scales are equal
    plt.gca().set_aspect('equal', adjustable='box')

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

    for i in range(len(ordered)-1, 0, -1):  # Start from the end
        dist = np.linalg.norm(ordered[i] - ordered[i-1])
        if dist > 3.0:
            ordered = np.delete(ordered, i, axis=0)
    return np.array(ordered)

def check_barrier(arr: np.ndarray, map:np.ndarray)->np.ndarray:

    #NE DELA KOT BI SI ZELEL
    newPoints = []
    padded = np.pad(map, pad_width=1, mode='constant', constant_values=0)
    for point in arr:
        i,j = point
        neighborhood = padded[i:i+3, j:j+3]
        zero_count = np.sum(neighborhood == 0)

        if zero_count <= 3:
            newPoints.append(point)

    return np.array(newPoints)

def plot_differences(diff_of_burned_area, diff_diff, start_idx, n, save_path):
    # Create time axis
    time = np.arange(len(diff_of_burned_area))

    # Plot 1: diff_of_burned_area
    plt.figure(figsize=(12, 6))
    plt.plot(time, diff_of_burned_area, 'b-', label='Daily burned area difference')

    # Highlight the selected window
    plt.axvspan(start_idx, start_idx+n, color='yellow', alpha=0.3,
               label=f'Selected window (idx {start_idx}-{start_idx+n})')

    # Mark the start_idx point
    plt.scatter(start_idx, diff_of_burned_area[start_idx],
               color='red', s=100, zorder=5, label='Start index')

    plt.title('Daily Burned Area Differences')
    plt.xlabel('Time (hours/days)')
    plt.ylabel('Area difference')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(f"{save_path}diff_of_burned_area.pdf")
    plt.close()

    # Plot 2: diff_diff
    plt.figure(figsize=(12, 6))
    plt.plot(time, diff_diff, 'g-', label='Difference of differences')

    # Highlight the selected window
    plt.axvspan(start_idx, start_idx+n, color='yellow', alpha=0.3,
               label=f'Selected window (idx {start_idx}-{start_idx+n})')

    # Mark the start_idx point
    plt.scatter(start_idx, diff_diff[start_idx],
               color='red', s=100, zorder=5, label='Start index')

    plt.title('Second-Order Differences (Diff of Diffs)')
    plt.xlabel('Time (hours/days)')
    plt.ylabel('Difference value')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(f"{save_path}diff_diff.pdf")
    plt.close()

def pravokotnica_na_tocko(zac:np.ndarray, najdle:np.ndarray, T:np.ndarray, length = 50)-> np.ndarray:

    dx = najdle[0] - zac[0]
    dy = najdle[1] - zac[1]
    perp_dir = np.array([-dy, dx], dtype=np.float64)
    perp_dir /= np.linalg.norm(perp_dir)
    perp_dir *= length
    point1 = T + (int(perp_dir[0]),int(perp_dir[1])+1)
    point2 = T - (int(perp_dir[0]),int(perp_dir[1])+1)

    return np.vstack([point1,point2])

def bresenham_line(x0: int, y0: int, x1: int, y1: int) -> np.ndarray:
    points = []
    dx = abs(x1 - x0)
    dy = -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx + dy

    while True:
        points.append((x0, y0))
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy

    return np.array(points, dtype=int)

def podalsaj_pregrado(pregrada:np.ndarray, n:float=0.1)->np.ndarray:

    direction = pregrada[1] - pregrada[0]
    new_start = pregrada[0] - n * direction
    new_end = pregrada[1] + n * direction
    res = np.vstack([new_start, new_end]).astype(int)

    return res
