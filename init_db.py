import mysql.connector

conn = mysql.connector.connect(
    host="localhost:3360",
    user="root",         # ← Replace this
    password="saru"      # ← Replace this
)

cursor = conn.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS certificates_db")
cursor.execute("USE certificates_db")

cursor.execute("""
CREATE TABLE IF NOT EXISTS certificates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    course VARCHAR(100) NOT NULL,
    date DATE NOT NULL
)
""")

conn.commit()
cursor.close()
conn.close()
