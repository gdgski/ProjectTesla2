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

    #Inspect how the ADTV and ADTV Std change if gotten from a 2,5,10,20 and 50 days average.
    # Convert the values to int.

    def ADTV_DAYS(dataframe, column, days):
        # Controlla se la colonna esiste
        # Calcola la media mobile
        dataframe[f'ADTV_{days}'] = dataframe[column].rolling(window=days, min_periods=1).mean()

        # Riempiamo i primi 4 valori di ADTV con il valore della colonna originale
        dataframe.loc[:4, f'ADTV_{days}'] = dataframe.loc[:4, column]

        # Converti l'ADTV in interi
        dataframe[f'ADTV_{days}'] = dataframe[f'ADTV_{days}'].astype(int)
        return dataframe

    def ADTV_DAYS_std(dataframe, column, days):
        # Calcola la deviazione standard dell'ADTV su una finestra di 5 giorni
        dataframe[f'ADTV_{days}_std'] = dataframe[column].rolling(window=days, min_periods=1).std()

        # Riempiamo i primi 4 valori di ADTV_std con 0 (non ci sono abbastanza dati per calcolare la deviazione standard)
        dataframe.loc[:4, f'ADTV_{days}_std'] = dataframe.loc[:4, column]

        # convertiamo l'ADTV_std iun interi
        dataframe[f'ADTV_{days}_std'] = dataframe[f'ADTV_{days}_std'].astype(int)

        return dataframe


    result = ADTV_DAYS(final_file, "Volume", 2)
    result = ADTV_DAYS(final_file, "Volume", 5)
    # result = ADTV_DAYS_std(result, "Volume", 10)
    result = ADTV_DAYS(final_file, "Volume", 10)
    result = ADTV_DAYS(final_file, "Volume", 20)
    result = ADTV_DAYS(final_file, "Volume", 50)
    print(result)




    # Plotting
    fig, ax = plt.subplots()
    # ax.set_aspect(1)
    ax.plot(result['Date'], result['ADTV_2'], label='ADTV_2')
    ax.plot(result['Date'], result['ADTV_5'], label='ADTV_5')
    ax.plot(result['Date'], result['ADTV_10'], label='ADTV_10')
    ax.plot(result['Date'], result['ADTV_20'], label='ADTV_20')
    ax.plot(result['Date'], result['ADTV_50'], label='ADTV_50')

    # ax.plot(final_file['Date'], final_file['Low'], label='Low')
    # ax.plot(final_file['Date'], final_file['Close'], label='Close')
    # ax.plot(final_file['Date'], final_file['Adj Close'], label='Adj Close')
    ax.set_xlim([final_file['Date'].min(), final_file['Date'].max()])
    ax.set_title('TSLA Stock ADTV')
    ax.set_xlabel('Date')
    ax.set_ylabel('ADTV')
    ax.legend()
    ax.grid(True)
    plt.show()

