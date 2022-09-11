from flask_restful import Resource
from web.api.BaseResponse import BaseResponse
from models.NotificationFilesManager import NotificationFilesManager


class NotificationView(Resource):
    def get(self, notification_name=None):
        response = BaseResponse()
        response.status = "ok"
        response.message = "success"
        view = NotificationFilesManager.create_view(notification_name)
        response.data = {'text': view[0], 'rows': view[1]}

        return response.__dict__
