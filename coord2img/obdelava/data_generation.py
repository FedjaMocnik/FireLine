
from pathlib import Path
import numpy as np
import pandas as pd
import argparse
from sentinelhub import SentinelHubDownloadClient
import sys
import time

sys.path.append("../0_utils")
try:
    from utils import (
        SHub_profile,
        load_slovenia_bbox,
        create_SHrequest,
        plot_slovenia_bbox_rgb,
        plot_slovenia_bbox_forest,
        plot_bbox_water,
        plot_slovenia_forest
    )
except ImportError:
    from coord2img.utils.utils import (
        SHub_profile,
        load_slovenia_bbox,
        create_SHrequest,
        plot_slovenia_bbox_rgb,
        plot_slovenia_bbox_forest,
        plot_bbox_water,
        plot_slovenia_forest
    )

def parse_arguments():
    parser = argparse.ArgumentParser(description="Process deforestation data.")
    parser.add_argument(
        "--box_size",
        type=int,
        default=2000,
        help="Size of the bounding boxes in meters.",
    )
    parser.add_argument(
        "--resolution",
        type=int,
        default=10,
        help="Resolution for the bounding boxes in m/px.",
    )
    parser.add_argument(
        "--start_year", type=int, default=2024, help="Start year for the data."
    )
    parser.add_argument(
        "--end_year", type=int, default=2024, help="End year for the data."
    )
    parser.add_argument(
        "--data_folder",
        type=Path,
        default=Path("../data"),
        help="Folder to store the data.",
    )
    parser.add_argument(
        "--nvdi_treshold", type=float, default=0.7, help="Treshold for the NDVI index."
    )
    return parser.parse_args()

def get_default_args():
    return {
        "box_size": 2000,
        "resolution": 10,
        "start_year": 2024,
        "end_year": 2024,
        "data_folder": Path("../data"),
        "nvdi_treshold": 0.7,
    }

# Evalscript for the SH request
# reference: https://documentation.dataspace.copernicus.eu/notebook-samples/sentinelhub/deforestation_monitoring_with_xarray.html
evalscript_cloudless = """
// Define the channels which we want from the Satellite
// refence: https://gisgeography.com/sentinel-2-bands-combinations/
// B08 - Near Infrared (NIR)
// B04 - Red
// B03 - Green
// B02 - Blue
// SCL - Scene Classification Map
// Use SCL to remove cloudy data
function setup() {
    return {
        input: [{
                bands: ["B02","B03","B04","B08","SCL"],
                units: "DN"
            }],
        output: {
            bands: 4,
            sampleType: "INT16",
        },
        mosaicking: "ORBIT"
    }
}

function getFirstQuartileValue(values) {
    values.sort((a,b) => a-b);
    return getFirstQuartile(values);
}

function getFirstQuartile(sortedValues) {
    var index = Math.floor(sortedValues.length / 4);
    return sortedValues[index];
}

function validate(sample) {
    // Define codes as invalid:
    const invalid = [
        0, // NO_DATA
        1, // SATURATED_DEFECTIVE
        3, // CLOUD_SHADOW
        7, // CLOUD_LOW_PROBA
        8, // CLOUD_MEDIUM_PROBA
        9, // CLOUD_HIGH_PROBA
        10 // THIN_CIRRUS
    ]
    return !invalid.includes(sample.SCL)
}

function evaluatePixel(samples) {
    var valid = samples.filter(validate);
    if (valid.length > 0 ) {
        let cloudless = {
            b08: getFirstQuartileValue(valid.map(s => s.B08)),
            b04: getFirstQuartileValue(valid.map(s => s.B04)),
            b03: getFirstQuartileValue(valid.map(s => s.B03)),
            b02: getFirstQuartileValue(valid.map(s => s.B02)),
        }
        let data = [cloudless.b04, cloudless.b03, cloudless.b02, cloudless.b08];
        return data
    }
    // If there isn't enough data, return NODATA
    return [-32768, -32768, -32768, -32768]
}
"""
def get_data():

    # Set the Sentinel Hub profile
    config = SHub_profile("", "")

    # Load the bounding boxes for Slovenia
    if __name__ == "__main__":
        geojson_path = "./input_area.geojson"
    else:
        args = argparse.Namespace(**get_default_args())
        geojson_path = "./coord2img/utils/input_area.geojson"
    bbox_list, bbox_info_list = load_slovenia_bbox(geojson_path,args.box_size, save_img=True)

    start_year = args.start_year
    end_year = args.end_year
    data_folder = args.data_folder

    # Desired resolution of our data in m/px.
    # Default is 100m/px
    resolution = (args.resolution, args.resolution)
    # Number of channels in the data
    channels = 4

    # Create a dataframe to store the forest area data
    forest_area_df = pd.DataFrame(columns=["year", "forest_area", "total_area", "ratio"])
    ndvi_dict = {}
    ndwi_dict = {}
    data_dict = {}

    year = 2024

    print(f"Downloading data for {year}")

    bbox_forest_area_km2 = 0
    sh_requests = {}
    # Create the requests for the data
    print(f"Number of bboxes to load: {len(bbox_list)} (???/s)")
    for i, box in enumerate(bbox_list):
        time.sleep(1)
        sh_requests[(i, year)] = create_SHrequest(
            year, box, resolution, evalscript_cloudless, config, data_folder=data_folder
        )
    list_of_requests = [request.download_list[0] for request in sh_requests.values()]

    # Download data with multiple threads
    data = SentinelHubDownloadClient(config=config).download(
        list_of_requests, max_threads=3, show_progress=True
    )

    print("Download completed")

    for i, box in enumerate(bbox_list):
        # Repack the data
        bbox_size = args.box_size // args.resolution

        # Divide by 10000 to get the data in the range [0,1]
        data_dict[(year, i)] = (
            np.array(data[i]).reshape(bbox_size, bbox_size, channels) / 10000 + 1e-6
        )

        # Calculate the ndvi - Normalized Difference Vegetation Index
        # Reference: https://gisgeography.com/ndvi-normalized-difference-vegetation-index/
        #NIR-red/NIR+red
        ndvi = (data_dict[(year, i)][:, :, 3] - data_dict[(year, i)][:, :, 0]) / (
            data_dict[(year, i)][:, :, 3] + data_dict[(year, i)][:, :, 0]
        )

        #calculate ndwi
        ndwi = (data_dict[(year, i)][:, :, 1] - data_dict[(year, i)][:, :, 3]) / (
            data_dict[(year, i)][:, :, 1] + data_dict[(year, i)][:, :, 3]
        ) 
        
        ndvi_dict[(year, i)] = ndvi
        ndwi_dict[(year, i)] = ndwi



    plot_slovenia_bbox_rgb(bbox_list, bbox_info_list, end_year, data_dict)
    plot_slovenia_bbox_forest(
        bbox_list, bbox_info_list, end_year, ndvi_dict, args.nvdi_treshold
    )
    plot_bbox_water(
        bbox_list, bbox_info_list, end_year, ndwi_dict
    )


if __name__ == "__main__":
    args = parse_arguments()

    get_data()
