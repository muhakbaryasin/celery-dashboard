from flask_restful import Resource
from web.api.BaseResponse import BaseResponse
import json


class CApps(Resource):
    def get(self):
        response = BaseResponse()
        response.status = "ok"
        response.message = "success"

        with open('flower_apis.json', 'r') as f:
            response.data = [key for key in json.loads(f.read())]

        return response.__dict__
