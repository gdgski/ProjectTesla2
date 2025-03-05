from flask import Flask, render_template, send_file , request, flash, redirect, url_for
import mysql
from joblib.parallel import method
from mysql.connector import Error
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

@app.route("/grafico1")
def grafico1():
    return render_template("grafico1.html")

@app.route("/grafico2")
def grafico2():
    return render_template("grafico2.html")

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
    adj_close = request.form.get('adj close')
    close = request.form.get('close')
    low = request.form.get('low')

    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="ProjectTesla"
    )
    cursor = connection.cursor(dictionary=True)

    q = """INSERT INTO dati (date,open,high,low,close,adj_close,volume) Values (%s,%s,%s,%s,%s,%s,%s)"""

    esegui_query_parametrizzata(q,date,open,high,low,close,adj_close,volume)
    
    cursor.execute(q)
    risultato = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template("visualizza_dati.html", lista_tesla=risultato)
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




if __name__ == "__main__":
    app.run(debug=True)