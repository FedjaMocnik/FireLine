import warnings
warnings.filterwarnings("ignore", message="Signature .* does not match any known type") # To filter warning from numpy

from coord2img.utils.geojson_tools import *
from coord2img.obdelava.data_generation import get_data


# Creates .geojson file from coordinates
# SMALL AREAS ONLY as too many requests are rejected
# koordinate tivoli:(456231.740204,5102686.348333),(461467.877750,5099408.768305)
create_geojson_rectangle((456231.740204,5102686.348333),(461467.877750,5099408.768305))

# Gets data form setelites and saves it to coord2img/results
get_data()

