from flask import Flask, render_template

app = Flask(__name__)

# sports = ["Calcio", "Basket", "Tennis", "Volley", "Atletica"]


@app.route("/")
def index():
    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)