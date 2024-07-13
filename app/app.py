from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import yaml
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configure MySQL
db = yaml.load(open('db.yaml'), Loader=yaml.FullLoader)
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM users WHERE username = %s", [username])
    if result > 0:
        user = cur.fetchone()
        if check_password_hash(user[2], password):
            return f"Welcome, {username}!"
        else:
            flash("Invalid credentials. Please try again.", "danger")
    else:
        flash("Invalid credentials. Please try again.", "danger")
    cur.close()
    return redirect(url_for('home'))

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    hashed_password = generate_password_hash(password, method='sha256')

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
    mysql.connection.commit()
    cur.close()

    flash("You have successfully signed up!", "success")
    return redirect(url_for('home'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
