from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module
from web.api.endpoints.CApps import CApps
from web.api.endpoints.CTask import CTask
from web.api.endpoints.CTaskHistory import CTaskHistory
from web.api.endpoints.CTaskExecute import CTaskExecute
from web.api.endpoints.CTaskTerminate import CTaskTerminate
from web.api.endpoints.CTaskMaxConcurrent import CTaskMaxConcurrent
from web.api.endpoints.QueryHelper import QueryHelperFields, QueryHelperTables, QueryHelperReturnType, \
    QueryHelperComparators, QueryHelperSql
from web.api.endpoints.NotificationFile import NotificationFile
from web.api.endpoints.NotificationView import NotificationView
from web.api.endpoints.LogMan import LogMan


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
    api.add_resource(CApps, "/v1/capps")
    api.add_resource(CTask, "/v1/ctask/<string:client_name>")
    api.add_resource(CTaskHistory, "/v1/ctask/<string:client_name>/<string:task_name>/history",
                     "/v1/ctask/<string:client_name>/<string:task_name>/history/<int:page>")
    api.add_resource(CTaskExecute, "/v1/ctask/<string:client_name>/<string:task_name>/execute")
    api.add_resource(CTaskTerminate, "/v1/ctask/<string:client_name>/<string:task_id>/terminate")
    api.add_resource(CTaskMaxConcurrent, "/v1/ctask/<string:client_name>/max-concurrent",
                     "/v1/ctask/<string:client_name>/max-concurrent/<int:number>")
    api.add_resource(QueryHelperTables, "/v1/query-helper/tables")
    api.add_resource(QueryHelperFields, "/v1/query-helper/<int:table_idx>/fields")
    api.add_resource(QueryHelperComparators, "/v1/query-helper/comparators")
    api.add_resource(QueryHelperReturnType, "/v1/query-helper/return-type")
    api.add_resource(QueryHelperSql, "/v1/query-helper/sql")
    api.add_resource(NotificationFile, "/v1/notifications", "/v1/notifications/<string:notification_name>")
    api.add_resource(NotificationView, "/v1/notifications/<string:notification_name>/view")
    api.add_resource(LogMan, "/v1/logs/<string:client_name>",
                     "/v1/logs/<string:client_name>/<int:index>/<int:line_end_no>",
                     "/v1/logs/<string:client_name>/<int:index>")


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
