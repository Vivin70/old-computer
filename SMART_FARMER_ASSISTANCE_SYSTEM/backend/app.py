'''from flask import Flask, render_template, request, redirect, session
from database import get_db_connection
import pickle
from ml.schemes import get_schemes
from flask import Flask, request, jsonify, render_template
from ml.chatbot_ml import chatbot_response

@app.route("/chatbot", methods=["POST"])
def chatbot():
    data = request.json
    message = data["message"]
    lang = data["lang"]
    reply = chatbot_response(message, lang)
    return jsonify({"reply": reply})




app = Flask(__name__)
app.secret_key = "smart_farmer_secret"

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO users (name,email,password) VALUES (%s,%s,%s)",
            (name,email,password)
        )
        db.commit()
        return redirect('/login')

    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM users WHERE email=%s AND password=%s",
            (email,password)
        )
        user = cursor.fetchone()

        if user:
            session['user'] = user
            if user['role'] == 'admin':
                return redirect('/admin')
            else:
                return redirect('/index')

    return render_template('login.html')

@app.route('/index')
def index():
    if 'user' in session:
        return render_template('index.html')
    return redirect('/login')

@app.route('/admin')
def admin():
    if 'user' in session and session['user']['role'] == 'admin':
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        return render_template('admin.html', users=users)
    return redirect('/login')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/weather', methods=['GET', 'POST'])
def weather():
    prediction = None
    if request.method == 'POST':
        temp = float(request.form['temperature'])
        humidity = float(request.form['humidity'])

        model = pickle.load(open('backend/ml/weather_model.pkl', 'rb'))
        result = model.predict([[temp, humidity]])

        prediction = "Rain Expected 🌧" if result[0] == 1 else "No Rain ☀"

    return render_template('weather.html', prediction=prediction)

@app.route('/contract', methods=['GET','POST'])
def contract():
    prediction = None
    decision = None

    if request.method == 'POST':
        crop = int(request.form['crop'])
        quantity = float(request.form['quantity'])
        market_price = float(request.form['market_price'])

        model = pickle.load(open('backend/ml/contract_model.pkl', 'rb'))
        predicted_price = model.predict([[crop, quantity, market_price]])[0]

        prediction = round(predicted_price, 2)

        expected_market_value = quantity * market_price

        if predicted_price > expected_market_value:
            decision = "✅ Good Contract (Profitable)"
        else:
            decision = "❌ Bad Contract (Not Profitable)"

    return render_template(
        'contract.html',
        prediction=prediction,
        decision=decision
    )

@app.route("/chatbot", methods=["POST"])
def chatbot():
    data = request.json
    message = data["message"]
    lang = data["lang"]
    reply = chatbot_response(message, lang)
    return jsonify({"reply": reply})
@app.route('/schemes')
def schemes():
    schemes = get_schemes()
    return render_template('schemes.html', schemes=schemes)

@app.route('/admin/delete/<int:user_id>')
def delete_user(user_id):
    if 'user' in session and session['user']['role'] == 'admin':
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))
        db.commit()
        return redirect('/admin')
    return redirect('/login')
@app.route('/admin/update', methods=['POST'])
def update_user():
    if 'user' in session and session['user']['role'] == 'admin':
        user_id = request.form['id']
        role = request.form['role']

        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute(
            "UPDATE users SET role=%s WHERE id=%s",
            (role, user_id)
        )
        db.commit()
        return redirect('/admin')
    return redirect('/login')


if __name__ == '__main__':
    app.run(debug=True)
'''
from flask import Flask, render_template, request, redirect, session, jsonify
from database import get_db_connection
import pickle
from ml.schemes import get_schemes
from ml.chatbot_ml import chatbot_response
import os

# ================= FLASK APP =================
app = Flask(__name__)
app.secret_key = "smart_farmer_secret"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ================= HOME =================
@app.route('/')
def home():
    return render_template('home.html')

# ================= REGISTER =================
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO users (name,email,password,role) VALUES (%s,%s,%s,'farmer')",
            (name, email, password)
        )
        db.commit()
        cursor.close()
        db.close()

        return redirect('/login')

    return render_template('register.html')

# ================= LOGIN =================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM users WHERE email=%s AND password=%s",
            (email, password)
        )
        user = cursor.fetchone()
        cursor.close()
        db.close()

        if user:
            session['user'] = user
            if user['role'] == 'admin':
                return redirect('/admin')
            else:
                return redirect('/index')

        return "Invalid credentials"

    return render_template('login.html')

# ================= FARMER DASHBOARD =================
@app.route('/index')
def index():
    if 'user' in session:
        return render_template('index.html')
    return redirect('/login')

# ================= ADMIN DASHBOARD =================
@app.route('/admin')
def admin():
    if 'user' in session and session['user']['role'] == 'admin':
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        cursor.close()
        db.close()
        return render_template('admin.html', users=users)
    return redirect('/login')

# ================= WEATHER PREDICTION =================
@app.route('/weather', methods=['GET', 'POST'])
def weather():
    prediction = None

    if request.method == 'POST':
        temp = float(request.form['temperature'])
        humidity = float(request.form['humidity'])

        model_path = os.path.join(BASE_DIR, 'ml', 'weather_model.pkl')
        model = pickle.load(open(model_path, 'rb'))
        result = model.predict([[temp, humidity]])

        prediction = "Rain Expected 🌧" if result[0] == 1 else "No Rain ☀"

    return render_template('weather.html', prediction=prediction)

# ================= CONTRACT PREDICTOR =================
@app.route('/contract', methods=['GET', 'POST'])
def contract():
    prediction = None
    decision = None

    if request.method == 'POST':
        crop = int(request.form['crop'])
        quantity = float(request.form['quantity'])
        market_price = float(request.form['market_price'])

        model_path = os.path.join(BASE_DIR, 'ml', 'contract_model.pkl')
        model = pickle.load(open(model_path, 'rb'))
        predicted_price = model.predict([[crop, quantity, market_price]])[0]

        prediction = round(predicted_price, 2)
        expected_market_value = quantity * market_price

        if predicted_price > expected_market_value:
            decision = "✅ Good Contract (Profitable)"
        else:
            decision = "❌ Bad Contract (Not Profitable)"

    return render_template(
        'contract.html',
        prediction=prediction,
        decision=decision
    )

# ================= CHATBOT API =================
@app.route("/chatbot", methods=["POST"])
def chatbot():
    data = request.get_json()
    message = data.get("message", "")
    lang = data.get("lang", "en")

    reply = chatbot_response(message, lang)
    return jsonify({"reply": reply})

# ================= GOVERNMENT SCHEMES =================
@app.route('/schemes')
def schemes():
    schemes_data = get_schemes()
    return render_template('schemes.html', schemes=schemes_data)

# ================= ADMIN DELETE USER =================
@app.route('/admin/delete/<int:user_id>')
def delete_user(user_id):
    if 'user' in session and session['user']['role'] == 'admin':
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))
        db.commit()
        cursor.close()
        db.close()
        return redirect('/admin')
    return redirect('/login')

# ================= ADMIN UPDATE USER =================
@app.route('/admin/update', methods=['POST'])
def update_user():
    if 'user' in session and session['user']['role'] == 'admin':
        user_id = request.form['id']
        role = request.form['role']

        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute(
            "UPDATE users SET role=%s WHERE id=%s",
            (role, user_id)
        )
        db.commit()
        cursor.close()
        db.close()
        return redirect('/admin')
    return redirect('/login')

# ================= LOGOUT =================
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# ================= RUN =================
if __name__ == '__main__':
    app.run(debug=True)
