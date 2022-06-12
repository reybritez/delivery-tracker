import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    # Crea y configura la app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='st3vdev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        # Carga la configuracion instanciada, si existe cuando no se esta testeando
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        # Carga el test config si ha pasado
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    # Se asegura que la carpeta instanciada exista
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/holi')
    def holi():
        return 'Holi Stevencin!'

    from . import db, auth, blog
    db.init_app(app)
    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')
    return app