from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

# Initialize the database
def init_db():
    conn = sqlite3.connect(':memory:')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)''')
    conn.commit()
    conn.close()

# Route to handle the main page
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        user_name = request.form['name']
        conn = sqlite3.connect(':memory:')
        c = conn.cursor()
        c.execute("INSERT INTO users (name) VALUES (?)", (user_name,))
        conn.commit()
        conn.close()
        return f"User {user_name} added successfully!"
    
    # Fetch all users from the database
    conn = sqlite3.connect(':memory:')
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    users = c.fetchall()
    conn.close()
    
    # Render a simple HTML form and display users
    return render_template_string('''
        <h1>User Registration</h1>
        <form method="post">
            Name: <input type="text" name="name"><br>
            <input type="submit" value="Register">
        </form>
        <h2>Registered Users:</h2>
        <ul>
            {% for user in users %}
                <li>{{ user[1] }}</li>
            {% endfor %}
        </ul>
    ''', users=users)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
