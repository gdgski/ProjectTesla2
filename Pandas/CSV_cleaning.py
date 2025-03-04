#We will import the CSV
import csv
from xmlrpc.client import DateTime
from pprint import pprint
import json
import pandas as pd
import numpy as np


def create_dataframe(file_csv):
# Create a dictionary to then create a dataframe
    with open(f"{file_csv}","r", encoding='utf-8') as f:
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
    df_cleaned = dataframe_prices.dropna().reset_index(drop=True)
    # Salvo il DataFrame 'df_cleaned' su un csv chiamato 'updated_data.csv'
    df_cleaned.to_csv(path_or_buf ="updated_data.csv", index = False)
    return(df_cleaned)

if __name__ == "__main__":
    x = create_dataframe("TSLA_modified.csv")
    print(x)


    # visual % NaN
    def nan_percentage(column: pd.Series) -> float:
      """
      Restituisce la percentuale di NaN per una specifica colonna
      """
      return column.isna().sum() / column.shape[0] * 100




    #counting the NaNs after clearing

    total_nans = x.isna().sum().sum()
    print(total_nans)






#Creo il file json da esportare in MongoDB

def to_json(file_csv):
    with open(f'{file_csv}','r', encoding='utf-8') as f:
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
           return json_da_esportare





