from flask_restful import Resource
from web.api.BaseResponse import BaseResponse
from models.LogManager import LogManager


class LogMan(Resource):
    def get(self, client_name, index, line_end_no=None):
        response = BaseResponse()
        response.status = "ok"
        response.message = "success"

        response.data = LogManager(client_name).read_content(index, line_end_no=line_end_no)

        return response.__dict__
