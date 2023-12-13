from io import StringIO
from iamtest.commons import util
from iamtest.commons import config
from iamtest.models.entity import user
import iamtest.models.entity.user as Entity

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
                employee_id = '{target_id}';
        '''

        with conn.cursor() as cur:
            cur.execute(query)
            result = [Entity.Model(data=data).data for data in cur.fetchall()]
            return result, cur.rowcount
    except Exception as error:
        raise Exception(error)
