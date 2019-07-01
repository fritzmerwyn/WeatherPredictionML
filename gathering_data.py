import os.path
import pickle
from datetime import timedelta

from weather_gathering import DARKSKY_API_KEY, GPS_COORDS, extract_weather_data, get_target_date

# ---- how many days do you want gather? -----
DAYS = 1000
# --------------------------------------------

filename1 = 'records.pkl'

target_date = get_target_date()

records = extract_weather_data(DARKSKY_API_KEY, GPS_COORDS, target_date, DAYS)

records_length = len(records)
print(f'{records_length} records collected from Wunderground API')

with open(filename1, 'wb') as f:
    pickle.dump(records, f)

    print(f'Weather records from day 1 saved to {filename1}.')
