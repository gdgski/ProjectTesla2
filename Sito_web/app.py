from flask import Flask, render_template
import mysql
from mysql.connector import Error

app = Flask(__name__)

# sports = ["Calcio", "Basket", "Tennis", "Volley", "Atletica"]


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




if __name__ == "__main__":
    app.run(debug=True)