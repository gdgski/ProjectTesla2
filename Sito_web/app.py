from flask import Flask, render_template

app = Flask(__name__)

# sports = ["Calcio", "Basket", "Tennis", "Volley", "Atletica"]


@app.route("/")
def index():
    return render_template("home.html")

@app.route("/visualizza")
def visualizza_dati():
    return render_template("visualizza_dati.html")

@app.route("/visualizza2")
def visualizza_dati2():
    # Lista di dati base in Python
    dati_finanziari = [
        {'date': '2010-07-01', 'open': 9999, 'high': 5.184, 'low': 4.054, 'close': 4.392, 'adj_close': 4.392,
         'volume': 41094000},
        {'date': '2010-07-02', 'open': 4.6, 'high': 4.62, 'low': 3.742, 'close': 3.84, 'adj_close': 3.84,
         'volume': 25699000},
        {'date': '2010-07-06', 'open': 4.0, 'high': 4.0, 'low': 3.166, 'close': 3.222, 'adj_close': 3.222,
         'volume': 34334500},
        {'date': '2010-07-07', 'open': 3.28, 'high': 3.326, 'low': 2.996, 'close': 3.16, 'adj_close': 3.16,
         'volume': 34608500},
        {'date': '2010-07-08', 'open': 3.2, 'high': 3.3, 'low': 3.05, 'close': 3.1, 'adj_close': 3.1,
         'volume': 29987000},
    ]
    return render_template("visualizza_dati2.html",data = dati_finanziari)


if __name__ == "__main__":
    app.run(debug=True)