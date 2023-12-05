from io import StringIO
from iamtest.commons import util
import iamtest.commons.config as config
from iamtest.models.entity import group

def select_group(data):
    db = config.db_connection()
    
    search_option = util.make_search_option(data, ['group_name', 'remark'])
    try:
        query = f'''
            SELECT
                group_id
                , group_name
                , remark
            FROM
                `group`
        ''' 
        query += search_option + ';'

        if search_option != '':
            result = db.query(query, param=data, model=group.Group)
        else:
            result = db.query(query, model=group.Group)

        db.connection.commit()
        return result
    except Exception as error_msg:
        db.connection.rollback()
        raise(error_msg)

def insert_group(data):
    db = config.db_connection()
    try:
        insert_query = util.make_insert_query('group', data)
        select_query = 'SELECT @@IDENTITY AS group_id;'

        db.execute(insert_query, param=data)
        result = db.query_first(select_query, model=group.Group)

        db.connection.commit()
        return result
    except Exception as error_msg:
        db.connection.rollback()
        raise(error_msg)

def update_group(target_id, data):
    db = config.db_connection()
    
    update_values = util.make_entity_colums(data)
    try:
        query = f'''
            UPDATE
                `group`
            SET 
                {update_values}
            WHERE
                group_id = {target_id};
        '''

        result = db.execute(query, param=data)

        db.connection.commit()
        return result
    except Exception as error_msg:
        db.connection.rollback()
        raise(error_msg)

def delete_group(target_id):
    db = config.db_connection()
    try:
        query = '''
            DELETE FROM `group` WHERE group_id = ?group_id?;
        '''

        result = db.execute(query, param={'group_id': target_id})

        db.connection.commit()
        return result
    except Exception as error_msg:
        db.connection.rollback()
        raise(error_msg)