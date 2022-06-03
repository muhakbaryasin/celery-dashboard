from flask_restful import Resource
from api.BaseResponse import BaseResponse
from models.FlowerClient import FlowerClient

flower_client = FlowerClient()


class CTaskHistory(Resource):
    def get(self, task_name):
        response = BaseResponse()
        response.status = "ok"
        response.message = "success"
        task_history = flower_client.get_tasks_history()
        filtered_tasks = {key: val for key, val in task_history.items() if val['name'] == task_name}
        sorted_tasks = {k: v for k, v in sorted(filtered_tasks.items(), key=lambda item: item[1]['started'], reverse=True)}
        response.data = sorted_tasks

        return response.__dict__
