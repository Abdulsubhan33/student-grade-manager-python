from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def init_db():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS students
                 (name TEXT, rollno TEXT PRIMARY KEY, grade TEXT)''')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'admin':
            session['user'] = request.form['username']
            return redirect('/home')
        else:
            error = 'Invalid Credentials'
    return render_template('login.html', error=error)

@app.route('/home')
def index():
    if 'user' in session:
        return render_template('home.html', session=session)
    return redirect('/')

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    message = ''
    if request.method == 'POST':
        name = request.form['name']
        rollno = request.form['rollno']
        grade = request.form['grade']
        try:
            conn = sqlite3.connect('students.db')
            c = conn.cursor()
            c.execute("INSERT INTO students VALUES (?, ?, ?)", (name, rollno, grade))
            conn.commit()
            conn.close()
            return redirect('/view')
        except sqlite3.IntegrityError:
            message = 'Student with this roll number already exists.'
    return render_template('add.html', message=message)

@app.route('/view')
def view_students():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute("SELECT * FROM students")
    students = c.fetchall()
    conn.close()
    return render_template('view.html', students=students)

@app.route('/search', methods=['GET', 'POST'])
def search_student():
    result = None
    if request.method == 'POST':
        rollno = request.form['rollno']
        conn = sqlite3.connect('students.db')
        c = conn.cursor()
        c.execute("SELECT * FROM students WHERE rollno = ?", (rollno,))
        result = c.fetchone()
        conn.close()
    return render_template('search.html', result=result)

@app.route('/delete', methods=['GET', 'POST'])
def delete_student():
    message = ''
    if request.method == 'POST':
        rollno = request.form['rollno']
        conn = sqlite3.connect('students.db')
        c = conn.cursor()
        c.execute("DELETE FROM students WHERE rollno = ?", (rollno,))
        conn.commit()
        if c.rowcount:
            message = 'Student deleted successfully.'
        else:
            message = 'Student not found.'
        conn.close()
    return render_template('delete.html', message=message)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
