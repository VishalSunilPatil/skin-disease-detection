from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__)
    app.secret_key = '1010101010'

    from . import project
    app.register_blueprint(project.bp)

    return app
