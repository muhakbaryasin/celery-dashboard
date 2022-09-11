from flask_restful import Resource
from web.api.BaseResponse import BaseResponse
from models.FlowerClient import FlowerClient


class CTaskTerminate(Resource):
    def delete(self, client_name, task_id):
        flower_client = FlowerClient(client_name)
        flower_client.terminate_task(task_id)
        response = BaseResponse()
        response.status = "ok"
        response.message = "success"

        return response.__dict__
