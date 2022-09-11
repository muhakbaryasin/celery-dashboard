import os
import base64
import json
from models.QueryHelper import QueryHelper
from db.prod.ProdNativeQuery import TempProdNativeQuery


class NotificationFilesManager(object):
    path_location = './notifications'

    @staticmethod
    def get_list():
        res = []

        for file in os.listdir(NotificationFilesManager.path_location):
            if file.endswith('.txt'):
                res.append(file.replace('.txt', ''))

        return res

    @staticmethod
    def save(name, text):
        if name.find('/') > -1:
            raise Exception('Name could not contain /')

        if name.find('.') > -1:
            raise Exception('Name could not contain .')

        b64_text = base64.b64encode(text.encode('utf-8'))
        with open(NotificationFilesManager.path_location + "/{}.txt".format(name), 'wb') as f:
            f.write(b64_text)

    @staticmethod
    def get(name):
        file_list = NotificationFilesManager.get_list()

        if name in file_list:
            with open(NotificationFilesManager.path_location + "/{}.txt".format(name), 'rb') as f:
                b64_text = f.read()
                return base64.b64decode(b64_text).decode('utf-8')
        else: raise Exception('Notification {} not found'.format(name))

    @staticmethod
    def create_view(name):
        content = NotificationFilesManager.get(name)
        content_split = content.split('\n')
        rows = len(content_split)

        for line in content_split:
            open_bracket = line.find('[')

            if open_bracket == -1:
                continue

            close_bracket = -1

            try:
                while line[close_bracket+1:].find(']') > -1:
                    close_bracket = 1 + close_bracket + line[close_bracket+1:].find(']')
            except:
                pass

            if close_bracket == -1:
                break

            sql_template_text = line[open_bracket+1:close_bracket]
            sql_template_json = json.loads(sql_template_text)
            sql_query = QueryHelper.create_query(sql_template_json['table'], sql_template_json['columns'],
                                                 sql_template_json['return_type'], sql_template_json['where_clauses'],
                                                 sql_template_json['order_by_columns'], sql_template_json['order_by_sort'])
            result_list = []
            query_result = TempProdNativeQuery.run(sql_query, result=True, result_many=False)
            for key in query_result:
                result_list.append("({}) {}".format(key, query_result[key]))
            result_str = ", ".join(result_list)
            content = content.replace(sql_template_text, result_str)

        return content, rows




