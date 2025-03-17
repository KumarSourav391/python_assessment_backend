from flask import Flask
from http import HTTPStatus
from app.settings import db, ma
from dotenv import  load_dotenv,find_dotenv

load_dotenv(find_dotenv())

def create_app(test_config=None):

    app = Flask(__name__)

    if test_config is None:
        app.config.from_pyfile("config.py")
    else:
        app.config.update(test_config)

    from app.api import api_home
    app.register_blueprint(api_home,url_prefix="/home")

    from app.api.product import api_upload_csv
    app.register_blueprint(api_upload_csv,url_prefix="/api/")

    db.init_app(app)

    ma.init_app(app)


    @app.errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR)
    def handle_error(e):
        db.engine.dispose()

    @app.teardown_appcontext
    def app_close_handle(e):
        db.engine.dispose()

    return app