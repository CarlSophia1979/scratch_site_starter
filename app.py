from flask import Flask, render_template, request, redirect, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Needed for flashing messages

# Home page
@app.route('/')
def home():
    return render_template('index.html')

# Signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        # Save user to the database
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                      (name, email, password))
            conn.commit()
            flash("Account created successfully!", "success")
            return redirect('/')
        except sqlite3.IntegrityError:
            flash("Email already exists!", "error")
        finally:
            conn.close()

    return render_template('signup.html')

# Login page (basic, coming soon)
@app.route('/login')
def login():
    return '<h2>Login Page Coming Soon</h2>'

# Run the app
if __name__ == '__main__':
    app.run(debug=True)

