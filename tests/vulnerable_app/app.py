from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# ZAFİYETLİ UÇ NOKTA: SQL Injection ve Yetkisiz Erişim
@app.route('/user', methods=['GET'])
def get_user():
    user_id = request.args.get('id')
    
    # Doğrudan query birleştirme (SQL Injection)
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    query = f"SELECT id, username, email FROM users WHERE id = '{user_id}'"
    
    cursor.execute(query)
    user = cursor.fetchone()
    
    return jsonify({"user": user})

if __name__ == '__main__':
    app.run(debug=True)
