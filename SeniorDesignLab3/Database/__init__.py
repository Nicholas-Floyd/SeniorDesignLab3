import sqlite3
import click
from flask import current_app, g
from werkzeug.security import generate_password_hash
from flask.cli import with_appcontext

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    with current_app.open_resource('database/schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

    # Insert default user and team members
    default_user = ('defaultUser', generate_password_hash('Fall2024Lab3'))
    team_members = [
        ('team_member1', generate_password_hash('password1')),
        ('team_member2', generate_password_hash('password2')),
        ('team_member3', generate_password_hash('password3')),
        ('team_member4', generate_password_hash('password4'))
    ]
    db.executemany('INSERT OR REPLACE INTO users (username, password) VALUES (?, ?)',
                   [default_user] + team_members)
    db.commit()

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
