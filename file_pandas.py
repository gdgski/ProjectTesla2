import csv
from matplotlib import pyplot as plt
from typing import final
from xmlrpc.client import DateTime
from pprint import pprint
import pandas as pd
import numpy as np

if __name__ == "__main__":
    from CSV_cleaning import create_dataframe

    #creation of a dataframe called final_file with only the first 700 rows
    final_file = create_dataframe("TSLA_modified.csv").head(701)
    print(final_file)

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
    ax.set_xlim([final_file['Date'].min(), final_file['Date'].max()])
    ax.set_title('TSLA Stock Prices')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    ax.legend()
    ax.grid(True)
    plt.show()