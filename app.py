from flask import Flask, render_template, request, redirect, flash, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this to something strong!

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

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                      (name, email, password))
            conn.commit()
            flash("Account created successfully! Please log in.", "success")
            return redirect('/login')
        except sqlite3.IntegrityError:
            flash("Email already exists!", "error")
        finally:
            conn.close()

    return render_template('signup.html')

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
        user = c.fetchone()
        conn.close()

        if user:
            session['user_id'] = user[0]  # Save user id in session
            flash("Logged in successfully!", "success")
            return redirect('/')
        else:
            flash("Incorrect email or password.", "error")

    return render_template('login.html')

# Logout route (optional if you want)
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("Logged out successfully!", "success")
    return redirect('/login')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)

