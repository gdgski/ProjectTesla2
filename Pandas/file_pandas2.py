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


    # Calcola l'ADTV a 5 giorni
    final_file['ADTV'] = final_file['Volume'].rolling(window=5, min_periods=1).mean()

    # Riempiamo i primi 4 valori di ADTV con il Volume del giorno stesso
    final_file['ADTV'].iloc[:4] = final_file['Volume'].iloc[:4]

    # Converti l'ADTV in interi
    final_file['ADTV'] = final_file['ADTV'].astype(int)

    # Calcola la deviazione standard dell'ADTV su una finestra di 5 giorni
    final_file['ADTV_std'] = final_file['ADTV'].rolling(window=5, min_periods=1).std()

    # Riempiamo i primi 4 valori di ADTV_std con 0 (non ci sono abbastanza dati per calcolare la deviazione standard)
    final_file['ADTV_std'].iloc[:4] = 0

    # Visualizza il DataFrame con le nuove colonne
    print(final_file[['Date', 'Volume', 'ADTV', 'ADTV_std']])