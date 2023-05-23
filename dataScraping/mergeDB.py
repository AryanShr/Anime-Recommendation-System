import pandas as pd
import csv

# Merge the csv files
def merge_csv():
    combined_data = []
    for i in range(1, 6):
        df = pd.read_csv(f'animeDB{i}.csv')
        combined_data.append(df)
    combined_data = pd.concat(combined_data)
    combined_data.to_csv("animeDB.csv", index=False)

merge_csv()