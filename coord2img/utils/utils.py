from datetime import datetime
import matplotlib.colors as mcolors
import geopandas as gpd
import numpy as np
from shapely.geometry import Polygon
from sentinelhub import (
    DataCollection,
    MimeType,
    SentinelHubRequest,
    SHConfig,
    UtmZoneSplitter
)
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import json
try:
    from geojson_tools import *
except ModuleNotFoundError:
    from coord2img.utils.geojson_tools import *

# Function to set up the Sentinel Hub profile
def SHub_profile(client_id="", client_secret="", profile_name=""):
    if profile_name:
        try:
            config = SHConfig(profile_name)
            print(f"Loaded SH profile: {profile_name}.")
        except:
            if not client_id or not client_secret:
                raise ValueError(f"Profile {profile_name} not found and client_id and client_secret not provided.")
            print(f"Profile {profile_name} not found, creating a new one.")
            config = SHConfig()
            config.sh_client_id = client_id
            config.sh_client_secret = client_secret
            config.sh_token_url = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"
            config.sh_base_url = "https://sh.dataspace.copernicus.eu"
            config.save(profile_name)
            print(f"Profile {profile_name} created and saved.")    
    else:
        print(f"Creating a new SH profile.")
        config = SHConfig()
        config.sh_client_id = client_id
        config.sh_client_secret = client_secret
        config.sh_token_url = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"
        config.sh_base_url = "https://sh.dataspace.copernicus.eu"
    return config

# Function to set the time interval to months from June to September
def interval_of_interest(year):
       return (datetime(year, 6, 1), datetime(year, 9, 1))

# Function to generate the request for the Sentinel Hub API
def create_SHrequest(year, bbox, resolution, eval_script, config, data_folder=""):
    time_interval = interval_of_interest(year)
    return SentinelHubRequest(
        evalscript=eval_script,
        input_data=[
            SentinelHubRequest.input_data(
                data_collection=DataCollection.SENTINEL2_L2A.define_from(
                    "s2", service_url=config.sh_base_url
                ),
                time_interval=time_interval,
            )
        ],
        responses=[SentinelHubRequest.output_response("default", MimeType.TIFF)],
        bbox=bbox,
        resolution=resolution,
        config=config,
        data_folder=data_folder,
    )

# Function to load slovenia's bounding boxes and if desired save an image of the resulting grid
def load_slovenia_bbox(geojson_name,box_size=20000, save_img=False):
    # Load the country's shape (Slovenia)
    print("Loading shape...")
    country = gpd.read_file(geojson_name)

    # Get the country's shape in polygon format
    country_shape = country.geometry.values[0]

    # Print size of the country bounding box
    country_width = country_shape.bounds[2] - country_shape.bounds[0]
    country_height = country_shape.bounds[3] - country_shape.bounds[1]
    print(f"Dimension of the area is {country_width:.0f} x {country_height:.0f} m2")

    """ Coordinates for original rect
        # Return the coordinates of the edges
        min_x, min_y, max_x, max_y = country_shape.bounds
        print(f"Bounding box edges: ({min_x}, {min_y}) -> ({max_x}, {max_y})")

        edges = {
            "bottom_left": (min_x, min_y),
            "bottom_right": (max_x, min_y),
            "top_right": (max_x, max_y),
            "top_left": (min_x, max_y)
        }
        gj = edges_to_geojson_rectangle(edges)
        #print(json.dumps(gj, indent=2))
        """

    # Split the country into bounding boxes
    bbox_splitter = UtmZoneSplitter([country_shape], country.crs, box_size)

    bbox_list = np.array(bbox_splitter.get_bbox_list())
    bbox_info_list = np.array(bbox_splitter.get_info_list())
    #""" Coordinates for new rect
    # Calculate the edges of the combined bounding boxes (grid edges)
    # Get all unique x and y coordinates from the bboxes
    all_x_coords = []
    all_y_coords = []
    for bbox in bbox_list:
        bbox_min_x, bbox_min_y, bbox_max_x, bbox_max_y = bbox
        all_x_coords.extend([bbox_min_x, bbox_max_x])
        all_y_coords.extend([bbox_min_y, bbox_max_y])

    # Get the outer edges of the grid
    grid_min_x = min(all_x_coords)
    grid_max_x = max(all_x_coords)
    grid_min_y = min(all_y_coords)
    grid_max_y = max(all_y_coords)

    # Create edges dictionary for the combined grid
    grid_edges = {
        "bottom_left": (grid_min_x, grid_min_y),
        "bottom_right": (grid_max_x, grid_min_y),
        "top_right": (grid_max_x, grid_max_y),
        "top_left": (grid_min_x, grid_max_y)
    }

    # Convert to GeoJSON points
    grid_gj = edges_to_geojson_rectangle(grid_edges)
    #print("\nCombined grid edges:")
    #print(json.dumps(grid_gj, indent=2))
    with open("coord2img/results/new_area.geojson", 'w') as f:
        json.dump(grid_gj, f, indent=2)
        #"""

    if save_img:
        # Prepare info of bboxes
        geometry = [Polygon(bbox.get_polygon()) for bbox in bbox_list]
        idxs = [info["index"] for info in bbox_info_list]
        idxs_x = [info["index_x"] for info in bbox_info_list]
        idxs_y = [info["index_y"] for info in bbox_info_list]

        # Display bboxes over country
        bbox_gdf = gpd.GeoDataFrame({"index": idxs, "index_x": idxs_x, "index_y": idxs_y}, crs=country.crs, geometry=geometry)
        fig, ax = plt.subplots(figsize=(20, 20))
        country.plot(ax=ax, facecolor="w", edgecolor="b", alpha=0.5)
        bbox_gdf.plot(ax=ax, facecolor="w", edgecolor="r", alpha=0.5)

        for bbox, info in zip(bbox_list, bbox_info_list):
            geo = bbox.geometry
            ax.text(geo.centroid.x, geo.centroid.y, info["index"], ha="center", va="center")

        plt.axis("off");
        plt.savefig('coord2img/results/bboxed.png',bbox_inches='tight')
    return bbox_list, bbox_info_list

# Function to plot the RGB data of the bounding boxes
def plot_slovenia_bbox_rgb(bbox_list, info_list, year, data):
    rows = max([info["index_y"] for info in info_list]) + 1
    cols = max([info["index_x"] for info in info_list]) + 1
    
    fig = plt.figure(figsize=(cols, rows)) 
    
    w, h = 1.0 / cols, 1.0 / rows

    for bbox, info in zip(bbox_list, info_list):
        x_pos = info["index_x"] * w
        y_pos = info["index_y"] * h
        ax = fig.add_axes([x_pos, y_pos, w, h])
        # Clip the data to the range [0,1] and multiply by 3.5 to increase contrast
        ax.imshow(np.clip((data[(year, info["index"])][:, :, :3]) * 3.5, 0, 1))
        ax.set_aspect("equal")
        ax.set_xticks([])
        ax.set_yticks([]) 
        ax.set_frame_on(False)
        ax.axis("off")
    plt.savefig('coord2img/results/bboxed_rgb.png', bbox_inches='tight', pad_inches=0)  # Save without padding

# Function to plot the forest data of the bounding boxes
green_white = mcolors.LinearSegmentedColormap.from_list(
    "green_white", ["white", "lightgreen", "darkgreen"], N=256
)

colors_ndwi = [
    (1.0, 1.0, 1.0),
    (0.0, 0.0, 0.75),
    (0.0, 0.0, 1.0)
]
ndwi_cmap = mcolors.ListedColormap(colors_ndwi)

def plot_bbox_water(bbox_list, info_list, year, data):
    rows = max([info["index_y"] for info in info_list]) + 1
    cols = max([info["index_x"] for info in info_list]) + 1
    cmap = colors.ListedColormap(['white', 'green'])
    fig = plt.figure(figsize=(cols, rows)) 
    
    w, h = 1.0 / cols, 1.0 / rows

    for bbox, info in zip(bbox_list, info_list):
        x_pos = info["index_x"] * w
        y_pos = info["index_y"] * h
        ax = fig.add_axes([x_pos, y_pos, w, h])
        #ax.imshow(data[(year, info["index"])]>treshold,cmap=cmap)
        ax.imshow(data[(year, info["index"])], cmap=ndwi_cmap, vmin=-1, vmax=1)
        ax.set_aspect("equal")
        ax.set_xticks([])
        ax.set_yticks([]) 
        ax.set_frame_on(False)
        ax.axis("off")
    plt.savefig('coord2img/results/water.png', bbox_inches='tight', pad_inches=0)  # Save without padding


colors_ndvi = [
    (0.05, 0.05, 0.05),  # NDVI < -0.5
    (0.75, 0.75, 0.75),  # NDVI < -0.2
    (0.86, 0.86, 0.86),  # NDVI < -0.1
    (0.92, 0.92, 0.92),  # NDVI < 0
    (1.0, 0.98, 0.8),    # NDVI < 0.025
    (0.93, 0.91, 0.71),  # NDVI < 0.05
    (0.87, 0.85, 0.61),  # NDVI < 0.075
    (0.8, 0.78, 0.51),   # NDVI < 0.1
    (0.74, 0.72, 0.42),  # NDVI < 0.125
    (0.69, 0.76, 0.38),  # NDVI < 0.15
    (0.64, 0.8, 0.35),   # NDVI < 0.175
    (0.57, 0.75, 0.32),  # NDVI < 0.2
    (0.5, 0.7, 0.28),    # NDVI < 0.25
    (0.44, 0.64, 0.25),  # NDVI < 0.3
    (0.38, 0.59, 0.21),  # NDVI < 0.35
    (0.31, 0.54, 0.18),  # NDVI < 0.4
    (0.25, 0.49, 0.14),  # NDVI < 0.45
    (0.19, 0.43, 0.11),  # NDVI < 0.5
    (0.13, 0.38, 0.07),  # NDVI < 0.55
    (0.06, 0.33, 0.04),  # NDVI < 0.6
    (0.0, 0.27, 0.0),    # NDVI >= 0.6
]

# Create a discrete colormap using these colors
ndvi_cmap = mcolors.ListedColormap(colors_ndvi)

def plot_slovenia_bbox_forest(bbox_list, info_list, year, data, treshold):
    rows = max([info["index_y"] for info in info_list]) + 1
    cols = max([info["index_x"] for info in info_list]) + 1
    fig = plt.figure(figsize=(cols, rows)) 
    
    w, h = 1.0 / cols, 1.0 / rows

    for bbox, info in zip(bbox_list, info_list):
        x_pos = info["index_x"] * w
        y_pos = info["index_y"] * h
        ax = fig.add_axes([x_pos, y_pos, w, h])
        #ax.imshow(data[(year, info["index"])]>treshold,cmap=cmap)
        ax.imshow(data[(year, info["index"])], cmap=ndvi_cmap, vmin=-1, vmax=1)
        ax.set_aspect("equal")
        ax.set_xticks([])
        ax.set_yticks([]) 
        ax.set_frame_on(False)
        ax.axis("off")
    plt.savefig('coord2img/results/forest.png', bbox_inches='tight', pad_inches=0)  # Save without padding

# Function to plot country data without bounding boxes
def plot_slovenia_rgb(year, data):
    plt.figure(figsize=(data[(year)].shape[1]/100, data[(year)].shape[0]/100 ), dpi=100)
    plt.imshow(np.clip((data[(year)][:, :, :3]) * 3.5, 0, 1))
    plt.axis("off")
    plt.savefig('coord2img/results/rgb.png', bbox_inches='tight', pad_inches=0)  # Save

def plot_slovenia_forest(year, data, treshold):
    plt.figure(figsize=(data[(year)].shape[1]/100, data[(year)].shape[0]/100 ), dpi=100)
    cmap = colors.ListedColormap(['white', 'green'])
    plt.imshow(data[(year)]>treshold,cmap=cmap)
    plt.axis("off")
    plt.savefig('coord2img/results/F.png', bbox_inches='tight', pad_inches=0)  # Save

