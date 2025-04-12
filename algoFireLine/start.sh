#!/bin/bash

if [ "$#" -lt 4 ];
then
    echo "Ni dovolj argumentov. Zazeni kot: $0 <PATH_TO_HOURLY_STATS> <PATH_TO_GRIDS> <SAVE_PATH> <PATH_TO_PNGS>"
    exit 1
fi


# NE TEGA UPORABLAT K NASTIMAN DA MEN RUNA PAR TESTOV NAEKRAT
# sam zazen $ python3 fireline.py {path do HourlyStats.csv} {path do .../Grids/Grids1/} {path do mape kjer shran rezultate} {path do pngs}


#Primer uporabe:
#./start.sh Stats/HourlyStats.csv Grids/Grids1/ res/res testni_primer/

echo "Zacenjam algoritem za FireLine ..."


for i in {1..5}; do
    echo "  Sim $i..."
    PATH_TO_HOURLY_STATS="results$i/$1"
    PATH_TO_GRIDS="results$i/$2"
    SAVE_PATH="res/res$i/"
    PATH_TO_PNGS=$4

    python3 fireline.py "$PATH_TO_HOURLY_STATS" "$PATH_TO_GRIDS" "$SAVE_PATH" "$PATH_TO_PNGS"
done

echo "Konec algoritma."
