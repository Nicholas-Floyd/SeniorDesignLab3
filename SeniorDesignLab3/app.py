import os
import sqlite3
from flask import Flask, render_template, request, jsonify, current_app, g, redirect, url_for, flash, session
from flask.cli import with_appcontext
import click
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Ensure instance folder exists
instance_path = os.path.join(os.getcwd(), 'instance')
if not os.path.exists(instance_path):
    os.makedirs(instance_path)

app.config['DATABASE'] = os.path.join(instance_path, 'flaskr.sqlite')


def init_db():
    db = get_db()
    # Make sure you have a `schema.sql` file in a `database` directory
    with app.open_resource('Database/schema.sql', mode='r') as f:
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
            # If login is successful, you might store user info in session
            session['user_id'] = user['id']
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')
            return redirect(url_for('login'))

    # If GET request, just show the login form
    return render_template('login.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/team_member/<name>')
def team_member(name):
    valid_names = ['nick', 'alex', 'michael', 'robby']
    name = name.lower()
    if name in valid_names:
        return render_template(f'{name}.html', name=name.capitalize())
    else:
        return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)


