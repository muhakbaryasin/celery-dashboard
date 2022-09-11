import json
import urllib.parse
from models.Scraper import Scraper


class FlowerClient(object):
    def __init__(self, client_name):
        self.client_name = client_name

    @property
    def api_base_url(self):
        with open('flower_apis.json', 'r') as f:
            return json.loads(f.read())[self.client_name]['url']

    def restart(self):
        endpoint_url = '/api/worker/pool/restart/celery@worker1'
        scraper = Scraper()
        scraper.request_data(url=self.api_base_url + endpoint_url, method='POST')

    def get_tasks_history(self, task_name=None, limit=100, offset=0, sort_by='started'):
        params = {'limit': limit, 'offset': offset, 'sorted_by': sort_by}

        if limit is None:
            del params['limit']

        if task_name is not None:
            params['taskname'] = task_name

        endpoint_url = '/api/tasks?{}'.format(urllib.parse.urlencode(params))
        scraper = Scraper()
        response = scraper.request_data(url=self.api_base_url + endpoint_url, method='GET')

        if response is None:
            raise Exception('Unable to get task list')

        return json.loads(response)

    def get_workers(self):
        scraper = Scraper()
        endpoint_url = '/api/workers'
        response = scraper.request_data(url=self.api_base_url + endpoint_url, method='GET')

        if response is None:
            raise Exception('Unable to get workers')

        return json.loads(response)

    def execute_task(self, task_name):
        task_ids = self.get_tasks_history(task_name)

        for id_ in task_ids:
            if task_ids[id_]['state'] == 'STARTED':
                raise Exception('The task is running')

        scraper = Scraper()
        endpoint_url = '/api/task/send-task/{}'.format(task_name)
        response = scraper.request_data(url=self.api_base_url + endpoint_url, method='POST')

        if response is None:
            raise Exception('Unable to execute task {}'.format(task_name))

    def terminate_task(self, task_id):
        scraper = Scraper()
        endpoint_url = '/api/task/revoke/{}?terminate=true'.format(task_id)
        response = scraper.request_data(url=self.api_base_url + endpoint_url, method='POST')

        if response is None:
            raise Exception('Unable to terminate task {}'.format(task_id))
