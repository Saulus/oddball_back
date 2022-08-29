# Extrahiere relevante Daten aus Destatis Genesis Flat files
# Zielformat: "Jahr, Zahl"
# und erweitere liste.csv mit: id, bezeichnung, jahr_min, jahr_max

import glob, os
import pandas as pd
import numpy as np

# importiere Konfigurationsparameter
import config



# functions
# read csv
def readcsv(file):
    return pd.read_csv(file, **config.csv_args_r)

def check_df_for_destatis(df):
    is_ok = True
    #bezeichnung_columns
    is_ok = is_ok and select_bez_columns(df).size>0
    #Zeit_Label=Jahr
    is_ok = is_ok and df['Zeit_Label'].iloc[0] =='Jahr'
    #anzahl_columns
    is_ok = is_ok and select_anzahl_columns(df).size>0
    return is_ok

#select columns to concat for Bezeichnung
def select_bez_columns(df):
    columns = pd.Index([])
    if 'Statistik_Label' in df.columns:
        columns = columns.append(pd.Index(['Statistik_Label']))
    columns = columns.append(df.filter(regex='Auspraegung_Label', axis=1).columns)
    return columns

def select_anzahl_columns(df):
    columns = pd.Index([])
    columns = columns.append(df.filter(regex='Anzahl', axis=1).columns)
    return columns

def strip_anzahl_column(colstring):
    parts=colstring.split('_')
    while('' in parts) :
        parts.remove('')
    return '_'.join(parts[2:])


# Listenframe
if os.path.isfile(config.listenpath): 
    liste = readcsv(config.listenpath)
else:
    liste = pd.DataFrame(columns=['id', 'bezeichnung', 'anzahlbez','jahr_min', 'jahr_max','quelle','quelle_id'])

# Get CSV files list from a folder
csv_files = glob.glob(config.sourcepath + "/*.csv")

# Read each CSV file into DataFrame
# This creates a list of dataframes
df_list = (readcsv(file) for file in csv_files)

number = max(0,liste['id'].max()+1)

for index, df in enumerate(df_list):
    #check for right content
    if check_df_for_destatis(df):
        #get anzahl columnd
        anzahl_cols = select_anzahl_columns(df)
        quelle = csv_files[index].replace('.csv','').replace(config.sourcepath,'').replace('/','').replace('\\','').replace('_flat','')
        #create bez new column
        df['bezeichnung'] = df[select_bez_columns(df)].T.agg('_'.join)
        # split based on column
        gb = df.groupby('bezeichnung')    
        sub_df_list = [gb.get_group(x) for x in gb.groups]
        for sub_df in sub_df_list:
            for anzahl_col in anzahl_cols:
                save_df = sub_df[['Zeit',anzahl_col]].rename(columns={'Zeit':'jahr',anzahl_col:'anzahl'})
                #clean anzahl column
                save_df['anzahl'] = save_df['anzahl'].replace('.',np.nan)
                save_df.to_csv(config.targetpath + "/" + str(number) + ".csv", **config.csv_args_w)
                liste.loc[len(liste.index)] = [number, sub_df['bezeichnung'].iloc[0], strip_anzahl_column(anzahl_col), save_df['jahr'].min(), save_df['jahr'].max(),'DESTATIS',quelle]
                print('Saved file number:', number)
                number += 1


#save liste
liste.to_csv(config.listenpath, **config.csv_args_w)