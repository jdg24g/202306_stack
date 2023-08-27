from app import app

from flask import render_template,redirect,flash,session,url_for

from app.models.user import User

from flask_bcrypt import Bcrypt
from flask import request

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    password = request.form['password']
    password_confirm = request.form['password_confirm']
    
    data = {
        'email': email,
    }
    user = User.get_by_email(data)

    if user:
        flash('Email already exists','danger')
        return redirect(url_for('index'))
    if password != password_confirm:
        flash('Passwords do not match','danger')
        return redirect(url_for('index'))
    
    password_hash = bcrypt.generate_password_hash(password)
    result = User.create({
        'email': email,
        'password': password_hash
    })

    if result:
        flash('Account created successfully','success')
    else:
        flash('Something went wrong','danger')
    return redirect(url_for('index'))


@app.route('/login/')
def login():
    email = request.form['email']
    password = request.form['password']

    data = {
        'email': email,
    }
    user = User.get_by_email(data)

    if not user:
        flash('Email not found','danger')
        return redirect(url_for('index'))
    
    check_password = bcrypt.check_password_hash(user.password, password)
    if check_password:
        session['user'] = {
            'id': user.id,
            'email': user.email
        }
        flash('Logged in successfully','info')
    else:
        flash('Error','danger')
        return redirect(url_for('index'))
    return redirect(url_for('dashboard'))

@app.route('/logout/')
def logout():
    if 'user' not in session:
        return redirect(url_for('index'))
    session.clear()
    flash('Logged out successfully','info')
    return redirect(url_for('index'))

@app.route('/dashboard/')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('index'))
    return render_template('dashboard/index.html')