from flask_restful import Resource
from web.api.BaseResponse import BaseResponse
from models.FlowerClient import FlowerClient


class CTaskExecute(Resource):
    def post(self, client_name, task_name):
        flower_client = FlowerClient(client_name)
        flower_client.execute_task(task_name)
        response = BaseResponse()
        response.status = "ok"
        response.message = "success"

        return response.__dict__
