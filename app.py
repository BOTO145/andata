from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

# Database initialization
def init_db():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS data (id INTEGER PRIMARY KEY, timestamp TEXT, value TEXT)')
    conn.commit()
    conn.close()

@app.route('/store', methods=['POST'])
def store_data():
    data = request.json
    timestamp = data.get('timestamp')
    value = data.get('value')

    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('INSERT INTO data (timestamp, value) VALUES (?, ?)', (timestamp, value))
    conn.commit()
    conn.close()

    return jsonify({"message": "Data stored successfully"}), 201

@app.route('/data', methods=['GET'])
def get_data():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('SELECT * FROM data')
    rows = c.fetchall()
    conn.close()
    return jsonify(rows)

@app.route('/')
def index():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('SELECT * FROM data')
    rows = c.fetchall()
    conn.close()
    return render_template('index.html', rows=rows)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
