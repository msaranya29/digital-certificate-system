from flask import Flask, render_template, request
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# MySQL Database Connection (Directly in app.py)
def get_connection():
    try:
        # Establish a connection to the MySQL database
        connection = mysql.connector.connect(
            host="127.0.0.1",  # e.g. "localhost" or use Replit MySQL hostname
            user="root",  # e.g. "root"
            password="saru",  # password for the MySQL user
            database="Local Instance MySQL80"  # e.g. "certificate_db"
        )
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None

# Route to issue certificates
@app.route('/', methods=['GET', 'POST'])
def issue_certificate():
    if request.method == 'POST':
        name = request.form['name']
        course = request.form['course']
        date = request.form['date']

        conn = get_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO certificates (name, course, date) VALUES (%s, %s, %s)", (name, course, date))
            conn.commit()
            cursor.close()
            conn.close()

            return "✅ Certificate Issued!"
        else:
            return "❌ Error connecting to the database."

    return render_template('form.html')

# Route to verify certificates
@app.route('/verify', methods=['GET', 'POST'])
def verify_certificate():
    if request.method == 'POST':
        certificate_id = request.form['certificate_id']

        conn = get_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM certificates WHERE id = %s", (certificate_id,))
            certificate = cursor.fetchone()

            cursor.close()
            conn.close()

            if certificate:
                return render_template('verify.html', certificate=certificate)
            else:
                return "❌ Certificate not found."
        else:
            return "❌ Error connecting to the database."

    return render_template('verify.html', certificate=None)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


