from io import StringIO
from iamtest.commons import util
import iamtest.commons.config as config
from iamtest.models.entity import user

def select_info(target_id):
    db = config.db_connection()
    
    try:
        query = f'''
            SELECT
                id AS employee_id
                , employee_name
                , employee_email
                , `rank`
            FROM
                employee
            WHERE
                id = ?employee_id?
        ''' 

        result = db.query(query, param={'employee_id' : target_id}, model=user.Employee)
        
        db.connection.commit()
        return result
    except Exception as error_msg:
        db.connection.rollback()
        raise(error_msg)