from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import requests


app = Flask(__name__)

app.secret_key = 'Your secret key here'

app.config['MYSQL_HOST'] = 'Your host here'
app.config['MYSQL_USER'] = 'Your user here'
app.config['MYSQL_PASSWORD'] = 'Your password here'
app.config['MYSQL_DB'] = 'Your DB here'

mysql = MySQL(app)

def retrieve_weather():
    url = "https://api.weather.gov/points/42.988979,-78.163874"
    response = requests.get(url)
    if response.status_code != 200:
        return None, None
    data = response.json()
    forecast_url = data["properties"]["forecast"]
    city = data["properties"]["relativeLocation"]["properties"]["city"]
    state = data['properties']['relativeLocation']['properties']['state']
    location = f"{city}, {state}"
    return forecast_url, location

@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            msg = 'Logged in successfully !'
            return render_template('index.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and  'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s)', (username, password, email, ))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)
@app.route('/Home')
def home():
    return render_template('home.html')

@app.route('/weather', methods =['GET', 'POST'])
def weather():
    forecast_url, location = retrieve_weather()
    
    forecast = None
    periods = None
    if forecast_url is not None:
        response = requests.get(forecast_url)
        if response.status_code == 200:
            forecast = response.json()
            periods = forecast["properties"]["periods"]
    return render_template('weather.html', forecast_url=forecast_url, location=location, periods=periods)


