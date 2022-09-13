import json


class ClientConfigManager(object):
    config_json = 'flower_apis.json'

    def __init__(self, client_name):
        self.client_name = client_name

    @property
    def api_base_url(self):
        with open(self.config_json, 'r') as f:
            return json.loads(f.read())[self.client_name]['url']

    @property
    def project_base_dir(self):
        with open(self.config_json, 'r') as f:
            return json.loads(f.read())[self.client_name]['project_base_dir']
