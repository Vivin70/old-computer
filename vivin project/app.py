'''from flask import Flask, render_template, request, redirect, session
from db import get_db
import csv, os

app = Flask(__name__)
app.secret_key = "smartfarmers"

@app.route('/')
def login():
    return render_template("login.html")

@app.route('/login', methods=['POST'])
def do_login():
    email = request.form['email']
    password = request.form['password']

    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM users WHERE email=%s AND password=%s",
                (email,password))
    user = cur.fetchone()

    if user:
        session['user'] = user
        if user['role'] == 'admin':
            return redirect('/admin')
        else:
            return redirect('/farmer')
    return "Invalid login"

@app.route('/register')
def register():
    return render_template("register_chat.html")

@app.route('/save_user', methods=['POST'])
def save_user():
    data = request.json
    db = get_db()
    cur = db.cursor()
    cur.execute("""
        INSERT INTO users(name,dob,email,password,role)
        VALUES(%s,%s,%s,%s,'farmer')
    """,(data['name'],data['dob'],data['email'],data['password']))
    db.commit()
    return {"status":"success"}

@app.route('/admin')
def admin():
    return render_template("admin_dashboard.html")

@app.route('/farmer')
def farmer():
    return render_template("farmer_dashboard.html")

# WEATHER (CSV)
@app.route('/weather')
def weather():
    with open('data/weather.csv') as f:
        reader = csv.reader(f)
        rows = list(reader)
    return render_template("iframe_weather.html", rows=rows)

# DISEASE (DUMMY)
@app.route('/disease', methods=['POST'])
def disease():
    file = request.files['image']
    file.save("static/uploads/"+file.filename)
    return "Predicted Disease: Leaf Blight"

app.run(debug=True)'''


from flask import Flask, render_template, request, redirect, session, jsonify
import mysql.connector
import csv
import os

app = Flask(__name__)
app.secret_key = "smart_farmers_secret"

# ---------------- DATABASE CONNECTION ----------------
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="vivin",
        database="smart_farmers"
    )

# ---------------- LOGIN ----------------
@app.route('/')
def login_page():
    return render_template("login.html")

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute(
        "SELECT * FROM users WHERE email=%s AND password=%s",
        (email, password)
    )
    user = cur.fetchone()

    if user:
        session['user'] = user
        if user['role'] == 'admin':
            return redirect('/admin')
        else:
            return redirect('/farmer')
    else:
        return "Invalid Email or Password"

# ---------------- REGISTER (CHAT STYLE) ----------------
@app.route('/register')
def register():
    return render_template("register_chat.html")

@app.route('/save_user', methods=['POST'])
def save_user():
    data = request.get_json()

    name = data['name']
    dob = data['dob']
    email = data['email']
    password = data['password']

    db = get_db()
    cur = db.cursor()

    cur.execute("""
        INSERT INTO users (name, dob, email, password, role)
        VALUES (%s, %s, %s, %s, 'farmer')
    """, (name, dob, email, password))

    db.commit()
    return jsonify({"status": "success"})

# ---------------- ADMIN MODULE ----------------
@app.route('/admin')
def admin_dashboard():
    return render_template("admin_dashboard.html")

@app.route('/add_contractor', methods=['GET', 'POST'])
def add_contractor():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        experience = request.form['experience']
        area = request.form['area']
        crop = request.form['crop']

        db = get_db()
        cur = db.cursor()
        cur.execute("""
            INSERT INTO contractors
            (name, email, experience, area, crop_specialization)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, email, experience, area, crop))

        db.commit()
        return redirect('/admin')

    return render_template("add_contractor.html")

@app.route('/view_users')
def view_users():
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    return render_template("view_users.html", users=users)

# ---------------- FARMER MODULE ----------------
@app.route('/farmer')
def farmer_dashboard():
    return render_template("farmer_dashboard.html")

# ---------------- WEATHER (CSV BASED) ----------------
@app.route('/weather')
def weather():
    data = []
    with open('data/weather.csv') as file:
        reader = csv.reader(file)
        data = list(reader)
    return render_template("weather.html", data=data)

# ---------------- DISEASE PREDICTION (DUMMY) ----------------
@app.route('/disease', methods=['GET', 'POST'])
def disease():
    result = ""
    if request.method == 'POST':
        image = request.files['image']
        upload_path = os.path.join("static/uploads", image.filename)
        image.save(upload_path)
        result = "Predicted Disease: Leaf Blight"
    return render_template("disease.html", result=result)

# ---------------- CONTRACT MATCH ----------------
@app.route('/contract')
def contract_match():
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM contractors")
    contractors = cur.fetchall()
    return render_template("contract_match.html", contractors=contractors)

# ---------------- CHATBOT ----------------
@app.route('/chatbot')
def chatbot():
    return render_template("chatbot.html")

# ---------------- FARMER PROFILE ----------------
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    user = session.get('user')

    if request.method == 'POST':
        land = request.form['land']
        crop = request.form['crop']

        db = get_db()
        cur = db.cursor()
        cur.execute("""
            REPLACE INTO farmer_profile (farmer_id, land_size, crop)
            VALUES (%s, %s, %s)
        """, (user['user_id'], land, crop))

        db.commit()

    return render_template("profile.html", user=user)

# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)

