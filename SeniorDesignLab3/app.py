from datetime import datetime
import random
import secrets
import string
from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import select
# from database import db
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # Replace with your secret key

# Database configuration (adjust accordingly)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # For local development
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db.init_app(app)
# migrate = Migrate(app, db)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/team_member/<int:member_id>')
def team_member(member_id):
    return render_template(f'team_member_{member_id}.html', member_id=member_id)

if __name__ == '__main__':
    app.run(debug=True)
