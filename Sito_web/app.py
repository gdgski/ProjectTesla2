from flask import Flask, render_template, send_file , request, flash,jsonify, redirect, url_for, send_from_directory
import mysql
from joblib.parallel import method
from mysql.connector import Error
import pymysql
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import csv
import os

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
def esegui_query_parametrizzata(query, parametri):
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
            cursor.execute(query, parametri)
            connection.commit()
            cursor.close()
            print(f"Query eseguita con successo: {query}")
    except Error as e:
        print(f"Errore durante l'esecuzione della query: {e}")
        return None
    finally:
        if connection.is_connected():
            connection.close()

# Webapp creation

app = Flask(__name__)
app.secret_key = 'chiave_segreta_per_flash' # Necessaria per usare flash

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/visualizza")
def visualizza_dati():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="ProjectTesla"
    )
    cursor = connection.cursor(dictionary=True)

    q = """SELECT * From dati"""

    cursor.execute(q)
    risultato = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template("visualizza_dati.html",lista_tesla = risultato)

@app.route("/modelli")
def modelli():
    return render_template("modelli.html")

@app.route("/contatti")
def contatti():
    return render_template("contatti.html")

@app.route("/tecnologia")
def tecnologia():
    return render_template("tecnologia.html")

@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

@app.route("/inserisci_dati")
def inserisci_dati():
    return render_template("inserisci_dati.html")

@app.route("/inserisci_nuovi_dati",methods=['POST'])
def inserisci_nuovi_dati():

    date = request.form.get('date')
    high = request.form.get('high')
    open = request.form.get('open')
    volume = request.form.get('volume')
    adj_close = request.form.get('adj_close')
    close = request.form.get('close')
    low = request.form.get('low')

    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="ProjectTesla"
    )
    cursor = connection.cursor(dictionary=True)

    q = """INSERT INTO dati_iniziali (date,open,high,low,close,adj_close,volume) Values (%s,%s,%s,%s,%s,%s,%s)"""
    valori = (date,open,high,low,close,adj_close,volume)
    esegui_query_parametrizzata(q,valori)


    cursor.close()
    connection.close()

    flash("Dati inseriti con successo")

    return redirect(url_for("inserisci_dati"))

@app.route("/graficiinterattivi")
def graficiinterattivi():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="ProjectTesla"
    )
    cursor = connection.cursor(dictionary=True)

    q = """SELECT * From dati"""

    cursor.execute(q)
    risultato = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template("graficiinterattivi.html", lista_tesla=risultato)

@app.route("/formattazione_dati")
def formattazione_dati():


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
        dataframe.loc[:days-1, f'ADTV_{days}'] = dataframe.loc[:days-1, column]

        # Convert ADTV to integers
        dataframe[f'ADTV_{days}'] = dataframe[f'ADTV_{days}'].astype(int)
        return dataframe

    def ADTV_DAYS_std(dataframe, column, days):
        # Calculate the standard deviation of ADTV over a 5-day window
        dataframe[f'ADTV_{days}_std'] = dataframe[column].rolling(window=days, min_periods=1).std()

        # Fill the first 4 values of ADTV_std with 0
        dataframe.loc[:days-1, f'ADTV_{days}_std'] = dataframe.loc[:days-1, column]

        # Convert ADTV_std to integers
        dataframe[f'ADTV_{days}_std'] = dataframe[f'ADTV_{days}_std'].astype(int)

        return dataframe

    def calculate_mfm(df, high_col="high", low_col="low", close_col="close"):
        return ((df[close_col] - df[low_col]) - (df[high_col] - df[close_col])) / (df[high_col] - df[low_col])

    final_file = create_dataframe_from_db()
    # Elaborate the ADTV over a period time of 5 days
    final_file['ADTV'] = final_file['volume'].rolling(window=5, min_periods=1).mean()
    # fill the first 4 value with the volume of the day itself
    final_file['ADTV'].iloc[:4] = final_file['volume'].iloc[:4]
    final_file['ADTV'] = final_file['ADTV'].astype(int)
    final_file['ADTV_std'] = final_file['ADTV'].rolling(window=5, min_periods=1).std()
    final_file['ADTV_std'].iloc[:4] = 0
    final_file['ADTV_std'] = final_file['ADTV_std'].astype(int)
    final_file['MFM'] = calculate_mfm(final_file)
    final_file["MFV"] = final_file['MFM'] * final_file["volume"]
    final_file["CMF"] = final_file["MFV"].rolling(21).sum() / final_file["volume"].rolling(21).sum()
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
         "ADTV_10", "ADTV_10_std", "ADTV_20", "ADTV_20_std", "ADTV_50", "ADTV_50_std", "MFM", "CMF"]])


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



    return redirect(url_for("visualizza_dati"))

@app.route("/elimina_dati")
def elimina_dati():
    return render_template("elimina_dati.html")

@app.route("/elimina_back_dati",methods=['POST'])
def elimina_back_dati():

    date = request.form.get('date')
    q = f"""DELETE FROM dati_iniziali WHERE date = '{date}'"""
    q2 = f"""DELETE FROM dati WHERE date = '{date}'"""

    esegui_query(q)
    esegui_query(q2)

    flash("Dati eliminati con successo")
    return redirect(url_for("elimina_dati"))

@app.route("/modifica_dati")
def modifica_dati():
    return render_template("modifica_dati.html")

@app.route("/modifica_dati_back",methods=['POST'])
def modifica_dati_back():

    date = request.form.get('date')
    high = request.form.get('high')
    open = request.form.get('open')
    volume = request.form.get('volume')
    adj_close = request.form.get('adj_close')
    close = request.form.get('close')
    low = request.form.get('low')

    if open != "":

        q = f"""UPDATE dati SET open = '{open}' WHERE date = '{date}'"""
        esegui_query(q)

    if high != "":
        q = f"""UPDATE dati SET high = '{high}' WHERE date = '{date}'"""
        esegui_query(q)

    if volume != "":
        q = f"""UPDATE dati SET volume = '{volume}' WHERE date = '{date}'"""
        esegui_query(q)

    if adj_close != "":
        q = f"""UPDATE dati SET adj_close = '{adj_close}' WHERE date = '{date}'"""
        esegui_query(q)

    if close != "":
        q = f"""UPDATE dati SET close = '{close}' WHERE date = '{date}'"""
        esegui_query(q)

    if low != "":
        q = f"""UPDATE dati SET low = '{low}' WHERE date = '{date}'"""
        esegui_query(q)




    flash("Dati modifica con successo")
    return redirect(url_for("modifica_dati"))

# Define the directory where the CSV file will be saved

DOWNLOAD_FOLDER = os.path.join(os.getcwd(), "static")
app.config["DOWNLOAD_FOLDER"] = DOWNLOAD_FOLDER

@app.route("/download")
def download_file():
    # Connect to the database
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="ProjectTesla"
    )
    cursor = connection.cursor(dictionary=True)

    # Query to fetch data
    query = """SELECT * FROM dati"""
    cursor.execute(query)
    data = cursor.fetchall()

    cursor.close()
    connection.close()

    # Convert data to a Pandas DataFrame
    df = pd.DataFrame(data)

    # Define the full file path inside the static folder
    filename = "data.csv"
    file_path = os.path.join(app.config["DOWNLOAD_FOLDER"], filename)

    # Save DataFrame to CSV inside the static folder
    df.to_csv(file_path, index=False, encoding="utf-8")

    # Send the file to the user
    return send_from_directory(app.config["DOWNLOAD_FOLDER"], filename, as_attachment=True)

@app.route('/get_data')
def get_data():
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')

    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="ProjectTesla"
    )
    cursor = connection.cursor(dictionary=True)

    # Query to fetch data
    query = """SELECT * FROM dati"""
    cursor.execute(query)
    data = cursor.fetchall()

    cursor.close()
    connection.close()

    # Convert data to a Pandas DataFrame
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])

    filtered_df = df
    if start_date and end_date:
        filtered_df = filtered_df[(filtered_df['date'] >= start_date) & (filtered_df['date'] <= end_date)]

    return jsonify(filtered_df.to_dict(orient="records"))


@app.route('/calcola_rendimento',methods=['POST'])
def calcola_rendimento():
    # Ottieni le date dai parametri della richiesta
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="ProjectTesla"
    )
    cursor = connection.cursor(dictionary=True)

    # Query per ottenere il prezzo di apertura
    cursor.execute("SELECT open FROM dati WHERE date = %s", (start_date,))
    open_price = cursor.fetchone()

    # Query per ottenere il prezzo di chiusura
    cursor.execute("SELECT close FROM dati WHERE date = %s", (end_date,))
    close_price = cursor.fetchone()


    cursor.close()
    connection.close()

    # Controllo se i dati esistono
    if not open_price or not close_price:
        return jsonify({"error": "Dati non trovati per le date fornite"}), 404

    # Calcolo del rendimento

    rendimento = ((close_price['close'] - open_price['open']) / open_price['open']) * 100


    return jsonify({"rendimento": round(rendimento, 2)})



if __name__ == "__main__":
    app.run(debug=True)