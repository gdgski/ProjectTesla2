import mysql.connector
from mysql.connector import Error
import csv

def create_tables():
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
            sql = """
                CREATE TABLE IF NOT EXISTS dati(
                    date DATE PRIMARY KEY,
                    open FLOAT(10),
                    high FLOAT(10),
                    low FLOAT(10),
                    close FLOAT(10),
                    adj_close FLOAT(10),
                    volume FLOAT(10),
                    ADTV_2 FLOAT(10), 
                    ADTV_2_std FLOAT(10), 
                    ADTV_5 FLOAT(10), 
                    ADTV_5_std FLOAT(10), 
                    ADTV_10 FLOAT(10), 
                    ADTV_10_std FLOAT(10), 
                    ADTV_20 FLOAT(10), 
                    ADTV_20_std FLOAT(10), 
                    ADTV_50 FLOAT(10), 
                    ADTV_50_std FLOAT(10)
                );
            """
            # Esecuzione della query
            cursor.execute(sql)

            cursor.close()
            print("Creazione tabelle avvenuta!")
    except Error as e:
        print(f"Errore durante l'esecuzione della query: {e}")
    finally:
        if connection.is_connected():
            connection.close()

create_tables()
