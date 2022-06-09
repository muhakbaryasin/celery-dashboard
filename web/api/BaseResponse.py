from flask_restful import fields


class BaseResponse(object):
    status = ""
    message = ""
    data = None


resource_fields = {
    'status': fields.String,
    'message': fields.String,
    'reason': fields.String,
}
