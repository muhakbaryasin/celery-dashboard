from flask_restful import Resource
from web.api.BaseResponse import BaseResponse
from models.FlowerClient import FlowerClient


class CTask(Resource):
    def get(self, client_name):
        flower_client = FlowerClient(client_name)
        response = BaseResponse()
        response.status = "ok"
        response.message = "success"
        task_history = flower_client.get_tasks_history(limit=None, sort_by='name')
        registered_tasks = flower_client.get_workers()
        sorted_tasks = {}

        for worker_name in registered_tasks.keys():
            for task_name in registered_tasks[worker_name]['registered']:
                sorted_tasks[task_name] = {
                    'latest_id': None,
                    'latest_started': None,
                    'latest_status': None,
                    'runtime_average': 0,
                    'executed_times': 0
                }
            break

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

            if task_history[key]['started'] is not None and (sorted_tasks[task_history[key]['name']]['latest_started'] is None or task_history[key]['started'] > sorted_tasks[task_history[key]['name']]['latest_started']):
                sorted_tasks[task_history[key]['name']]['latest_id'] = task_history[key]['uuid']
                sorted_tasks[task_history[key]['name']]['latest_started'] = task_history[key]['started']
                sorted_tasks[task_history[key]['name']]['latest_status'] = task_history[key]['state']

        response.data = sorted_tasks

        return response.__dict__
