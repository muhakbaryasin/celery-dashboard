from models.xmlsettings import XMLSettings


class TaskManager(object):
    task_list = None
    max_concurrent_task = None

    @staticmethod
    def get_max_concurrent_task():
        return int(TaskManager.get_config().get('max-concurrent-task', 2))

    @staticmethod
    def get_config():
        return XMLSettings('conf_xml/TaskManager.xml')

    @staticmethod
    def set_max_concurrent_task(max_concurrent_task):
        if max_concurrent_task > 4:
            raise Exception('{} is over the max allowed concurrent task which is 4'.format(max_concurrent_task))

        config = TaskManager.get_config()
        config.put('max-concurrent-task', max_concurrent_task)
        config.save()
