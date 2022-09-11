from db.MysqlNativeQuery import MysqlNativeQuery


class TempProdNativeQuery(object):
    @staticmethod
    def run(query, values=(), result=False, result_many=False):
        return MysqlNativeQuery.run(query, values=values, result=result, result_many=result_many, db_name='prod_id')

    @staticmethod
    def get_tables():
        sql = """
        SHOW TABLES
        """

        result = TempProdNativeQuery.run(sql, [], result=True, result_many=True)
        return [row['Tables_in_temp_prod'] for row in result]

    @staticmethod
    def get_field_list(table_name):
        sql = """
        SHOW COLUMNS from {}
        """.format(table_name)

        result = TempProdNativeQuery.run(sql, [], result=True, result_many=True)
        return [row['Field'] for row in result]
