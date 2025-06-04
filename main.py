from flask import Flask, render_template_string, request, redirect, session
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
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
<div class="container mt-5">
    <div class="card mx-auto" style="max-width: 400px;">
        <div class="card-body">
            <h3 class="card-title text-center mb-4">Login</h3>
            <form method="post">
                <div class="mb-3">
                    <label>Username</label>
                    <input name="username" class="form-control" required>
                </div>
                <div class="mb-3">
                    <label>Password</label>
                    <input name="password" type="password" class="form-control" required>
                </div>
                <button type="submit" class="btn btn-primary w-100">Login</button>
            </form>
            {% if error %}
                <div class="alert alert-danger mt-3">{{ error }}</div>
            {% endif %}
        </div>
    </div>
</div>
</body>
</html>
''', error=error)

@app.route('/home')
def index():
    if 'user' in session:
        return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <title>Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
<div class="container mt-5">
    <h1 class="mb-4">Welcome, {{ session["user"] }}!</h1>
    <div class="d-flex flex-wrap gap-2">
        <a href="/add" class="btn btn-success">Add Student</a>
        <a href="/view" class="btn btn-info">View Students</a>
        <a href="/search" class="btn btn-warning">Search Student</a>
        <a href="/delete" class="btn btn-danger">Delete Student</a>
        <a href="/logout" class="btn btn-secondary">Logout</a>
    </div>
</div>
</body>
</html>
''', session=session)
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
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <title>Add Student</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
<div class="container mt-5">
    <div class="card mx-auto" style="max-width: 500px;">
        <div class="card-body">
            <h3 class="card-title text-center mb-4">Add Student</h3>
            <form method="post">
                <div class="mb-3">
                    <label>Name</label>
                    <input name="name" class="form-control" required>
                </div>
                <div class="mb-3">
                    <label>Roll No</label>
                    <input name="rollno" class="form-control" required>
                </div>
                <div class="mb-3">
                    <label>Grade</label>
                    <input name="grade" class="form-control" required>
                </div>
                <button type="submit" class="btn btn-success w-100">Add Student</button>
            </form>
            {% if message %}
                <div class="alert alert-danger mt-3">{{ message }}</div>
            {% endif %}
            <a href="/home" class="btn btn-link mt-3">Back to Home</a>
        </div>
    </div>
</div>
</body>
</html>
''', message=message)

@app.route('/view')
def view_students():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute("SELECT * FROM students")
    students = c.fetchall()
    conn.close()
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <title>View Students</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
<div class="container mt-5">
    <h2 class="mb-4">All Students</h2>
    <table class="table table-striped table-bordered">
        <thead class="table-dark">
            <tr><th>Name</th><th>Roll Number</th><th>Grade</th></tr>
        </thead>
        <tbody>
            {% for s in students %}
                <tr><td>{{ s[0] }}</td><td>{{ s[1] }}</td><td>{{ s[2] }}</td></tr>
            {% endfor %}
        </tbody>
    </table>
    <a href="/home" class="btn btn-link">Back to Home</a>
</div>
</body>
</html>
''', students=students)

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
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <title>Search Student</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
<div class="container mt-5">
    <h2 class="mb-4">Search Student</h2>
    <form method="post" class="mb-3">
        <div class="input-group">
            <input name="rollno" class="form-control" placeholder="Enter Roll Number" required>
            <button class="btn btn-warning" type="submit">Search</button>
        </div>
    </form>
    {% if result %}
        <div class="alert alert-success">Found: <strong>{{ result[0] }}</strong>, Roll No: {{ result[1] }}, Grade: {{ result[2] }}</div>
    {% elif result is not none %}
        <div class="alert alert-danger">Record not found.</div>
    {% endif %}
    <a href="/home" class="btn btn-link">Back to Home</a>
</div>
</body>
</html>
''', result=result)

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
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <title>Delete Student</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
<div class="container mt-5">
    <h2 class="mb-4">Delete Student</h2>
    <form method="post" class="mb-3">
        <div class="input-group">
            <input name="rollno" class="form-control" placeholder="Enter Roll Number" required>
            <button class="btn btn-danger" type="submit">Delete</button>
        </div>
    </form>
    {% if message %}
        <div class="alert alert-info">{{ message }}</div>
    {% endif %}
    <a href="/home" class="btn btn-link">Back to Home</a>
</div>
</body>
</html>
''', message=message)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
