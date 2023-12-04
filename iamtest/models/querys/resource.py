from io import StringIO
from iamtest.models.entity import resource
from iamtest.commons import util
import iamtest.commons.config as config

def select_resource(data):
    db = config.db_connection()
    
    search_option = util.make_search_option(data, ['group_name', 'remark'])
    try:
        query = f'''
            SELECT
                resource_id
                , service_id
                , name
                , remark
            FROM
                resource
        ''' 
        query += search_option + ';'
        
        if search_option != '':
            result = db.query(query, param=data, model=resource.Resource)
        else:
            result = db.query(query, model=resource.Resource)

        db.connection.commit()
        return result
    except Exception as error_msg:
        db.connection.rollback()
        raise(error_msg)

def insert_resource(data):
    db = config.db_connection()
    try:
        insert_query = util.make_insert_query('resource', data)
        select_query = 'SELECT @@IDENTITY AS resource_id;'

        db.execute(insert_query, param=data)
        result = db.query_first(select_query, param=data, model=resource.Resource)

        db.connection.commit()
        return result
    except Exception as error_msg:
        db.connection.rollback()
        raise(error_msg)

def update_resource(target_id, data):
    db = config.db_connection()
    update_values = util.make_entity_colums(data)
    try:
        query = f'''
            UPDATE
                resource
            SET 
                {update_values}
            WHERE
                resource_id = {target_id};
        '''
        
        result = db.execute(query, param=data)

        db.connection.commit()
        return result
    except Exception as error_msg:
        db.connection.rollback()
        raise(error_msg)


def delete_resource(target_id):
    db = config.db_connection()
    try:
        query = '''
            DELETE FROM resource WHERE resource_id = ?resource_id?;
        '''
        #TODO : 리소스 하위 권한 삭제
        
        result = db.execute(query, param={'resource_id': target_id})
        db.connection.commit()
        return result
    except Exception as error_msg:
        db.connection.rollback()
        raise(error_msg)