from flask import Flask, request, render_template_string, session, redirect, url_for
import sqlite3
import hashlib

app = Flask(__name__)
app.secret_key = 'a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6'

# Initialize the database
def init_db(conn):
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')
    conn.commit()

# Route to handle the main page
@app.route('/', methods=['GET', 'POST'])
def home():
    conn = sqlite3.connect(':memory:')
    init_db(conn)
    c = conn.cursor()
    if 'logged_in' in session:
        if request.method == 'POST':
            return redirect(url_for('logout'))
        c.execute("SELECT * FROM users")
        users = c.fetchall()
        conn.close()
        return render_template_string('''
            <h1>Registered Users:</h1>
            <ul>
                {% for user in users %}
                    <li>{{ user[1] }}</li>
                {% endfor %}
            </ul>
            <form method="post">
                <input type="submit" value="Logout">
            </form>
        ''', users=users)
    else:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            c.execute("SELECT * FROM users WHERE username = ?", (username,))
            user = c.fetchone()
            if user and user[2] == hashlib.sha256(password.encode()).hexdigest():
                session['logged_in'] = True
                session['username'] = username
                return redirect(url_for('home'))
            else:
                return 'Invalid username or password'
        c.execute("SELECT * FROM users")
        users = c.fetchall()
        conn.close()
        return render_template_string('''
            <h1>Login</h1>
            <form method="post">
                Username: <input type="text" name="username"><br>
                Password: <input type="password" name="password"><br>
                <input type="submit" value="Login">
            </form>
            <h1>Register</h1>
            <form action="/register" method="post">
                Username: <input type="text" name="username"><br>
                Password: <input type="password" name="password"><br>
                <input type="submit" value="Register">
            </form>
        ''', users=users)

@app.route('/register', methods=['GET', 'POST'])
def register():
    conn = sqlite3.connect(':memory:')
    init_db(conn)
    c = conn.cursor()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashlib.sha256(password.encode()).hexdigest()))
        conn.commit()
        conn.close()
        return redirect(url_for('home'))
    conn.close()
    return render_template_string('''
        <h1>Register</h1>
        <form method="post">
            Username: <input type="text" name="username"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Register">
        </form>
    ''')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
