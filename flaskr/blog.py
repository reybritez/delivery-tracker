from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db import get_db
import requests 
from requests.structures import CaseInsensitiveDict

bp = Blueprint('blog', __name__, template_folder='templates')

@bp.route('/')
def index():
    return render_template('restaurant/index.html')


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')

def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))

@bp.route('/blog')
def blog():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)

@bp.route('/api')
def api():
    server_key = "aDZtFNxtPm7RIuTIz5XvtbNpigZ7Em6gP"
    restaurant_token= "d3l1saj0" 
    restaurant_key = "M4RMbs8PoSnYYVD54"

    url = "https://pos.globalfoodsoft.com/pos/order/pop"

    headers = CaseInsensitiveDict()
    headers["Authorization"] = restaurant_key
    headers["Accept"] = "application/json"
    headers["Glf-Api-Version"] = "2"
    print(headers)

    resp = requests.post(url, headers=headers)
    print(resp) 
    resp = resp.json()
    print(resp['orders'])

    return resp

@bp.route('/muestra')
def muestra():
    obtencion = requests.get('https://delivery-trackerpy.herokuapp.com/api')
    obtencion = obtencion.json()
    print(obtencion)
    return render_template('blog/api.html', obtencion=obtencion)
