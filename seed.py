import mysql.connector

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",  # change this
    "database": "crud_db"
}

conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

items = [
    ("Item 1",),
    ("Item 2",),
    ("Item 3",)
]

cursor.executemany("INSERT INTO items (name) VALUES (%s)", items)

conn.commit()
cursor.close()
conn.close()

print("Seed data inserted!")