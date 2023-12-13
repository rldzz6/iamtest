from io import StringIO
from iamtest.commons import util
from iamtest.commons import config
from iamtest.models.entity import user

def select_info(conn, target_id):
    try:
        query = f'''
            SELECT
                employee_id
                , employee_name
                , employee_mail
                , employee_rank
            FROM
                employee
            WHERE
                id = {target_id};
        '''

        with conn.cursor() as cur:
            cur.execute(query)
            columns = cur.description
            result = [{columns[index][0]:column for index, column in enumerate(value)} for value in cur.fetchall()]
            return result
    except Exception as error:
        raise Exception(error)
