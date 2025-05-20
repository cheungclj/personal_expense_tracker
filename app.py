from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Important for security

DATABASE = 'instance/expenses.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    with open('schema.sql') as f:  # Create schema.sql (see below)
        conn.executescript(f.read())
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = get_db_connection()
    if request.method == 'POST':
        date_str = request.form['date']
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()  # Convert string to date
        except ValueError:
            date = datetime.now().date()

        category = request.form['category']
        description = request.form['description']
        amount = float(request.form['amount'])

        conn.execute("INSERT INTO expenses (date, category, description, amount) VALUES (?, ?, ?, ?)",
                     (date, category, description, amount))
        conn.commit()
        return redirect(url_for('index'))

    expenses = conn.execute("SELECT * FROM expenses ORDER BY date DESC").fetchall()
    conn.close()
    return render_template('index.html', expenses=expenses)

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM expenses WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        init_db()  # Initialize database on first run
    app.run(debug=True)
