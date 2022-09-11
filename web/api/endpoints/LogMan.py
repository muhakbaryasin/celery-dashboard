from flask_restful import Resource
from web.api.BaseResponse import BaseResponse
from models.LogManager import LogManager


class LogMan(Resource):
    def get(self, client_name, opt_num=0, counter=0):
        response = BaseResponse()
        response.status = "ok"
        response.message = "success"

        response.data = LogManager().read_content(counter)

        return response.__dict__
