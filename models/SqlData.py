import mysql.connector
from datetime import datetime

class SqlData(object):
    def __init__(self, database, table):
        self.database = database
        self.table = table
        self.today = datetime.now().strftime('%Y-%m-%d')

    def db_connection(self):
        conf = {
            'host': '127.0.0.1',
            'user': 'root',
            'password': 'pass1234',
            'database': self.database,
        }

        return conf
    
    def get_data(self):
        connection = mysql.connector.connect(**self.db_connection())
        cursor = connection.cursor()

        query = f"""
            SELECT 
                (SELECT count(`id`) FROM `{self.table}` WHERE `created_at` LIKE '{self.today}%') as created, 
                (SELECT count(`id`) FROM `{self.table}` WHERE `updated_at` LIKE '{self.today}%') as updated,
                (SELECT count(`id`) FROM `{self.table}`) as total
        """
        
        cursor.execute(query)
        results = cursor.fetchall()

        return results

    
