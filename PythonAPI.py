# Dependencies and Setup
#import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
import time
import json

# Import API key
import api_keys
import plotly

# Incorporated citipy to determine city based on latitude and longitude
from citipy import citipy

#############################################################################
#############################################################################
def generte_city_datarame():
    # Range of latitudes and longitudes
    lat_range = (-90, 90)
    lng_range = (-180, 180)

    # List for holding lat_lngs and cities
    lat_lngs = []
    cities = []

    weather_df = pd.DataFrame([])

    # Create a set of random lat and lng combinations
    lats = np.random.uniform(low=-90.000, high=90.000, size=1500)
    lngs = np.random.uniform(low=-180.000, high=180.000, size=1500)
    lat_lngs = zip(lats, lngs)

    # Identify nearest city for each lat, lng combination
    for lat_lng in lat_lngs:
        city = citipy.nearest_city(lat_lng[0], lat_lng[1]).city_name

    # If the city is unique, then add it to a our cities list
        if city not in cities:
            cities.append(city)
            weather_df = weather_df.append(pd.DataFrame({"City": city, "latitude":lat_lng[0], "longitude":lat_lng[1]}, index=[0]), ignore_index=True)

    return weather_df

#################    Debug   ##################################################
print("------------ Weather ------------------------")
print(generte_city_datarame().head())


################################################################################
################################################################################
################################################################################
def get_wearther_API(weather_df):
    # OpenWeatherMap API Key
    units = "Imperial"
    params = {"appid":  api_keys.api_key,
            "units" : units,
            "q" : ""}

    # Starting URL for Weather Map API Call
    url = "http://api.openweathermap.org/data/2.5/weather?"

    #set the DataFrme with empty values
    weather_df['Temperature'] = np.nan
    weather_df['Humidity'] = np.nan
    weather_df['Cloudiness'] = np.nan
    weather_df['Wind Speed'] = np.nan

    #iterate over the citys and get data from each city
    for index, row in weather_df.iterrows():
        params["q"]= row["City"]
        #Call API to get Data
        response = requests.get(url, params=params).json()
        ##print(json.dumps(response, indent=4))
        #break
        #Fill the data
        try:
            weather_df.loc[index,"Temperature"] = response["main"]["temp_max"]
            weather_df.loc[index,"Humidity"] = response["main"]["humidity"]
            weather_df.loc[index,"Cloudiness"] = response["clouds"]["all"]
            weather_df.loc[index,"Wind Speed"] = response["wind"]["speed"]
            #Print City Index and City
            print(f"Processing Record {index} | {row['City']}")
            print (f'{url}units={params["units"]}APPID=xxxxxxxxx&q{params["q"]}')
        except:
            pass

    weather_df = weather_df.dropna()
    save_df('cities.csv', weather_df)

    return (weather_df)

################################################################################
################################################################################
def save_df(filename, weather_df):
    # Output File (CSV)
    import os

    outname = filename
    outdir = '../output_data'
    if not os.path.exists(outdir):
        os.mkdir(outdir)

    weather_df.to_csv(outdir + "/"+ outname)



################################################################################
print("------------ OpenWeather Map ------------------------")
print(get_wearther_API(generte_city_datarame()).head())
