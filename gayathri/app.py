from flask import Flask, render_template, request, redirect, session
import mysql.connector
import pickle
import datetime
import pandas as pd

app = Flask(__name__)
app.secret_key = "eth_secret_key"

# ---------------- LOAD ML MODEL ----------------
model = pickle.load(open("eth_model.pkl", "rb"))

# ---------------- DATABASE CONNECTION ----------------
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="vivin",
    database="eth_db"
)
cursor = db.cursor()

USD_TO_INR = 83  # fixed conversion rate for project

# ---------------- LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        cursor.execute(
            "SELECT * FROM users WHERE username=%s AND password=%s",
            (username, password)
        )
        user = cursor.fetchone()

        if user:
            session["user"] = username
            return redirect("/dashboard")
        else:
            return "Invalid Username or Password"

    return render_template("login.html")

# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        cursor.execute(
            "INSERT INTO users(username,password) VALUES(%s,%s)",
            (username, password)
        )
        db.commit()
        return redirect("/")

    return render_template("register.html")

# ---------------- DASHBOARD ----------------
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user" not in session:
        return redirect("/")

    # Load historical ETH data
    data = pd.read_csv("ethereum.csv")

    dates = data["Date"].tolist()

    # Convert historical prices to INR
    prices_usd = data["Close"].tolist()
    prices_inr = [round(price * USD_TO_INR, 2) for price in prices_usd]

    prediction = None

    if request.method == "POST":
        future_date = request.form["date"]

        date_obj = datetime.datetime.strptime(future_date, "%Y-%m-%d")
        start_date = datetime.datetime(2023, 1, 1)

        days = (date_obj - start_date).days

        predicted_usd = model.predict([[days]])[0]
        prediction = round(predicted_usd * USD_TO_INR, 2)

        # Add predicted value to graph
        dates.append(future_date)
        prices_inr.append(prediction)

    return render_template(
        "dashboard.html",
        dates=dates,
        prices=prices_inr,
        prediction=prediction
    )

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)
