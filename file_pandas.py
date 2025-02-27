import csv
from matplotlib import pyplot as plt
from typing import final
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
# print(df_cleaned)

#creation of a dataframe called final_file with only the first 700 rows
final_file = df_cleaned.head(701)
# print(final_file)

#FIRST REQUEST
# Check if for all rows the following statements are true:
#creation of a def to check if the statement condition is True
def verifica(condition):
    if not condition.all():
        print("valore errato")
    else:
        print("okey")
    # The High value is greater than or equal to both the Open and the Close values.
# The High value is greater than or equal to both the Open and the Close values.
condition1 = (final_file['High'] >= final_file['Open']) & (final_file['High'] >= final_file['Close'])
verifica(condition1)
# # The Low value is less than or equal to both the Open and the Close values
condition2 = (final_file['Low'] <= final_file['Open']) & (final_file['Low'] <= final_file['Close'])
verifica(condition2)
 # The Adj Close values is less than or equal to the Close value
condition3 = (final_file['Adj Close'] <= final_file['Close'])
verifica(condition3)
#aggiungere una riga e testare
#su colab presentarlo in maniera più leggibile

#use this command to obtain a dataframe including the mean,min ,max,standard deviation and first,second,third quartile
print(final_file.describe())



# Plotting
fig, ax = plt.subplots()
# ax.set_aspect(1)
ax.plot(final_file['Date'], final_file['Open'], label='Open')
ax.plot(final_file['Date'], final_file['High'], label='High')
ax.plot(final_file['Date'], final_file['Low'], label='Low')
ax.plot(final_file['Date'], final_file['Close'], label='Close')
ax.plot(final_file['Date'], final_file['Adj Close'], label='Adj Close')
ax.set_xlim()
ax.set_title('TSLA Stock Prices')
ax.set_xlabel('Date')
ax.set_ylabel('Price')
ax.legend()
ax.grid(True)
plt.show()