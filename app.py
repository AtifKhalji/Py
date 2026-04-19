from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        date TEXT,
        status TEXT
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS activities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        activity TEXT,
        date TEXT
    )''')

    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/attendance', methods=['GET', 'POST'])
def attendance():
    if request.method == 'POST':
        name = request.form['name']
        status = request.form['status']
        date = datetime.now().strftime("%Y-%m-%d")

        conn = sqlite3.connect('attendance.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO attendance (name, date, status) VALUES (?, ?, ?)",
                       (name, date, status))
        conn.commit()
        conn.close()

        return redirect('/view_attendance')

    return render_template('attendance.html')

@app.route('/view_attendance')
def view_attendance():
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM attendance")
    data = cursor.fetchall()
    conn.close()

    return render_template('view_attendance.html', data=data)

@app.route('/activity', methods=['GET', 'POST'])
def activity():
    if request.method == 'POST':
        name = request.form['name']
        activity = request.form['activity']
        date = datetime.now().strftime("%Y-%m-%d")

        conn = sqlite3.connect('attendance.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO activities (name, activity, date) VALUES (?, ?, ?)",
                       (name, activity, date))
        conn.commit()
        conn.close()

        return redirect('/view_activity')

    return render_template('activity.html')

@app.route('/view_activity')
def view_activity():
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM activities")
    data = cursor.fetchall()
    conn.close()

    return render_template('view_activity.html', data=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)