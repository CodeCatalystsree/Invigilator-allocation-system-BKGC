from flask import Flask, render_template, request, redirect, url_for, session, flash
import pymysql
import pandas as pd
from duty_ga import run_ga_allocation  # Import your GA function
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# DB connection
conn = pymysql.connect(host="localhost", user="root", password="", database="duty_allo")
cursor = conn.cursor()

# ----------- ROUTES -----------

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['username']
        password = request.form['password']

        cursor.execute("SELECT * FROM teachers WHERE username=%s AND password=%s", (name, password))
        data = cursor.fetchone()
        if data:
            session['user'] = name
            return redirect(url_for('selection'))
        else:
            flash('Invalid Credentials', 'danger')
    return render_template('login100.html')


@app.route('/selection', methods=['GET', 'POST'])
def selection():
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        # You can use these inputs later if needed in GA
        semester = request.form['semester']
        exam_month = request.form['month']
        exam_date = request.form['exam_date']
        
        # Save to session
        session['semester'] = semester
        session['month'] = exam_month
        session['exam_date'] = exam_date

        # Run GA here
        run_ga_allocation("duty_allo_input.xlsx")  # Save result to final_duty_allocation100.xlsx
        return redirect(url_for('dashboard'))

    return render_template('selection100.html')


@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))

    df = pd.read_excel("final_duty_allocation100.xlsx")
    records = df.to_dict(orient='records')
    return render_template('dash100.html', allocations=records, user=session['user'])


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
