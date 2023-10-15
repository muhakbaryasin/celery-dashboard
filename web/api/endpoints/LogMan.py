from flask_restful import Resource
from web.api.BaseResponse import BaseResponse
from models.LogManager import LogManager


class LogMan(Resource):
    def get(self, client_name, type, index=None, line_end_no=None):
        response = BaseResponse()
        response.status = "ok"
        response.message = "success"
        log_man = LogManager(client_name, type)
        list_ = log_man.get_list(need_full_path=False)
        data = {'list': list_, 'total_lines': 0}

        if index is not None:
            if line_end_no is None or line_end_no == 0:
                name, content, total_lines = log_man.tail_file(index)
            else:
                name, content, total_lines = log_man.read_content(index, line_end_no=line_end_no+1)

            del data['total_lines']
            data['name'] = name
            data['content']= content
            data['total_lines'] = total_lines

        response.data = data

        return response.__dict__
