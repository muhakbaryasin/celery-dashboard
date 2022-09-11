from flask import request
from flask_restful import Resource
from web.api.BaseResponse import BaseResponse
from models.QueryHelper import QueryHelper


class QueryHelperFields(Resource):
    def get(self, table_idx=None):
        response = BaseResponse()
        response.status = "ok"
        response.message = "success"

        if table_idx is not None:
            table_name = QueryHelper.get_tables()[table_idx]
            response.data = [value for value in QueryHelper.get_fields(table_name).values()]

        return response.__dict__


class QueryHelperTables(Resource):
    def get(self):
        response = BaseResponse()
        response.status = "ok"
        response.message = "success"
        response.data = [value for value in QueryHelper.get_tables().values()]

        return response.__dict__


class QueryHelperReturnType(Resource):
    def get(self):
        response = BaseResponse()
        response.status = "ok"
        response.message = "success"
        response.data = [value for value in QueryHelper.get_return_type().values()]

        return response.__dict__


class QueryHelperComparators(Resource):
    def get(self):
        response = BaseResponse()
        response.status = "ok"
        response.message = "success"
        response.data = [value for value in QueryHelper.get_comparators().values()]

        return response.__dict__


class QueryHelperSql(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        response = BaseResponse()
        response.status = "ok"
        response.message = "success"
        response.data = QueryHelper.create_query(json_data['table'], json_data['columns'], json_data['return_type'],
                                                 json_data['where_clauses'], json_data['order_by_columns'],
                                                 json_data['order_by_sort'])

        return response.__dict__
