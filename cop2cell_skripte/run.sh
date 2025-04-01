#!/bin/bash

# preveri ali je dovolj argumentov
if [ "$#" -lt 7 ]; then
        echo "Uporaba: $0 <IME_NDIV.png> <IME_VODA.png> <XLLCORNER> <YLLCORNER> <CELLSIZE> <IME.geojson> <DATUM_ZACETNI - YYYY-MM-DD> <DATUM_KONCNI - YYYY-MM-DD> <IME_SCENARIJ>"
    exit 1
fi

# doloci vrednosti
SLIKA_NDIV=$1
SLIKA_VODA=$2
XLLCORNER=$3
YLLCORNER=$4
CELLSIZE=${5:-100}  # nastimaj na 100 po default
IME_GEOJSON=${6}
DATUM_ZACETNI=${7}
DATUM_KONCNI=${8}
IME_SCENARIJ=${9}

# zazeni ukaze po vrsti
python3 png2Forest.py "$SLIKA_NDIV" "$SLIKA_VODA" "$XLLCORNER" "$YLLCORNER" "$CELLSIZE" --output Forest.asc
python3 api2elevation.py "$IME_GEOJSON"
python3 ele2slope.py
python3 api2Weather.py "$IME_GEOJSON" "$DATUM_ZACETNI" "$DATUM_KONCNI" "$IME_SCENARIJ"
echo "Konec generiranja, lep pozdrav."
