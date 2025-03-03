import csv
from matplotlib import pyplot as plt
from typing import final
from xmlrpc.client import DateTime
from pprint import pprint
import pandas as pd
import numpy as np
import os
if __name__ == "__main__":
    from CSV_cleaning import create_dataframe

    #creation of a dataframe called final_file with only the first 700 rows
    final_file = create_dataframe("TSLA_modified.csv").head(701)



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

    # convertiamo l'ADTV_std iun interi
    final_file['ADTV_std'] = final_file['ADTV_std'].astype(int)

    # Visualizza il DataFrame con le nuove colonne
    print(final_file[["Date","Open","High","Low","Close","Adj Close","Volume",'ADTV', 'ADTV_std']])

    # Plot results on a single plot and fill the area between the ADTV and its standard deviation (i.e. ADTV Std) with
    # the fill_between() function.

    fig, ax = plt.subplots()
    # ax.set_aspect(1)
    ax.plot(final_file['Date'], final_file['ADTV'], label='ADTV')
    ax.set_xlim([final_file['Date'].min(), final_file['Date'].max()])
    ax.set_title('TSLA Stock average statistics')
    ax.set_xlabel('Date')
    ax.set_ylabel('average')
    ax.fill_between(final_file['Date'], final_file['ADTV'] - final_file['ADTV_std'], final_file['ADTV'] + final_file['ADTV_std'], color="red", alpha=0.2, label="±1 Std Dev")
    ax.legend()
    ax.grid(True)
    plt.show()

    # cartella_destinazione = '/Users/edoardolucca/Documents/GitHub/ProjectTesla2/Sito_web'  # Sostituisci con il percorso desiderato
    # nome_file = 'grafico.png'
    # percorso_completo = os.path.join('Sito_web',nome_file)
    # 
    # # Verifica se la cartella esiste, altrimenti la crea
    # 
    # 
    # # Salva il grafico come immagine PNG nella cartella
    # fig.savefig('/Users/edoardolucca/Documents/GitHub/ProjectTesla2/Sito_web')
    # 
    # # Mostra un messaggio di conferma
    # 