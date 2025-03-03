from flask import Flask, render_template, send_file
import mysql
from mysql.connector import Error


# Webapp creation

app = Flask(__name__)

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



if __name__ == "__main__":
    app.run(debug=True)