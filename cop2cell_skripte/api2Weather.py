# VERZIJA: 0.1.0
# ZAZENI TAKO:
# python3 api2Weather.py {IME.GEOJSON} {DATUM_ZACETKA}{IME_SCENARIJA}
# NPR: python3 api2Weather.py slika.geojson 2024-06-14 s1

# requirements ce kej manjka:
# pip install openmeteo-requests requests-cache retry-requests numpy pandas rasterio shapely geojson

import math
import numpy as np
import openmeteo_requests
import requests_cache
import pandas as pd
import argparse
from retry_requests import retry
import json
from shapely.geometry import shape
from datetime import datetime
from datetime import timedelta

def fetch_weather_data(latitude, longitude, start_date, scenario_value, output_path="Weather.csv"):
    
    # izracunamo end_date
    # string --> datetime object
    given_date = datetime.strptime(start_date,"%Y-%m-%d")
    #izracunamo nov datum -> koncni datum (zacetni + 5 dni)
    end_date = (given_date + timedelta(days=1)).date()
    
    # nastavi Open-Meteo API client z cacheom in ponovi ob napaki
    cache_session = requests_cache.CachedSession('.cache', expire_after = -1)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    # ce je zacetni datum manj kot en mesec nazaj uporabimo forecast API ce ne historical API
    danes = datetime.today().date()
    mesec_nazaj = danes - timedelta(days=30)

    if given_date.date() < mesec_nazaj:
        # historical API
        url = "https://archive-api.open-meteo.com/v1/archive"
        print("Given date is more than one month ago.")
        
    else:
        # forecast API
        url = "https://api.open-meteo.com/v1/forecast"
        print("Given date is within the last month.")

    # pomemben vrstni red parametrov !
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "hourly": ["temperature_2m", "wind_speed_10m", "wind_direction_10m", "relative_humidity_2m", "precipitation"]
    }
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]

    # podatki po urah, vrstni red enak kot requestano
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_wind_speed_10m = hourly.Variables(1).ValuesAsNumpy()
    hourly_wind_direction_10m = hourly.Variables(2).ValuesAsNumpy()
    hourly_relative_humidity_2m = hourly.Variables(3).ValuesAsNumpy()
    hourly_precipitation = hourly.Variables(4).ValuesAsNumpy()
    
    # datumi in ure
    datetime_range = pd.date_range(
        start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
        end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=hourly.Interval()),
        inclusive="left"
    )
    
    hourly_data = {
        "Scenario": [scenario_value] * len(datetime_range),
        "datetime": datetime_range.strftime("%Y-%m-%d %H:%M"),  # Format v "YYYY-MM-DD HH:MM" 
        "APCP": np.round(hourly_precipitation, 1), # APCP - Accumulate Precipitation
        "TMP": np.round(hourly_temperature_2m, 1), 
        "RH": np.round(hourly_relative_humidity_2m, 1),
        "WS": np.round(hourly_wind_speed_10m, 1),
        "WD": np.round(hourly_wind_direction_10m, 0)
    }

    # podatki --> pandas tabela
    hourly_dataframe = pd.DataFrame(data = hourly_data)
    
    hourly_dataframe["datetime"] = pd.to_datetime(hourly_dataframe["datetime"], format="%Y-%m-%d %H:%M") #datetime v pravi format

    # IZRACUNAMO FFMC, DMC, DC, ISI, BUI, FWI:
    
    # ker so to dnevni indeksi rabimo vrstice v katerih so podatki opoldne
    measurements_at_noon = hourly_dataframe[hourly_dataframe["datetime"].dt.hour == 13][["datetime", "APCP", "TMP", "RH", "WS"]]
    
    daily_ffmc = []
    prev_ffmc = 88 # povprecni suhi pogoji
    daily_dmc = []
    prev_dmc = 70 # suhi pogoji
    daily_dc = []
    prev_dc = 250 # suhi pogoji
    daily_isi = []
    daily_bui = []
    daily_fwi = []
    
    for _, row in measurements_at_noon.iterrows():
        # FFMC
        ffmc_value = calculate_ffmc(row["TMP"], row["RH"], row["WS"], row["APCP"], prev_ffmc)
        daily_ffmc.append(ffmc_value)
        prev_ffmc = ffmc_value

        # DMC
        dmc_value = calculate_dmc(row["TMP"], row["RH"], row["APCP"], prev_dmc)
        daily_dmc.append(dmc_value)
        prev_dmc = dmc_value

        # DC
        dc_value = calculate_dc(row["TMP"], row["APCP"], prev_dc) 
        daily_dc.append(dc_value)
        prev_dc = dc_value
        
        # ISI
        isi_value = calculate_ISI(row["WS"], ffmc_value) 
        daily_isi.append(isi_value)
        
        # BUI
        bui_value = calculate_BUI(dmc_value, dc_value) 
        daily_bui.append(bui_value)
        
        # FWI
        fwi_value = calculate_FWI(bui_value, isi_value) 
        daily_fwi.append(fwi_value)
        
    hourly_dataframe["date"] = hourly_dataframe["datetime"].dt.date # 'date' stolpec za dodajanje podatkov po dnevih
    
    # slovar: datum -> izracunane vrednosti
    daily_ffmc_dict = dict(zip(hourly_dataframe["datetime"].dt.date.unique(), daily_ffmc))
    daily_dmc_dict = dict(zip(hourly_dataframe["datetime"].dt.date.unique(), daily_dmc))
    daily_dc_dict = dict(zip(hourly_dataframe["datetime"].dt.date.unique(), daily_dc))
    daily_isi_dict = dict(zip(hourly_dataframe["datetime"].dt.date.unique(), daily_isi))
    daily_bui_dict = dict(zip(hourly_dataframe["datetime"].dt.date.unique(), daily_bui))
    daily_fwi_dict = dict(zip(hourly_dataframe["datetime"].dt.date.unique(), daily_fwi))
    
    # dodamo izracunane vrednosti v dataframe glede na datum
    hourly_dataframe["FFMC"] = hourly_dataframe["date"].map(daily_ffmc_dict)
    hourly_dataframe["DMC"] = hourly_dataframe["date"].map(daily_dmc_dict)
    hourly_dataframe["DC"] = hourly_dataframe["date"].map(daily_dc_dict)
    hourly_dataframe["ISI"] = hourly_dataframe["date"].map(daily_isi_dict)
    hourly_dataframe["BUI"] = hourly_dataframe["date"].map(daily_bui_dict)
    hourly_dataframe["FWI"] = hourly_dataframe["date"].map(daily_fwi_dict)


    # odstranimo 'date' stolpec ko ga vec ne rabimo za dodajanje podatkov po dnevih
    hourly_dataframe = hourly_dataframe.drop(columns=["date"])

    # vzamemo podatke od 12:00 naprej v prvem dnevu --> najbolj ugodni pogoji za zacetek pozara
    hourly_df_filtered = hourly_dataframe.drop(hourly_dataframe.index[:12]).reset_index(drop=True)
    
    # zapisemo v izhodno datoteko
    hourly_df_filtered.to_csv(output_path, index=False)



# FUNKCIJE ZA IZRACUN FFMC, DMC, DC, ISI, BUI, FWI
# formule iz https://ostr-backend-prod.azurewebsites.net/server/api/core/bitstreams/64b76432-d29e-411d-9f67-3466c6e2d2da/content in https://wikifire.wsl.ch/tiki-index259b.html?page=Fire+weather+index 
# Fine Fuel moisture Code (FFMC)
def calculate_ffmc(T, RH, Wind, Rain, prev_FFMC):
    """
    Izracun Fine Fuel Moisture Code (FFMC) glede na vreme opoldne.
    
    Parameteri:
    - T: Temperature (°C)
    - RH: Relative Humidity (%)
    - Wind: Wind Speed (km/h)
    - Rain: Rainfall (mm)
    - prev_FFMC: FFMC prejsnjega dne

    Vrne:
    -novi FFMC 
    """

    # 1: izracunamo Moisture Content 
    Mo = 147.2 * (101 - prev_FFMC) / (59.5 + prev_FFMC)
    
    # 2 in 3: ce je dezevalo (rain > 0.5mm)
    if Rain > 0.5:
        Rf = Rain - 0.5
        if (Mo <= 150): 
            Mr = Mo + 42.5 * Rf * math.exp(-100 / (251 - Mo)) * (1 - math.exp(-6.93 / Rf))
        else:
            Mr = Mo + 42.5 * Rf * math.exp(-100 / (251 - Mo)) * (1 - math.exp(-6.93 / Rf)) + 0.0015 * (Mo - 150) ** 2 * Rf ** 0.5
        
        if (Mr > 250):
            Mr = 250
        
        Mo = Mr
   
    # 4: izracunamo Drying Rate 
    Ed = 0.942 * (RH ** 0.679) + (11 * math.exp((RH - 100) / 10)) + 0.18 * (21.1 - T) * (1 - math.exp((-0.115) * RH))
    
    M = 0
    # 5:
    if Mo > Ed:
        Ko = 0.424 * (1 - ((RH/ 100) ** 1.7)) + (0.0694 * Wind ** 0.5) * (1 - ( RH / 100) ** 8)
        Kd = Ko * 0.581 * math.exp(0.0365 * T)
    
        M = Ed + (Mo - Ed) * 10 ** (-Kd)
    # 6:
    else:
        Ew = 0.618 * RH ** 0.753 + 10 * math.exp((RH - 100)/10) +  0.18 * (21.1 - T) * (1 - math.exp((-0.115) * RH))
        # 7:
        if Mo < Ew:
            K1 = 0.424 * (1 - ((100 - RH) / 100) ** 1.7) + (0.0694 * Wind ** 0.5) * (1 - ((100 - RH) / 100) ** 8)
            Kw = K1 * 0.581 * math.exp(0.0365 * T)
            
            M = Ew - (Ew - Mo) * 10 ** (-Kw)
        # 8:
        else:
            M = Mo 
 
            
    # 9: izracunamo FFMC
    FFMC = (59.5 * (250 - M)) / (147.2 + M)
    
    # preverimo da je v obmocju
    if FFMC > 101:
        FFMC = 101  # Max limit
    elif FFMC < 0:
        FFMC = 0  # Min limit

    return round(FFMC, 1)


# Duff Moisture Code

def calculate_dmc(T, RH, Rain, prev_DMC):
    """
    Izracun Duff Moisture Code (DMC) glede na vreme opoldne.
    
    Parameteri:
    - T : Temperature (°C)
    - RH : Relative Humidity (%)
    - Rain : Rainfall (mm)
    - prev_DMC : DMC vrednost prejsnjega dne
    
    Vrne:
    - novi DMC 
    """
    Pr = prev_DMC
    # 2: Rainfall Routine ce je rain > 1.5
    if (Rain > 1.5):
        # 2a
        Re = 0.92 * Rain - 1.27
        
        #2b
        Mo = 20 + math.exp(5.6348 - prev_DMC/43.43)
        
        # 2c
        b = 0
        if (prev_DMC <= 33):
            b = 100 / (0.5 + 0.3 * prev_DMC)
        elif (33 < prev_DMC and prev_DMC <= 65):
            b = 14 - 1.3 * math.log(prev_DMC)
        else:
            b = 6.2 * math.log(prev_DMC) - 17.2
        
        # 2d 
        Mr = Mo + (1000 * Re) / (48.77 + b * Re)
        
        # 2e
        Pr = 244.72 - 43.43 * math.log(Mr - 20)
        
        if (Pr < 0):
            Pr = 0
        
    # 3: Effective Day-Length 
    # iz tabele v dokumentaciji o teh kodah je 13.9 vrednost julija
    Le = 12.4
    
    # 4:
    if (T < -1.1):
        T = - 1.1
        
    K = 1.894 * (T + 1.1) * (100 - RH) * Le * 10 ** (-6)

    # 5: novi DMC
    DMC = Pr + 100 * K
    
    if DMC < 0:
        DMC = 0  # Min limit

    return round(DMC, 1)


# Drought Code (DC)
def calculate_dc(T, Rain, prev_DC):
    """
    Izracun Drought Code (DC) glede na vreme opoldne.
    
    Parameteri:
    - T: Temperature (°C)
    - Rain: Rainfall (mm)
    - prev_DC: DC prejsnjega dne

    Vrne:
    - novi DC 
    """
    
    # 2: ce je dezevalo vec kot 2.8 mm
    if (Rain > 2.8):
        #2a: effective rainfall
        Rd = 0.83 * Rain - 1.27
        #2b: the moisture equivalent of the previous day's DC
        Qo = 800 * math.exp((- prev_DC)/ 400)
        #2c: the moisture equivalent after rain
        Qr = Qo + 3.937 * Rd
        #2d
        Dr = 400 * math.log(800/Qr)
        if (Dr < 0):
            Dr = 0
            
        prev_DC = Dr

    # 3: Day-length factor
    Lf = 6.4 # vrednost julija (najvecja)
    
    # 4:
    if (T < -2.8):
        T = -2.8
    V = 0.36 * (T + 2.8) + Lf #potential evapotranspiration
    
    if (V < 0):
        V = 0
        
    # 5: novi DC
    D = prev_DC + 0.5 * V
    
    return round(D, 1)
    
# Initial Spread Index (ISI)
def calculate_ISI(Wind, FFMC):
    """
    Izracun Initial Spread Index (ISI) glede na FFMC in Wind Speed opoldne.

    Vrne:
    - novi ISI 
    """
    
    Fw = math.exp(0.05039 * Wind) # wind function 
    m = 147.2 * ((101 - FFMC)/(59.5 + FFMC)) # fuel moisture content
    Ff = 91.9 * math.exp(-0.1386 * m) * (1 + (m ** 5.31)/(4.93 * 10 ** 7)) # fine fuel moisture function
    R = 0.208 * Fw * Ff
    
    return round(R, 1)

# Buildup Index (BUI)
def calculate_BUI(DMC, DC):
    """
    Izracun Buildup Index (BUI) glede DMC in DC.

    Vrne:
    - novi BUI
    """
    U = 0
    if (DMC <= 0.4 * DC):
        U = 0.8 * (DMC * DC)/(DMC + 0.4 * DC)
    else:
        U = DMC - (1 - (0.8 * DC)/(DMC + 0.4 * DC)) * (0.92 + (0.0114 * DMC) ** 1.7)
    
    return round(U, 1)

# Fire Weather Index (FWI)
def calculate_FWI(BUI, ISI):
    """
    Izracun Fire Weather Index [FWI] glede BUI in ISI.

    Vrne:
    - novi FWI
    """
    Fd = 0
    if (BUI <= 80):
        Fd = 0.626 * BUI ** 0.809 + 2
    else:
        Fd = 1000/(25 + 108.64 * math.exp(-0.023 * BUI))
        
    B = 0.1 * ISI * Fd
    
    S = 0
    if (B > 1):
        S = math.exp(2.72 * (0.434 * math.log(B))** 0.647)
    else:
        S = B
        
    return round(S, 1)


###################################

def main():
    parser = argparse.ArgumentParser(description="Generiraj Weather.asc datoteko s pomočjo API in .geojson datoteke")
    parser.add_argument("geojson", help="Pot do geojson datoteke.")
    parser.add_argument("zacetekDatum", help="Datum zacetka pozara. Format: YYYY-MM-DD.")
    parser.add_argument("scenarij", help="Scenarij.")

    args = parser.parse_args()

    # PREBERI PODATKE IZ GEOJSON
    with open(args.geojson, "r") as f:
        geojson_data = json.load(f)

    polygon = shape(geojson_data["geometry"])
    minx, miny, maxx, maxy = polygon.bounds 

    latitude = (miny + maxy) / 2
    longitude = (minx + maxx) / 2

    fetch_weather_data(latitude, longitude, args.zacetekDatum, args.scenarij)

    print("Weather.csv je generiran. Verzija 0.1.0")

if __name__ == "__main__":
    main()  # Only runs if executed directly
    