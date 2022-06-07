from flask_restful import Resource
from api.BaseResponse import BaseResponse
from celery_app.TaskManager import TaskManager


class CTaskMaxConcurrent(Resource):
    def get(self, number=None):
        response = BaseResponse()
        response.status = "ok"
        response.message = "success"
        response.data = TaskManager().get_max_concurrent_task()

        return response.__dict__

    def put(self, number=None):
        response = BaseResponse()
        response.status = "ok"
        response.message = "success"

        if number is not None:
            TaskManager().set_max_concurrent_task(number)

        response.data = number

        return response.__dict__
