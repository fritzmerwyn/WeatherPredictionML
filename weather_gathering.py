from datetime import datetime, timedelta
from collections import namedtuple
import requests
from pyprind import ProgBar


## CONSTANTS ##

#################################################################################
## Sample requeset url for Biebertal,Koenigsberg (location in degrees)
## starting on the 01.01.2015 CET given in Unix-Time for daily-means,
## without any alerts, flags, hourly, minutely or currently accesses.

# ----  https://api.darksky.net/forecast/99bd5e74c583d752453ecf8c2c025536/50.644308,8.536081,1420074000?units=si&exclude=currently,minutely,hourly,alerts,flags
#################################################################################

target_date = datetime(2015,1,1,hour=1) # hour=1 because in of CET is GMT+1:00h
#url_time = str(int(target_date.timestamp()))
features = ["date", "moonPhase", "precipIntensity", "precipIntensityMax", "precipProbability", "temperatureHigh", "temperatureLow",
            "apparentTemperatureHigh", "apparentTemperatureLow", "dewPoint", "humidity", "windSpeed",
            "windGust",
            "windBearing",
             "cloudCover",
             "uvIndex",
             "visibility",
              "temperatureMax", "temperatureMin", "apparentTemperatureMax", "apparentTemperatureMin"
             ]

DailySummary = namedtuple("DailySummary", features)


# --------- User Settings ---------
CITY = "Biebertal,KB"
GPS_COORDS = "50.644308,8.536081"
DARKSKY_API_KEY = '99bd5e74c583d752453ecf8c2c025536'
# ---------------------------------

#api_conditions_url = "https://api.darksky.net/forecast/" + DARKSKY_API_KEY + "/" + GPS_COORDS + "," + url_time + "?units=si&exclude=currently,minutely,hourly,alerts,flags"
# ---------- Get the data from darksky-website and store it in the tuple 'DailySummary' -----------
def extract_weather_data(darksky_api_key, gps_coords, target_date, days):
    records = []
    bar = ProgBar(days)
    for _ in range(days):
        url_time = str(int(target_date.timestamp()))
        request = "https://api.darksky.net/forecast/" + darksky_api_key + "/" + gps_coords + "," + url_time + "?units=si&exclude=currently,minutely,hourly,alerts,flags"
        response = requests.get(request, [])
        if response.status_code == 200:
            try:
                data = response.json()['daily']['data'][0]
                records.append(DailySummary(
                    date=target_date,
                    moonPhase=data['moonPhase'],
                    precipIntensity=data['precipIntensity'],
                    precipIntensityMax=data['precipIntensityMax'],
                    precipProbability=data['precipProbability'],
                    temperatureHigh=data['temperatureHigh'],
                    temperatureLow=data['temperatureLow'],
                    apparentTemperatureHigh=data['apparentTemperatureHigh'],
                    apparentTemperatureLow=data['apparentTemperatureLow'],
                    dewPoint=data['dewPoint'],
                    humidity=data['humidity'],
                    windSpeed=data['windSpeed'],
                    windGust=data['windGust'],
                    windBearing=data['windBearing'],
                    cloudCover=data['cloudCover'],
                    uvIndex=data['uvIndex'],
                    visibility=data['visibility'],
                    temperatureMax=data['temperatureMax'],
                    temperatureMin=data['temperatureMin'],
                    apparentTemperatureMax=data['apparentTemperatureMax'],
                    apparentTemperatureMin=data['apparentTemperatureMin']))
            except KeyError:
                bar.update()
                target_date += timedelta(days=1)
                continue

        #time.sleep(6)
        bar.update()
        target_date += timedelta(days=1)
    return records

# ----------- get the date prior 1000 days from today ---------
def get_target_date():
    current_date = datetime.now()
    target_date = current_date - timedelta(days=1000)
    return target_date


#def get_current_conditions():
#	api_conditions_url = "https://api.darksky.net/forecast/" + DARKSKY_API_KEY + "/" + GPS_COORDS + "," + url_time + "?units=si&exclude=currently,minutely,hourly,alerts,flags"
#	try:
#		f = requests.get(api_conditions_url)
#	except:
#		return []
#	json_currently = f.json()
#	return json_currently
