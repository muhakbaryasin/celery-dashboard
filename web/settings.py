from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module
from web.api.endpoints.CTask import CTask
from web.api.endpoints.CTaskHistory import CTaskHistory
from web.api.endpoints.CTaskTerminate import CTaskTerminate
from web.api.endpoints.CTaskMaxConcurrent import CTaskMaxConcurrent


cors = CORS()
db = SQLAlchemy()
login_manager = LoginManager()


def initialize_plugins(app):
    cors.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)


def register_blueprints(app):
    for module_name in ('authentication', 'home'):
        module = import_module('web.controllers.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)


def register_restful_api(app):
    api = Api(app)
    api.add_resource(CTask, "/v1/ctask")
    api.add_resource(CTaskHistory, "/v1/ctask/<string:task_name>/history", "/v1/ctask/<string:task_name>/history/<int:page>")
    api.add_resource(CTaskTerminate, "/v1/ctask/<string:task_id>/terminate")
    api.add_resource(CTaskMaxConcurrent, "/v1/ctask/max-concurrent", "/v1/ctask/max-concurrent/<int:number>")


def configure_database(app):
    @app.before_first_request
    def initialize_database():
        db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()


def initialize_flask_app():
    app = Flask(__name__)
    return app
