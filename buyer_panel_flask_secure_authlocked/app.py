
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# DB Setup
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS buyers (
            id INTEGER PRIMARY KEY,
            name TEXT,
            path TEXT UNIQUE,
            message TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def admin():
    conn = sqlite3.connect('database.db')
    buyers = conn.cursor().execute('SELECT * FROM buyers').fetchall()
    conn.close()
    return render_template('index.html', buyers=buyers)

@app.route('/create', methods=['POST'])
def create():
    name = request.form['name']
    path = request.form['path']
    message = request.form['message']
    conn = sqlite3.connect('database.db')
    try:
        conn.execute('INSERT INTO buyers (name, path, message) VALUES (?, ?, ?)',
                     (name, path, message))
        conn.commit()
    except:
        return "Path must be unique.", 400
    finally:
        conn.close()
    return redirect('/')

@app.route('/welcome/<custom_path>', methods=['GET', 'POST'])
def welcome(custom_path):
    if request.method == 'POST':
        input_code = request.form['auth_code']
        if input_code != "AAZTOPEDWELCOMEMESSAGEINVT12@@#2909":
            return "Invalid authorization code.", 403
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('SELECT message FROM buyers WHERE path = ?', (custom_path,))
        result = c.fetchone()
        conn.close()
        if result:
            return render_template('buyer_view.html', message=result[0])
        else:
            return "Invalid path.", 404
    return render_template('auth_form.html', custom_path=custom_path)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
