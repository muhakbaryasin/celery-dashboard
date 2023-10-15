from flask_restful import Resource
from web.api.BaseResponse import BaseResponse
from models.ClientConfigManager import ClientConfigManager


class BWListHandler(Resource):
    def post(self, action, client_name, file, value):
        response = BaseResponse()
        response.status = "ok"
        response.message = "success"

        data = {}

        base_dir = ClientConfigManager(client_name).project_base_dir +"/celery_app/"+file

        if value is not None:
            if action == 'add':
                with open(base_dir, 'a') as document:
                    document.write(value+'\n')
            elif action == 'remove':
                try:
                    with open(base_dir, 'r') as document:
                        lines = document.readlines()
                except IOError as e:
                    # print(f"An error occurred while reading the document: {e}")
                    lines = []
                

                lines = [line for line in lines if line.strip() != value]

                try:
                    with open(base_dir, 'w') as document:
                        document.writelines(lines)
                        # print(f"Line '{value}' removed successfully.")
                except IOError as e:
                    print(f"An error occurred while writing to the document: {e}")

                
        data['value'] = value
        data['dir'] = base_dir

        
        response.data = data

        return response.__dict__
