from time import sleep
from datetime import date
from celery_app.tasks import task1, task2, task3, task4
from models.xmlsettings import XMLSettings


class TaskManager(object):
    __instance = None
    task_list = None
    max_concurrent_task = None

    def __new__(cls, *args):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls, *args)
        return cls.__instance

    def get_task_list(self):
        return self.task_list

    def get_max_concurrent_task(self):
        return int(self.get_config().get('max-concurrent-task', 2))

    @staticmethod
    def get_config():
        return XMLSettings('conf_xml/TaskManager.xml')

    def set_max_concurrent_task(self, max_concurrent_task):
        if max_concurrent_task > 4:
            raise Exception('{} is over the max allowed concurrent task which is 4'.format(max_concurrent_task))

        config = self.get_config()
        config.put('max-concurrent-task', max_concurrent_task)
        config.save()

    @staticmethod
    def write_running_task_log(task_list):
        with open('taskmanager.log', 'w') as f:
            f.write(str(task_list))

    def __init__(self):
        config = self.get_config()

        if self.task_list is None:
            self.task_list = [
                {"name": task1.__name__, "res": None, "day": None, "func": task1},
                {"name": task2.__name__, "res": None, "day": None, "func": task2},
                {"name": task3.__name__, "res": None, "day": None, "func": task3},
                {"name": task4.__name__, "res": None, "day": None, "func": task4},
            ]

        self.max_concurrent_task = self.get_max_concurrent_task()
        config.put('max-concurrent-task', self.max_concurrent_task)
        config.save()

    def run(self):
        running_task = []
        tasks_num = len(self.task_list)
        task_id = 0
        next_p_task_id = None
        sleep(5)

        while True:
            for each_task in self.task_list:
                if each_task['res'] is not None \
                        and (each_task['res'].state == "SUCCESS" or each_task['res'].state == "FAILURE" or each_task['res'].state == "REVOKED") \
                        and each_task['name'] in running_task:
                    running_task.remove(each_task['name'])
                    each_task['res'] = None

            each_task = self.task_list[task_id]
            each_task['task_id'] = task_id

            if len(running_task) >= self.get_max_concurrent_task():
                sleep(1)
                continue

            task_id = (task_id + 1) % tasks_num
            persist_running_task = list(filter(lambda x: (x[0] == 'p'), running_task))

            if each_task['res'] is not None and each_task['res'].state == "STARTED":
                sleep(1)
                continue
            elif each_task['name'][0] == 'p':
                if next_p_task_id is None:
                    next_p_task_id = each_task['task_id']

                if len(persist_running_task) > 0 or each_task['task_id'] != next_p_task_id:
                    sleep(1)
                    continue
                elif each_task['task_id'] == next_p_task_id:
                    next_p_task_id = None
            elif each_task['name'][0] == 'd' and str(date.today()) == each_task['day']:
                sleep(1)
                continue

            if each_task['name'] not in running_task:
                each_task['res'] = each_task['func'].delay()
                running_task.append(each_task['name'])

                if 'day' in each_task:
                    each_task['day'] = str(date.today())

                self.write_running_task_log(running_task)
                sleep(1)

