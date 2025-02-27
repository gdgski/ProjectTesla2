#We will import the CSV
import csv
from xmlrpc.client import DateTime
from pprint import pprint
import json




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
#visual % NaN
def nan_percentage(column: pd.Series) -> float:
 """
 Restituisce la percentuale di NaN per una specifica colonna
 """
 return column.isna().sum() / column.shape[0] * 100


#counting the NaNs
total_nans = dataframe_prices.isna().sum().sum()
print(total_nans)




#drop the NaNs from the dataframe
df_cleared = dataframe_prices.dropna(axis = 0, subset = ["Date","Open","High","Low","Close","Adj Close","Volume"])


#counting the NaNs after clearing
total_nansx = df_cleared.isna().sum().sum()
print(total_nansx)
df_cleaned = df_cleared.dropna().reset_index(drop=True)
print(df_cleaned)


# Salvo il DataFrame 'df_cleaned' su un csv chiamato 'updated_data.csv'
df_cleaned.to_csv(path_or_buf = "updated_data.csv", index = False)




#Creo il file json da esportare in MongoDB


with open('updated_data.csv','r', encoding='utf-8') as f:
   lettore = list(csv.reader(f, delimiter=','))
   chiavi = lettore[0]
   json_da_esportare = []


   for riga in lettore[1:]:
       dizionario = {}
       for i in range(len(chiavi)):
           chiave = chiavi[i]
           valore = riga[i]
           dizionario[chiave] = valore
       json_da_esportare.append(dizionario)


   pprint(json_da_esportare[:5])