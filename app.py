from flask import Flask, request, jsonify, render_template
import mysql.connector
import os

app = Flask(__name__)

# Read from environment variables (Kubernetes will inject these)
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "crud_db")
}

def get_db():
    return mysql.connector.connect(**DB_CONFIG)

@app.route('/')
def index():
    return render_template('index.html')

# CREATE
@app.route('/items', methods=['POST'])
def create_item():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO items (name) VALUES (%s)", (data['name'],))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Item created"})

# READ
@app.route('/items', methods=['GET'])
def get_items():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM items")
    items = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(items)

# UPDATE
@app.route('/items/<int:id>', methods=['PUT'])
def update_item(id):
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE items SET name=%s WHERE id=%s", (data['name'], id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Item updated"})

# DELETE
@app.route('/items/<int:id>', methods=['DELETE'])
def delete_item(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM items WHERE id=%s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Item deleted"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)