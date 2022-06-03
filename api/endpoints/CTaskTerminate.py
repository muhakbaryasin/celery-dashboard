from flask_restful import Resource
from api.BaseResponse import BaseResponse
from models.FlowerClient import FlowerClient

flower_client = FlowerClient()


class CTaskTerminate(Resource):
    def delete(self, task_id):
        flower_client.terminate_task(task_id)
        response = BaseResponse()
        response.status = "ok"
        response.message = "success"

        return response.__dict__
