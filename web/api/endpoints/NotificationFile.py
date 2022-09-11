from flask import request
from flask_restful import Resource
from web.api.BaseResponse import BaseResponse
from models.NotificationFilesManager import NotificationFilesManager


class NotificationFile(Resource):
    def get(self, notification_name=None):
        response = BaseResponse()
        response.status = "ok"
        response.message = "success"

        if notification_name is None:
            response.data = NotificationFilesManager.get_list()
        else:
            response.data = NotificationFilesManager.get(notification_name)

        return response.__dict__

    def post(self, notification_name=None):
        response = BaseResponse()
        response.status = "ok"
        response.message = "success"
        json_data = request.get_json(force=True)
        text = json_data['text']

        if notification_name is not None and text is not None:
            NotificationFilesManager.save(notification_name, text)

        response.data = notification_name

        return response.__dict__
