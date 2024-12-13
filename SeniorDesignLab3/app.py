import os
import sqlite3
from flask import Flask, render_template, request, jsonify, current_app, g, redirect, url_for, flash, session
from flask.cli import with_appcontext
import click
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from SeniorDesignLab3 import init_app, get_db



instance_path = os.path.join(os.getcwd(), 'instance')

if not os.path.exists(instance_path):
    os.makedirs(instance_path)

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['DATABASE'] = os.path.join('instance', 'flaskr.sqlite')

init_app(app)  # Call this to register commands and teardown logic




@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Retrieve form data
        username = request.form.get('username')
        password = request.form.get('password')

        db = get_db()
        user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()

        if user and check_password_hash(user['password'], password):
            # Store user info in session
            session['logged_in'] = True
            session['username'] = user['username']
            flash('Login successful!', 'success')
            return redirect(url_for('protected'))
        else:
            flash('Invalid username or password', 'error')
            return redirect(url_for('login'))

    # If GET request, just show the login form
    return render_template('login.html')


@app.route('/logout')
def logout():
    # Clear session data
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/protected')
def protected():
    if not session.get('logged_in'):
        flash('You must be logged in to access this page.', 'error')
        return redirect(url_for('login'))
    return render_template('protected.html', username=session.get('username'))


@app.route('/team_member/<name>')
def team_member(name):
    valid_names = ['nick', 'alex', 'michael', 'robby']
    name = name.lower()
    if name in valid_names:
        return render_template(f'{name}.html', name=name.capitalize())
    else:
        return render_template('404.html'), 404


@app.route('/contact/<name>', methods=['POST'])
def contact(name):
    message = request.form.get('message')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(f'protected/messages/{name}_{timestamp}.html', 'w') as f:
        f.write(f'<p>{message}</p><p>Timestamp: {timestamp}</p>')
    flash('Message sent successfully!', 'success')
    return redirect(url_for('team_member', name=name))


@app.route('/nick-embedded-systems')
def nick_embedded_systems():
    return render_template('nicksPages/nick-embedded-systems.html')

@app.route('/nick-senior-design')
def nick_senior_design():
    return render_template('nicksPages/nick-senior-design.html')

@app.route('/nick-iec')
def nick_iec():
    return render_template('nicksPages/nick-iec.html')

if __name__ == '__main__':
    app.run(debug=True)


