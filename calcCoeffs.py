# Berechne Correlation Coeff
# Zielformat: numpy matrix

import os
import pandas as pd
import numpy as np

# importiere Konfigurationsparameter
import config


# functions
# read csv
def readcsv(file):
    if os.path.isfile(file):
        return pd.read_csv(file, **config.csv_args_r)
    else:
        return pd.DataFrame()

# Listenframe
liste = readcsv(config.listenpath)

# Read each CSV file into DataFrame
# merge into our target dataframe
counter=0
for id in liste['id']:
    df = readcsv(config.targetpath + "/" + str(id) + ".csv")
    if not df.empty:
        df = df[['jahr','anzahl']].rename(columns={'anzahl':id})
        if counter==0:
            statistics_df=df
        else:
            statistics_df = statistics_df.merge(df, on = 'jahr', how = 'outer')
        counter +=1

#calc correlation matrix
statistics_df = statistics_df.set_index('jahr')
corrs=statistics_df.corr(method='pearson', min_periods=3)
corrs.rename_axis('id', inplace=True)

#save corr matrix and big target dataframe to csv
config.csv_args_w['index']=True
corrs.to_csv(config.corrpath, **config.csv_args_w)
statistics_df.to_csv(config.statisticspath, **config.csv_args_w)
print(counter, 'statistics correlated and saved.')