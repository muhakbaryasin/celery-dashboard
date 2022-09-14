from db.prod.ProdNativeQuery import TempProdNativeQuery


class QueryHelper(object):
    @staticmethod
    def get_comparators():
        return {
            0: '=',
            1: '!=',
            2: '<',
            3: '<=',
            4: '>',
            5: '>=',
            6: 'LIKE',
            7: 'NOT LIKE',
            8: 'IS NULL',
            9: 'IS NOT NULL'
        }

    @staticmethod
    def get_tables():
        return {
            0: 'brands',
            1: 'companies',
            2: 'copyrights',
            3: 'geographical_indication',
            4: 'industrial_design',
            5: 'patents'
        }

    @staticmethod
    def get_fields(table_name):
        fields = {}
        idx = 0

        for field in TempProdNativeQuery.get_field_list(table_name):
            fields[idx] = field
            idx += 1

        return fields

    @staticmethod
    def get_return_type():
        return {
            0: 'values',
            1: 'count'
        }

    @staticmethod
    def idx_to_fields(all_fields, columns):
        fields = []

        for idx in columns:
            fields.append(all_fields[idx])

        return fields

    @staticmethod
    def get_where_conjunction():
        return {
            0: 'OR',
            1: 'AND'
        }

    @staticmethod
    def create_query(table, selected_columns, return_type, where_clauses, order_by_columns, order_by_sort):
        table = QueryHelper.get_tables()[table]
        fields = QueryHelper.get_fields(table)

        if len(selected_columns) == 0:
            selected_columns = ['*']
        else:
            selected_columns = QueryHelper.idx_to_fields(fields, selected_columns)

        sql = "SELECT "

        if return_type == 1:
            sql = sql + "count({}) ".format(selected_columns[0])
        else:
            sql = sql + ", ".join(selected_columns)

        sql = sql + " FROM {}".format(table)
        where_idx = 0

        for each_clause in where_clauses:
            if len(each_clause) < 4:
                continue

            if where_idx == 0:
                sql = sql + " WHERE "
            where_idx += 1

            sql = sql + "{} {} {} ".format(fields[each_clause[0]], QueryHelper.get_comparators()[each_clause[1]], each_clause[2])

            if each_clause[3] is not None:
                sql = sql + "{} ".format(QueryHelper.get_where_conjunction()[each_clause[3]])

        if len(order_by_columns) > 0:
            order_by_columns = QueryHelper.idx_to_fields(fields, order_by_columns)
            sql = sql + " ORDER BY " + ", ".join(order_by_columns) + " {}".format('DESC' if order_by_sort == 1 else 'ASC')

        return sql
