from io import StringIO
from iamtest.commons import util
import iamtest.commons.config as config
from iamtest.models.entity import service

def select_service(data):
    db = config.db_connection()
    
    search_option = util.make_search_option(data, ['service_name', 'service_url'])
    try:
        query = f'''
            SELECT
                service_id
                , service_name
                , service_url
            FROM
                service
        ''' 
        query += search_option + ';'
        
        if search_option != '':
            result = db.query(query, param=data, model=service.Service)
        else:
            result = db.query(query, model=service.Service)
  
        db.connection.commit()
        return result
    except Exception as error_msg:
        db.connection.rollback()
        raise(error_msg)

def insert_service(data):
    db = config.db_connection()
    try:
        insert_query = util.make_insert_query('service', data)
        select_query = 'SELECT @@IDENTITY AS service_id;'

        db.execute(insert_query, param=data)
        result = db.query_first(select_query, model=service.Service)

        db.connection.commit()
        return result
    except Exception as error_msg:
        db.connection.rollback()
        raise(error_msg)


def update_service(target_id, data):
    db = config.db_connection()
    update_values = util.make_entity_colums(data)
    try:
        query = f'''
            UPDATE
                service
            SET 
                {update_values}
            WHERE
                service_id = {target_id};
        '''

        result = db.execute(query, param=data)

        db.connection.commit()
        return result
    except Exception as error_msg:
        db.connection.rollback()
        raise(error_msg)


def delete_service(target_id):
    db = config.db_connection()
    try:
        query = '''
            DELETE FROM service WHERE service_id = ?service_id?;
        '''
        #TODO : 서비스 하위 리소스 및 권한 삭제
        
        result = db.execute(query, param={'service_id': target_id})
        db.connection.commit()
        return result
    except Exception as error_msg:
        db.connection.rollback()
        raise(error_msg)