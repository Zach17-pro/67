from flask import Flask, render_template, redirect, url_for, request, session, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'secret123'  # needed for flash messages

# MySQL configuration
db = mysql.connector.connect(
    host="localhost",
    user="root",          # change to your MySQL username
    password="1111",  # change to your MySQL password
    database="SixSeven"     # your database name
)


@app.route('/')
def home():
    # Check if user is already logged in and redirect to appropriate dashboard
    if 'user' in session:
        role = session['user']['role']
        if role == 'admin':
            return redirect(url_for('admin'))
        elif role == 'manager':
            return redirect(url_for('manager'))
        else:
            return redirect(url_for('user'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    profile = request.form['profiles']

    cursor = db.cursor(dictionary=True)
    query = "SELECT * FROM users WHERE username = %s AND password = %s AND role = %s"
    cursor.execute(query, (username, password, profile))
    user = cursor.fetchone()
    cursor.close()

    if user:
        # Store user info in session
        session['user'] = {
            'id': user['id'],
            'username': user['username'],
            'full_name': user['full_name'],
            'role': user['role']
        }
        
        flash(f"Welcome, {user['full_name']} ({user['role']})!")
        
        # Redirect based on role
        if user['role'] == 'admin':
            return redirect(url_for('admin'))
        elif user['role'] == 'manager':
            return redirect(url_for('manager'))
        else:
            return redirect(url_for('user'))
    else:
        flash("Invalid credentials!")
        return redirect(url_for('home'))

# Different dashboards for different roles
@app.route('/admin/dashboard')
def admin():
    if 'user' not in session or session['user']['role'] != 'admin':
        flash("Access denied!")
        return redirect(url_for('home'))
    return render_template('admin.html', user=session['user'])

@app.route('/manager/dashboard')
def manager():
    if 'user' not in session or session['user']['role'] != 'manager':
        flash("Access denied!")
        return redirect(url_for('home'))
    return render_template('manager.html', user=session['user'])

@app.route('/user/dashboard')
def user():
    if 'user' not in session:
        flash("Please log in first!")
        return redirect(url_for('home'))
    return render_template('user.html', user=session['user'])

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("You have been logged out!")
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)