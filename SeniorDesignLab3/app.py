import os
import sqlite3
from flask import Flask, render_template, request, jsonify, current_app, g, redirect, url_for, flash, session
from flask.cli import with_appcontext
import click
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Ensure instance folder exists
instance_path = os.path.join(os.getcwd(), 'instance')
print(f"Instance path: {instance_path}")

if not os.path.exists(instance_path):
    os.makedirs(instance_path)

app.config['DATABASE'] = os.path.join(instance_path, 'flaskr.sqlite')


def init_db():
    db = get_db()
    # Make sure you have a `schema.sql` file in a `database` directory
    with app.open_resource('SeniorDesignLab3/Database/schema.sql', mode='r') as f:
        db.executescript(f.read())

    # Insert default user and team members
    default_user = ('defaultUser', generate_password_hash('Fall2024Lab3'))
    team_members = [
        ('team_member1', generate_password_hash('password1')),
        ('team_member2', generate_password_hash('password2')),
        ('team_member3', generate_password_hash('password3')),
        ('team_member4', generate_password_hash('password4'))
    ]

    db.executemany(
        'INSERT OR REPLACE INTO users (username, password) VALUES (?, ?)',
        [default_user] + team_members
    )
    db.commit()


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

app.cli.add_command(init_db_command)

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

app.teardown_appcontext(close_db)


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


