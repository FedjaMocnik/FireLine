import json
from pyproj import Transformer

# Define the coordinate transformer
transformer = Transformer.from_crs("EPSG:4326", "EPSG:32633", always_xy=True)

# Read the input GeoJSON file
with open("test.geojson", "r") as f:
    geojson_data = json.load(f)

# Extract coordinates and convert them
for feature in geojson_data["features"]:
    coords = feature["geometry"]["coordinates"]
    if feature["geometry"]["type"] == "Polygon":
        feature["geometry"]["coordinates"] = [[list(transformer.transform(lon, lat)) for lon, lat in ring] for ring in coords]
    elif feature["geometry"]["type"] == "MultiPolygon":
        feature["geometry"]["coordinates"] = [[[list(transformer.transform(lon, lat)) for lon, lat in ring] for ring in poly] for poly in coords]

# Update CRS to EPSG:32633
geojson_data["crs"] = {
    "type": "name",
    "properties": {
        "name": "urn:ogc:def:crs:EPSG::32633"
    }
}

# Save the corrected file
with open("test_fixed.geojson", "w") as f:
    json.dump(geojson_data, f, indent=4)

print("Fixed GeoJSON saved")