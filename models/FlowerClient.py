import json
from models.Scraper import Scraper


class FlowerClient(object):
    api_base_url = 'http://localhost:5566'

    def __init__(self):
        self.scraper = Scraper()

    def restart(self):
        endpoint_url = '/api/worker/pool/restart/celery@worker1'
        self.scraper.request_data(url=self.api_base_url + endpoint_url, method='POST')

    def get_tasks_history(self):
        endpoint_url = '/api/tasks'
        response = self.scraper.request_data(url=self.api_base_url + endpoint_url, method='GET')

        if response is None:
            raise Exception('Unable to get task list')

        return json.loads(response)

    def get_workers(self):
        endpoint_url = '/api/workers'
        response = self.scraper.request_data(url=self.api_base_url + endpoint_url, method='GET')

        if response is None:
            raise Exception('Unable to get workers')

        return json.loads(response).keys[0]

    def terminate_task(self, task_id):
        endpoint_url = '/api/task/revoke/{}?terminate=true'.format(task_id)
        response = self.scraper.request_data(url=self.api_base_url + endpoint_url, method='POST')

        if response is None:
            raise Exception('Unable to terminate task {}'.format(task_id))
