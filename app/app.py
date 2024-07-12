from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# Sample user data
users = {"user": "password"}

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    if username in users and users[username] == password:
        return "Welcome, {username}!"
    else:
        return "Invalid credentials. Please try again."

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

