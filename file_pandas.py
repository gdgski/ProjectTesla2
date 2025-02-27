import csv
from xmlrpc.client import DateTime
from pprint import pprint
import pandas as pd
import numpy as np

# Create a dictionary to then create a dataframe
with open('TSLA_modified.csv',"r", encoding='utf-8') as f:
    lettore = csv.reader(f, delimiter=',')
    f.readline()
    price_data = []
    for riga in lettore:
        price_data.append(riga)
# Creation of the dataframe
dataframe_prices = pd.DataFrame(price_data, columns=["Date","Open","High","Low","Close","Adj Close","Volume"])
dataframe_prices.replace("", np.nan, inplace=True)
#changing the type of datas
dataframe_prices['Date'] = pd.to_datetime(dataframe_prices['Date'])
dataframe_prices['Open'] = dataframe_prices['Open'].astype(float)
dataframe_prices['Close'] = dataframe_prices['Close'].astype(float)
dataframe_prices['Low'] = dataframe_prices['Low'].astype(float)
dataframe_prices['High'] = dataframe_prices['High'].astype(float)
dataframe_prices['Adj Close'] = dataframe_prices['Adj Close'].astype(float)
dataframe_prices['Volume'] = dataframe_prices['Volume'].astype(float)

#drop the NaNs from the dataframe
df_cleared = dataframe_prices.dropna(axis = 0, subset = ["Date","Open","High","Low","Close","Adj Close","Volume"])

#counting the NaNs after clearing
total_nansx = df_cleared.isna().sum().sum()
# print(total_nansx)
df_cleaned = df_cleared.dropna().reset_index(drop=True)
print(df_cleaned)

# Load the first 700 rows of the CSV file
# print(df_cleaned, nrows=700)