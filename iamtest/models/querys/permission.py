from io import StringIO
from iamtest.commons import util
import iamtest.commons.config as config
from iamtest.models.entity import permission

def select_permission(data):
    db = config.db_connection()
    search_option = util.make_search_option(data, ['permission_name', 'remark'])
    try:
        query = f'''
            SELECT
                permission_id
                , service_id
                , resource_id
                , permission_name
                , permission
                , remark
            FROM
                permission
        ''' 
        query += search_option + ';'      

        print(query)
        if search_option != '':
            result = db.query(query, param=data, model=permission.Permission)
        else:
            result = db.query(query, model=permission.Permission)
        db.connection.commit()
        return result
    except Exception as error_msg:
        db.connection.rollback()
        raise(error_msg)


def insert_permission(data):
    db = config.db_connection()
    try:
        insert_query = util.make_insert_query('permission', data)
        select_query = 'SELECT @@IDENTITY AS permission_id;'

        db.execute(insert_query, param=data)
        result = db.query_first(select_query, model=permission.Permission)

        db.connection.commit()
        return result
    except Exception as error_msg:
        db.connection.rollback()
        raise(error_msg)


def update_permission(target_id, data):
    db = config.db_connection()
    
    update_values = util.make_entity_colums(data)
    try:
        query = f'''
            UPDATE
                permission
            SET 
                {update_values}
            WHERE
                permission_id = {target_id};
        '''

        result = db.execute(query, param=data)

        db.connection.commit()
        return result
    except Exception as error_msg:
        db.connection.rollback()
        raise(error_msg)


def delete_permission(target_id):
    db = config.db_connection()
    try:
        query = '''
            DELETE FROM permission WHERE permission_id = ?permission_id?;
        '''
        #TODO : 할당되어있는 권한정보 삭제(user_permission, group_permission)
        
        result = db.execute(query, param={'permission_id': target_id})

        db.connection.commit()
        return result
    except Exception as error_msg:
        db.connection.rollback()
        raise(error_msg)