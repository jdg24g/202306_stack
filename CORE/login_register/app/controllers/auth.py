import re

from flask import flash, redirect, render_template, request, session, url_for
from flask_bcrypt import Bcrypt

from app import app
from app.models.user import User

bcrypt = Bcrypt(app)

regex = re.compile(r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+")

def email_validator(email):
    if(regex.fullmatch(email)):
        return True
    else:
        return False
    
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('dashboard'))

    return render_template('auth/index.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('index'))
    user = session
    print(user)
    return render_template('dashboard/index.html')


@app.route('/register', methods=['POST'])
def register():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']

    if not first_name or not last_name or not email or not password or not confirm_password:
        flash('Por favor relleno todos los campos', 'danger')
        return redirect(url_for('index'))
    
    if len(first_name) < 2 or len(last_name) < 2:
        flash('Nombre y apellido deben tener al menos 2 caracteres', 'danger')
        return redirect(url_for('index'))
    
    if len(password) < 8:
        flash('La contraseña debe tener al menos 8 caracteres', 'danger')
        return redirect(url_for('index'))
    
    if email_validator(email) == False:
        flash('Email no válido', 'danger')
        return redirect(url_for('index'))
    
    if password != confirm_password:
        flash('Las contraseñas no coinciden', 'danger')
        return redirect(url_for('index'))
    
    user = User.get_by_email(email)

    if user:
        flash('El Correo ya está registrado', 'danger')
        return redirect(url_for('index'))
    
    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    user_data = {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'password': password_hash
    }

    result = User.save_user(user_data)

    if result:
        flash('Usuario registrado correctamente', 'success')
        return redirect(url_for('index'))
    else:
        flash('Ocurrio un error al registrar el usuario', 'danger')
        return redirect(url_for('index'))
    
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    if not email or not password:
        flash('Por favor relleno todos los campos', 'danger')
        return redirect(url_for('index'))
    
    data = {'email': email}
    user = User.get_by_email(data)
    print(f'el resultado de user = {user}')

    if user == None:
        flash('El correo no está registrado', 'danger')
        return redirect(url_for('index'))
    
    if email == user.email and bcrypt.check_password_hash(user.password,password):
        session['user'] = {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
            }
        flash(f'Bienvenido {user.first_name}', 'success')
        return redirect(url_for('dashboard'))
    else:
        flash('Credenciales incorrectas', 'danger')
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    if 'user' not in session:
        return redirect(url_for('index'))
    
    session.clear()
    flash('Sesión cerrada', 'success')
    return redirect(url_for('index'))