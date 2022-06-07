import json
import urllib.parse

from models.Scraper import Scraper


class FlowerClient(object):
    api_base_url = 'http://localhost:5566'

    def __init__(self):
        self.scraper = Scraper()

    def restart(self):
        endpoint_url = '/api/worker/pool/restart/celery@worker1'
        self.scraper.request_data(url=self.api_base_url + endpoint_url, method='POST')

    def get_tasks_history(self, task_name=None, limit=100, offset=0, sort_by='started'):
        params = {'limit': limit, 'offset': offset, 'sorted_by': sort_by}

        if limit is None:
            del params['limit']

        if task_name is not None:
            params['taskname'] = task_name

        endpoint_url = '/api/tasks?{}'.format(urllib.parse.urlencode(params))
        response = self.scraper.request_data(url=self.api_base_url + endpoint_url, method='GET')

        if response is None:
            raise Exception('Unable to get task list')

        return json.loads(response)

    def get_workers(self):
        endpoint_url = '/api/workers'
        response = self.scraper.request_data(url=self.api_base_url + endpoint_url, method='GET')

        if response is None:
            raise Exception('Unable to get workers')

        return json.loads(response)

    def terminate_task(self, task_id):
        endpoint_url = '/api/task/revoke/{}?terminate=true'.format(task_id)
        response = self.scraper.request_data(url=self.api_base_url + endpoint_url, method='POST')

        if response is None:
            raise Exception('Unable to terminate task {}'.format(task_id))
