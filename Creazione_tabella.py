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
                    date YEAR PRIMARY KEY,
                    open FLOAT(10),
                    high FLOAT(10),
                    low FLOAT(10),
                    close FLOAT(10),
                    adj_close FLOAT(10),
                    volume FLOAT(10)
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
