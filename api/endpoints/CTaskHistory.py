from flask_restful import Resource
from api.BaseResponse import BaseResponse
from models.FlowerClient import FlowerClient

flower_client = FlowerClient()


class CTaskHistory(Resource):
    def get(self, task_name, page=1):
        response = BaseResponse()
        response.status = "ok"
        response.message = "success"
        task_history = flower_client.get_tasks_history(task_name=task_name, limit=5, sort_by='started', offset=(page - 1) * 5)
        response.data = task_history

        return response.__dict__
