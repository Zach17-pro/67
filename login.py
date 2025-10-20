from flask import render_template, redirect, url_for, request, session, flash
from app import app, db

@app.route('/')
def home():
    if 'user' in session:
        role = session['user']['role']
        if role == 'Admin':
            return redirect(url_for('Admin'))
        elif role == 'Platform_Manager':
            return redirect(url_for('Platform_Manager'))
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
        session['user'] = {
            'id': user['user_id'],
            'username': user['username'],
            'full_name': user['full_name'],
            'role': user['role']
        }
        
        flash(f"Welcome, {user['full_name']} ({user['role']})!")
        
        if user['role'] == 'Admin':
            return redirect(url_for('Admin'))
        elif user['role'] == 'Platform_Manager':
            return redirect(url_for('Platform_Manager'))
        elif user['role'] == 'PIN_Support':
            return redirect(url_for('PIN_Support'))
        elif user['role'] == 'Csr_Rep':
            return redirect(url_for('Csr_Rep'))
        else:
            return redirect(url_for('home'))
    else:
        flash("Invalid credentials!")
        return redirect(url_for('home'))

@app.route('/Admin')
def Admin():
    if 'user' not in session or session['user']['role'] != 'Admin':
        flash("Access denied!")
        return redirect(url_for('home'))
    return render_template('Admin.html', user=session['user'])

@app.route('/Platform_Manager')
def Platform_Manager():
    if 'user' not in session or session['user']['role'] != 'Platform_Manager':
        flash("Access denied!")
        return redirect(url_for('home'))
    return render_template('Platform_Manager.html', user=session['user'])

@app.route('/Csr_Rep')
def Csr_Rep():
    if 'user' not in session or session['user']['role'] != 'Csr_Rep':
        flash("Access denied!")
        return redirect(url_for('home'))
    return render_template('Csr_Rep.html', user=session['user'])

@app.route('/PIN_Support')
def PIN_Support():
    if 'user' not in session or session['user']['role'] != 'PIN_Support':
        flash("Access denied!")
        return redirect(url_for('home'))
    return render_template('PIN_Support.html', user=session['user'])

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("You have been logged out!")
    return redirect(url_for('home'))

@app.route('/test_db')
def test_db():
    try:
        cursor = db.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        cursor.close()
        return f"Database connection successful! Test query result: {result}"
    except Exception as e:
        return f"Database connection failed: {str(e)}"
