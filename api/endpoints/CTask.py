from flask_restful import Resource
from api.BaseResponse import BaseResponse
from models.FlowerClient import FlowerClient

flower_client = FlowerClient()


class CTask(Resource):
    def get(self):
        response = BaseResponse()
        response.status = "ok"
        response.message = "success"
        task_history = flower_client.get_tasks_history()
        sorted_tasks = {}

        for key in task_history.keys():
            if task_history[key]['name'] not in sorted_tasks:
                sorted_tasks[task_history[key]['name']] = {
                    'latest_id': task_history[key]['uuid'],
                    'latest_started': task_history[key]['started'],
                    'latest_status': task_history[key]['state'],
                    'runtime_average': task_history[key]['runtime'],
                    'executed_times': 1
                }
                continue

            sorted_tasks[task_history[key]['name']]['executed_times'] = sorted_tasks[task_history[key]['name']]['executed_times'] + 1

            if task_history[key]['runtime'] is not None and sorted_tasks[task_history[key]['name']]['runtime_average'] is not None:
                sorted_tasks[task_history[key]['name']]['runtime_average'] = (sorted_tasks[task_history[key]['name']]['runtime_average'] + task_history[key]['runtime']) / 2
            elif task_history[key]['runtime'] is not None:
                sorted_tasks[task_history[key]['name']]['runtime_average'] = task_history[key]['runtime']

            if task_history[key]['started'] > sorted_tasks[task_history[key]['name']]['latest_started']:
                sorted_tasks[task_history[key]['name']]['latest_id'] = task_history[key]['uuid']
                sorted_tasks[task_history[key]['name']]['latest_started'] = task_history[key]['started']
                sorted_tasks[task_history[key]['name']]['latest_status'] = task_history[key]['state']

        sorted_tasks = {k: v for k, v in sorted(sorted_tasks.items(), key=lambda item: item[0])}
        response.data = sorted_tasks

        return response.__dict__
