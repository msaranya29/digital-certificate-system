from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    certificate_id = request.form['certificate_id']
    course = request.form['course']

    conn = sqlite3.connect('certificates.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS certificates
                 (name TEXT, certificate_id TEXT, course TEXT)''')
    c.execute("INSERT INTO certificates VALUES (?, ?, ?)", (name, certificate_id, course))
    conn.commit()
    conn.close()

    return "Certificate issued successfully!"

@app.route('/verify', methods=['GET', 'POST'])
def verify():
    if request.method == 'POST':
        certificate_id = request.form['certificate_id']
        conn = sqlite3.connect('certificates.db')
        c = conn.cursor()
        c.execute("SELECT * FROM certificates WHERE certificate_id=?", (certificate_id,))
        result = c.fetchone()
        conn.close()
        if result:
            return "Certificate is valid."
        else:
            return "Certificate not found."
    return render_template('verify.html')

if __name__ == '__main__':
    app.run(debug=True)

