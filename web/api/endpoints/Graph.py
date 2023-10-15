import mysql.connector
from flask_restful import Resource
from web.api.BaseResponse import BaseResponse
from models.SqlData import SqlData

class Graph(Resource):
    def get(self):
        response = BaseResponse()
        response.status = "ok"
        response.message = "success"

        australia = SqlData('prod_australia','companies').get_data()
        colombia = SqlData('prod_colombia','companies').get_data()
        indonesia = SqlData('prod_id','companies').get_data()
        malaysia = SqlData('prod_my','companies').get_data()
        philippines = SqlData('prod_ph','companies').get_data()
        singapore = SqlData('prod_sg','companies').get_data()

        # return data
        data = {
            'australia': australia[0],
            'colombia': colombia[0],
            'indonesia': indonesia[0],
            'malaysia': malaysia[0],
            'philippines': philippines[0],
            'singapore': singapore[0],
        }
        
        response.data = data

        return response.__dict__
