import functools #Importa functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
) # Dependencias de Flask
from werkzeug.security import check_password_hash, generate_password_hash # werkzeug security tools

from flaskr.db import get_db # Agarra la base de datos

bp = Blueprint('auth', __name__, url_prefix='/auth') # Crea el objeto blueprint

# Primera vista para registro
@bp.route('/register', methods=('GET', 'POST')) # Registra la vista
def register(): # En la funcion Register
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db() # Obtiene la base de datos
        error = None

        if not username:
            error = 'El Username es obligatorio.'
        elif not password:
            error = 'El Password es obligatorio.'

        if error is None: #Si no hay errores ejecuta esto
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"El usuario {username} ya esta registrado."
            else: #Sino Esto
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone() #El fetchone devuelve una sola fila

        if user is None: #Verifica si existe el dato en la fila devuelta
            error = 'Username incorrecto o No existe.'
        elif not check_password_hash(user['password'], password):
            error = 'Password Incorrecto.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
    