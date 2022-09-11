from flask_restful import Resource
from web.api.BaseResponse import BaseResponse
from models.TaskManager import TaskManager


class CTaskMaxConcurrent(Resource):
    def get(self, client_name, number=None):
        response = BaseResponse()
        response.status = "ok"
        response.message = "success"
        response.data = TaskManager.get_max_concurrent_task()

        return response.__dict__

    def put(self, client_name, number=None):
        response = BaseResponse()
        response.status = "ok"
        response.message = "success"

        if number is not None:
            TaskManager.set_max_concurrent_task(number)

        response.data = number

        return response.__dict__
