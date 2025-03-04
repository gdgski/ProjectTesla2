import csv
import mysql.connector
from mysql.connector import Error
import csv


def insert_csv_to_db(csv_file):
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

            # Lettura del CSV e inserimento dei dati nella tabella
            with open('../Pandas/ADTV_TSLA.csv', 'r') as file:
                csv_reader = csv.reader(file)

                # Salta la riga di intestazione (se presente)
                next(csv_reader)

                for row in csv_reader:
                    # Inserisci i dati nella tabella
                    sql = """
                        INSERT INTO dati (date, open, high, low, close, adj_close, volume, ADTV_2, ADTV_2_std, ADTV_5, ADTV_5_std, ADTV_10, ADTV_10_std, ADTV_20, ADTV_20_std, ADTV_50, ADTV_50_std)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(sql, row)

            # Commit per salvare i cambiamenti
            connection.commit()
            print(f"Dati dal file {csv_file} inseriti correttamente nella tabella 'dati'.")

    except Error as e:
        print(f"Errore durante l'inserimento dei dati: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


# Chiamata alla funzione con il nome del CSV
insert_csv_to_db("../Pandas/updated_data.csv")
