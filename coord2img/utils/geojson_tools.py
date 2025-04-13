from pyproj import Transformer
import json
import shutil
from pathlib import Path
import csv

def create_geojson_rectangle(top_left, bottom_right, output_file="./coord2img/utils/input_area.geojson"):
    """
    Create a GeoJSON file with a rectangle polygon from two corner coordinates.
    
    Args:
        top_left (tuple): (x, y) coordinates of top-left corner
        bottom_right (tuple): (x, y) coordinates of bottom-right corner
        output_file (str): Path to output GeoJSON file
        coordinates have to be 32633 - UTM 33N)
    """
    # Extract coordinates
    tl_x, tl_y = top_left
    br_x, br_y = bottom_right
    
    # Calculate all four corners (clockwise order)
    polygon_coords = [
        [tl_x, tl_y],       # Top-left
        [tl_x, br_y],       # Bottom-left
        [br_x, br_y],       # Bottom-right
        [br_x, tl_y],       # Top-right
        [tl_x, tl_y]        # Close the polygon
    ]
    
    # Create GeoJSON structure
    geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {},
                "geometry": {
                    "coordinates": [polygon_coords],
                    "type": "Polygon"
                }
            }
        ],
        "crs": {
            "type": "name",
            "properties": {
                "name": f"urn:ogc:def:crs:EPSG::32633"
            }
        }
    }
    
    # Save to file
    with open(output_file, 'w') as f:
        json.dump(geojson, f, indent=4)
    print(f"GeoJSON file saved to {output_file}")

def utm33n_to_latlon(easting, northing):
    """Convert UTM Zone 33N coordinates to WGS84 latitude/longitude"""
    transformer = Transformer.from_crs(32633, 4326, always_xy=True)
    lon, lat = transformer.transform(easting, northing)
    return lat, lon  # return as (lat, lon) for consistency

def latlon_to_utm33n(lat, lon):
    """Convert WGS84 latitude/longitude to UTM Zone 33N coordinates"""
    transformer = Transformer.from_crs(4326, 32633, always_xy=True)
    easting, northing = transformer.transform(lon, lat)
    return easting, northing  # return as (easting, northing)

def edges_to_geojson_points(edges, input_crs=32633):
    """
    Convert edge coordinates to GeoJSON Point features, with optional coordinate conversion.
    
    Args:
        edges (dict): Dictionary containing corner coordinates in either:
            - UTM 33N (if input_crs=32633)
            - WGS84 (if input_crs=4326)
            Format: {
                "bottom_left": (x, y),
                "bottom_right": (x, y),
                "top_right": (x, y),
                "top_left": (x, y)
            }
        input_crs (int): EPSG code of input coordinates (default: 32633 for UTM 33N)
    
    Returns:
        dict: GeoJSON FeatureCollection of Point features in WGS84
    """
    features = []
    
    # Create a point feature for each corner
    corners = [
        ("bottom_left", edges["bottom_left"]),
        ("bottom_right", edges["bottom_right"]),
        ("top_right", edges["top_right"]),
        ("top_left", edges["top_left"])
    ]
    
    for name, (x, y) in corners:
        # Convert coordinates if input is UTM
        if input_crs == 32633:
            lat, lon = utm33n_to_latlon(x, y)
            coords = [lon, lat]  # GeoJSON uses (longitude, latitude)
        else:
            coords = [x, y]  # Assume already in (lon, lat)
        
        feature = {
            "type": "Feature",
            "properties": {
                "corner": name,
                "original_x": x,
                "original_y": y
            },
            "geometry": {
                "coordinates": coords,
                "type": "Point"
            }
        }
        features.append(feature)
    
    return {
        "type": "FeatureCollection",
        "features": features
    }

def edges_to_geojson_rectangle(edges, input_crs=32633):
    """
    Convert edge coordinates to GeoJSON Polygon feature, with optional coordinate conversion.
    
    Args:
        edges (dict): Dictionary containing corner coordinates in either:
            - UTM 33N (if input_crs=32633)
            - WGS84 (if input_crs=4326)
            Format: {
                "bottom_left": (x, y),
                "bottom_right": (x, y),
                "top_right": (x, y),
                "top_left": (x, y)
            }
        input_crs (int): EPSG code of input coordinates (default: 32633 for UTM 33N)
    
    Returns:
        dict: GeoJSON Feature containing Polygon geometry in WGS84
    """
    # Get all corners in order (clockwise or counter-clockwise)
    corners = [
        edges["bottom_left"],
        edges["bottom_right"],
        edges["top_right"],
        edges["top_left"],
        edges["bottom_left"]  # Close the polygon
    ]
    
    # Convert coordinates if needed
    if input_crs == 32633:
        converted_coords = []
        for x, y in corners:
            lat, lon = utm33n_to_latlon(x, y)
            converted_coords.append([lon, lat])  # GeoJSON uses (longitude, latitude)
        coordinates = [converted_coords]
    else:
        coordinates = [[[x, y] for x, y in corners]]  # Already in (lon, lat)
    
    return {
        "type": "Feature",
        "properties": {
            "description": "Rectangle from bounding edges",
            "crs_original": f"EPSG:{input_crs}"
        },
        "geometry": {
            "type": "Polygon",
            "coordinates": coordinates
        }
    }

def copy_file(filename, src_dir, dest_dir, new_name=None):
    src = Path(src_dir) / filename
    dest_filename = new_name if new_name else filename
    dest = Path(dest_dir) / dest_filename
    Path(dest_dir).mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)
    
