import os
import csv
from flask import Flask, request, render_template_string, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'secretkey'  # Needed for session management

filename = "grades.txt"
USERNAME = "admin"
PASSWORD = "1234"

# Create the grades file with header
if not os.path.exists(filename) or os.stat(filename).st_size == 0:
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Roll Number", "Grade"])

# ---------- ROUTES ----------

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == USERNAME and password == PASSWORD:
            session['user'] = username
            return redirect(url_for('index'))
        else:
            error = 'Invalid credentials. Try again.'
    return render_template_string('''
        <h2>Login</h2>
        <form method="post">
            Username: <input name="username"><br>
            Password: <input name="password" type="password"><br>
            <input type="submit" value="Login">
        </form>
        <p style="color:red;">{{ error }}</p>
    ''', error=error)

# Logout route
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

# Home page / main menu
@app.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template_string('''
        <h1>Welcome, {{ session["user"] }}!</h1>
        <a href="/add">Add Student</a> |
        <a href="/view">View Students</a> |
        <a href="/search">Search Student</a> |
        <a href="/delete">Delete Student</a> |
        <a href="/logout">Logout</a>
    ''', session=session)

# Add student
@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if 'user' not in session:
        return redirect(url_for('login'))
    message = ''
    if request.method == 'POST':
        name = request.form['name'].strip()
        rollno = request.form['rollno'].strip()
        grade = request.form['grade'].strip()

        if not name or not rollno or not grade:
            message = "All fields are required."
        else:
            with open(filename, 'r') as f:
                for line in f:
                    if rollno in line:
                        message = f"Roll number {rollno} already exists."
                        break
                else:
                    with open(filename, 'a') as f:
                        f.write(f"{name},{rollno},{grade}\n")
                        return redirect(url_for('view_students'))

    return render_template_string('''
        <h2>Add Student</h2>
        <form method="post">
            Name: <input name="name"><br>
            Roll No: <input name="rollno"><br>
            Grade: <input name="grade"><br>
            <input type="submit" value="Add Student">
        </form>
        <p style="color:red;">{{ message }}</p>
        <a href="/">Back to Home</a>
    ''', message=message)

# View students
@app.route('/view')
def view_students():
    if 'user' not in session:
        return redirect(url_for('login'))
    students = []
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            next(reader)
            students = list(reader)
    except FileNotFoundError:
        pass
    return render_template_string('''
        <h2>All Students</h2>
        <table border="1">
            <tr><th>Name</th><th>Roll Number</th><th>Grade</th></tr>
            {% for s in students %}
                <tr><td>{{ s[0] }}</td><td>{{ s[1] }}</td><td>{{ s[2] }}</td></tr>
            {% endfor %}
        </table>
        <a href="/">Back to Home</a>
    ''', students=students)

# Search student
@app.route('/search', methods=['GET', 'POST'])
def search_student():
    if 'user' not in session:
        return redirect(url_for('login'))
    result = None
    if request.method == 'POST':
        rollno = request.form['rollno'].strip()
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                if row[1] == rollno:
                    result = row
                    break
    return render_template_string('''
        <h2>Search Student</h2>
        <form method="post">
            Enter Roll Number: <input name="rollno">
            <input type="submit" value="Search">
        </form>
        {% if result %}
            <p><strong>Found:</strong> Name: {{ result[0] }}, Roll No: {{ result[1] }}, Grade: {{ result[2] }}</p>
        {% elif result is not none %}
            <p style="color:red;">Record not found.</p>
        {% endif %}
        <a href="/">Back to Home</a>
    ''', result=result)

# Delete student
@app.route('/delete', methods=['GET', 'POST'])
def delete_student():
    if 'user' not in session:
        return redirect(url_for('login'))
    message = ''
    if request.method == 'POST':
        rollno = request.form['rollno'].strip()
        lines = []
        found = False

        with open(filename, 'r') as f:
            lines = f.readlines()

        with open(filename, 'w') as f:
            for line in lines:
                if rollno in line:
                    found = True
                    continue
                f.write(line)

        message = f"Record with Roll Number {rollno} deleted." if found else "Record not found."
    return render_template_string('''
        <h2>Delete Student</h2>
        <form method="post">
            Enter Roll Number: <input name="rollno">
            <input type="submit" value="Delete">
        </form>
        <p>{{ message }}</p>
        <a href="/">Back to Home</a>
    ''', message=message)

# ---------- Run App ----------
if __name__ == "__main__":
    app.run(debug=True)
