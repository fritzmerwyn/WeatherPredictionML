import pickle
import pandas as pd

from weather_gathering import features

with open('records.pkl', 'rb') as fp:
    records = pickle.load(fp)

df = pd.DataFrame(records, columns=features).set_index('date')

# ---- function to get the nth prior measurement and shift the column down N lines -----
def derive_nth_day_feature(df, features, N):
    nth_prior_measurements = df[features].shift(periods=N)
    col_name = f'{feature}_{N}'
    df[col_name] = nth_prior_measurements

# ---- for-loop to actually create N more columns/lines for prior measurements ----------
for feature in features:
    if feature != 'date':
        for N in range(1,4):
            derive_nth_day_feature(df, feature, N)

# ---- make list of original features without temperatureMax, temperatureMin, apparentTemperatureMax and apparentTemperatureMin
# ---- since we want to predict the temperature with those in the future, and dont want to 'reduce' the amount of data with them.
to_dump = [
    feature for feature in features
    if feature not in ['temperatureMax', 'temperatureMin', 'apparentTemperatureMax', 'apparentTemperatureMin']
]

# make a list of columns to keep, with which we can 'play' and reduce (the amount of data with).
to_keep = [col for col in df.columns if col not in to_dump]

df = df[to_keep]

df = df.apply(pd.to_numeric, errors='coerce')

# Call describe on df and transpose it due to the large number of columns
spread = df.describe().T

# precalculate interquartile range for ease of use in next calculation
IQR = spread['75%'] - spread['25%']

# create an outliers column which is either 3 IQRs below the first quartile or
# 3 IQRs above the third quartile
spread['outliers'] = (spread['min'] <
                      (spread['25%'] -
                       (3 * IQR))) | (spread['max'] >
                                      (spread['75%'] + 3 * IQR))

# just display the features containing extreme outliers
# spread.ix[spread.outliers,]
