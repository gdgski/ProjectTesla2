from flask import Flask, render_template, send_file , request, flash, redirect, url_for
import mysql
from joblib.parallel import method
from mysql.connector import Error
import pymysql
import pandas as pd
import numpy as np
from sqlalchemy import create_engine

def formattazione_dati():

    def esegui_query(query):
        try:
            # Creazione connessione
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="ProjectTesla"
            )
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute(query)
                connection.commit()
                cursor.close()
                print(f"Query eseguita con successo: {query}")
        except Error as e:
            print(f"Errore durante l'esecuzione della query: {e}")
            return None
        finally:
            if connection.is_connected():
                connection.close()


    def create_dataframe_from_db():
        # Connessione al database MySQL
        conn = pymysql.connect(host="localhost", user="root", password="", database="ProjectTesla")

        # Query per estrarre i dati
        query = f"SELECT * FROM dati_iniziali"

        # Creazione del DataFrame da MySQL
        dataframe_prices = pd.read_sql(query, conn)


        # Chiudere la connessione
        conn.close()

        # Pulizia e conversione dei dati
        dataframe_prices.replace("", np.nan, inplace=True)
        dataframe_prices['date'] = pd.to_datetime(dataframe_prices['date'])
        dataframe_prices['open'] = dataframe_prices['open'].astype(float)
        dataframe_prices['close'] = dataframe_prices['close'].astype(float)
        dataframe_prices['low'] = dataframe_prices['low'].astype(float)
        dataframe_prices['high'] = dataframe_prices['high'].astype(float)
        dataframe_prices['adj_close'] = dataframe_prices['adj_close'].astype(float)
        dataframe_prices['volume'] = dataframe_prices['volume'].astype(float)

        df_cleaned = dataframe_prices.dropna().reset_index(drop=True)

        # Salvo il DataFrame su un CSV

        return df_cleaned

        print(df.head())

    def ADTV_DAYS(dataframe, column, days):
        # Check if the column exists
        # Calculate the moving average
        dataframe[f'ADTV_{days}'] = dataframe[column].rolling(window=days, min_periods=1).mean()

        # Fill the first 4 values of ADTV with the original column value
        dataframe.loc[:4, f'ADTV_{days}'] = dataframe.loc[:4, column]

        # Convert ADTV to integers
        dataframe[f'ADTV_{days}'] = dataframe[f'ADTV_{days}'].astype(int)
        return dataframe

    def ADTV_DAYS_std(dataframe, column, days):
        # Calculate the standard deviation of ADTV over a 5-day window
        dataframe[f'ADTV_{days}_std'] = dataframe[column].rolling(window=days, min_periods=1).std()

        # Fill the first 4 values of ADTV_std with 0
        dataframe.loc[:4, f'ADTV_{days}_std'] = dataframe.loc[:4, column]

        # Convert ADTV_std to integers
        dataframe[f'ADTV_{days}_std'] = dataframe[f'ADTV_{days}_std'].astype(int)

        return dataframe

    final_file = create_dataframe_from_db()
    # Elaborate the ADTV over a period time of 5 days
    final_file['ADTV'] = final_file['volume'].rolling(window=5, min_periods=1).mean()
    # fill the first 4 value with the volume of the day itself
    final_file['ADTV'].iloc[:4] = final_file['volume'].iloc[:4]
    final_file['ADTV'] = final_file['ADTV'].astype(int)
    final_file['ADTV_std'] = final_file['ADTV'].rolling(window=5, min_periods=1).std()
    final_file['ADTV_std'].iloc[:4] = 0
    final_file['ADTV_std'] = final_file['ADTV_std'].astype(int)
    df = (final_file[["date", "volume"]])
    result = ADTV_DAYS(final_file, "volume", 2)
    result = ADTV_DAYS_std(result, "volume", 2)
    result = ADTV_DAYS(final_file, "volume", 5)
    result = ADTV_DAYS_std(result, "volume", 5)
    result = ADTV_DAYS(final_file, "volume", 10)
    result = ADTV_DAYS_std(result, "volume", 10)
    result = ADTV_DAYS(final_file, "volume", 20)
    result = ADTV_DAYS_std(result, "volume", 20)
    result = ADTV_DAYS(final_file, "volume", 50)
    result = ADTV_DAYS_std(result, "volume", 50)
    result_finale = (final_file[
        ["date", "open", "high", "low", "close", "adj_close", "volume", "ADTV_2", "ADTV_2_std", "ADTV_5", "ADTV_5_std",
         "ADTV_10", "ADTV_10_std", "ADTV_20", "ADTV_20_std", "ADTV_50", "ADTV_50_std"]])


    # Query per estrarre i dati
    query1 = f"DELETE FROM dati"
    esegui_query(query1)

    # Chiudere la connessione


    user = "root"
    password = ""
    host = "localhost"  # Cambia se il database è su un altro server
    database = "ProjectTesla"
    table_name = "dati"

    # Creazione dell'engine di SQLAlchemy
    engine = create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}/{database}")

    # Inserimento del DataFrame nel database MySQL
    result_finale.to_sql(table_name, con=engine, if_exists="append", index=False)

    print("Dati inseriti con successo nel database!")

def download_file():
    def recupera_dati_completi(query):
    # filename = "data.csv"  # Nome del file da scaricare
        query = """SELECT * FROM dati"""
        dati = recupera_dati_completi(query)
        print(dati)
    # return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename, as_attachment=True)

def esegui_query(query):
    try:
        # Creazione connessione
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="ProjectTesla"
        )
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
            cursor.close()
            print(f"Query eseguita con successo: {query}")
    except Error as e:
        print(f"Errore durante l'esecuzione della query: {e}")
        return None
    finally:
        if connection.is_connected():
            connection.close()





