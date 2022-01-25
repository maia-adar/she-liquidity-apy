
import pandas as pd
import os
import json
import datefinder
import numpy as np

# Loop through all rewards data files and extract json

directory_name = '/Users/maiaadar/Desktop/Projects/scoreboard/config/plugins/sourcecred/initiatives/initiatives/'
directory = os.fsencode(directory_name)

df = pd.DataFrame()
file_ind = 0

for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if 'liquidity-rewards' not in filename:
        continue

    else:
        test_file = open(directory_name + filename)
        epoch_file = json.load(test_file)

        epoch_name = epoch_file[1]['title']
        dates = list(datefinder.find_dates(epoch_name))
        epoch_start = dates[0]
        epoch_end = dates[1]

        df[str(epoch_end.date())] = 0

        for entry in epoch_file[1]['contributions']['entries']:
            first_contributor = entry['contributors'][0]
            cred_awarded = entry['weight']

            if first_contributor in df.index:
                df.loc[first_contributor, str(epoch_end.date())] = cred_awarded
            else:
                prev = [0] * file_ind
                prev.append(cred_awarded)
                df.loc[first_contributor] = prev
                print('new contributor')

        file_ind = file_ind + 1

df = df.iloc[:, pd.to_datetime(df.columns).argsort()].reset_index()
df = df.set_index('index')
df.index.name = None
df.to_csv('cred_history.csv')








