from flask import Blueprint, request, render_template, redirect, url_for
from werkzeug.security import check_password_hash
import mysql.connector

# db conn
db = mysql.connector.connect(
    host="",
    user="",
    password="",
    database=""
)

cursor = db.cursor()

login_blueprint = Blueprint('login', __name__)

@login_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # db username check
        cursor.execute("SELECT password FROM users WHERE username=%s", (username,))
        result = cursor.fetchone()

        # user exists
        if result is not None:
            # match password
            if check_password_hash(results[0], password):
                return redirect(url_for('index'))
            else:
                return "Incorrect password"
        else:
            return "Incorrect username"
    else:
        return render_template('login.html')
