from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from api.endpoints.CTask import CTask
from api.endpoints.CTaskHistory import CTaskHistory
from api.endpoints.CTaskTerminate import CTaskTerminate


cors = CORS()


def initialize_plugins(app):
    cors.init_app(app)


def register_restful_api(app):
    api = Api(app)
    api.add_resource(CTask, "/v1/ctask")
    api.add_resource(CTaskHistory, "/v1/ctask/<string:task_name>/history")
    api.add_resource(CTaskTerminate, "/v1/ctask/<string:task_id>/terminate")


def initialize_flask_app():
    app = Flask(__name__)
    return app
