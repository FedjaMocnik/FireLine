#!/bin/bash

if [ "$#" -lt 4 ];
then
    echo "Ni dovolj argumentov. Zazeni kot: $0 <PATH_TO_HOURLY_STATS> <PATH_TO_GRIDS> <SAVE_PATH> <PATH_TO_PNGS>"
    exit 1
fi

PATH_TO_HOURLY_STATS=$1
PATH_TO_GRIDS=$2
SAVE_PATH=$3
PATH_TO_PNGS=$4

#Primer uporabe:
#./start.sh resultsTolmin/results/Stats/HourlyStats.csv resultsTolmin/results/Grids/Grids1/ res/ testni_primer/


echo "Zacenjam algoritem za FireLine ..."
python3 fireline.py "$PATH_TO_HOURLY_STATS" "$PATH_TO_GRIDS" "$SAVE_PATH" "$PATH_TO_PNGS"
echo "Konec algoritma."
