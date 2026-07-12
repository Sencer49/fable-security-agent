from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/user', methods=['GET'])
def get_user():
    user_id = request.args.get('id')
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # Parametreli sorgu kullanımı (SQL Injection Önleme)
    query = 'SELECT id, username, email FROM users WHERE id = ?'
    cursor.execute(query, (user_id,))
    user = cursor.fetchone()
    return jsonify({'user': user})

if __name__ == '__main__':
    app.run(debug=False)