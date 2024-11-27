from flask import Flask, request, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

# Datenbank initialisieren
def init_db():
    conn = sqlite3.connect('newsletter.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE
        )
    ''')
    conn.commit()
    conn.close()

# Startseite mit HTML-Formular
@app.route('/')
def index():
    return render_template('index.html')

# E-Mail-Adresse speichern
@app.route('/submit', methods=['POST'])
def submit_email():
    email = request.form['email']
    conn = sqlite3.connect('newsletter.db')
    c = conn.cursor()
    try:
        c.execute('INSERT INTO emails (email) VALUES (?)', (email,))
        conn.commit()
        message = "E-Mail-Adresse erfolgreich gespeichert!"
    except sqlite3.IntegrityError:
        message = "Diese E-Mail-Adresse ist bereits registriert."
    conn.close()
    return f"<h1>{message}</h1><a href='/'>Zurück</a>"

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
